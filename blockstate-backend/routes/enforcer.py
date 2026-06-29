"""
Enforcer Routes
API endpoints for starting, stopping, and monitoring the system enforcer
"""

from fastapi import APIRouter, HTTPException
from typing import List
import logging
from datetime import datetime

from models import (
    EnforcerStartRequest, EnforcerStopRequest, EnforcerStatus,
    APIResponse
)
from services.hosts_manager import hosts_manager
from services.process_enforcer import process_enforcer
from services.session_manager import session_manager

logger = logging.getLogger(__name__)

router = APIRouter()

# Global enforcer state
enforcer_state = {
    "is_active": False,
    "current_session_id": None,
    "workflow_id": None,
    "start_time": None
}

@router.post("/start")
async def start_enforcer(request: EnforcerStartRequest):
    """
    Start the system enforcer for a focus session
    
    Args:
        request: EnforcerStartRequest with workflow_id and duration
        
    Returns:
        APIResponse with session details
    """
    try:
        # Create a new session
        session = session_manager.create_session(
            workflow_id=request.workflow_id,
            duration_minutes=request.duration_minutes,
            strict_mode=request.strict_mode
        )
        
        # Update enforcer state
        enforcer_state["is_active"] = True
        enforcer_state["current_session_id"] = session["id"]
        enforcer_state["workflow_id"] = request.workflow_id
        enforcer_state["start_time"] = datetime.now().isoformat()
        
        logger.info(f"Enforcer started for session {session['id']}")
        
        return APIResponse(
            success=True,
            message="Enforcer started successfully",
            data={
                "session_id": session["id"],
                "workflow_id": request.workflow_id,
                "duration_minutes": request.duration_minutes,
                "strict_mode": request.strict_mode
            }
        )
        
    except Exception as e:
        logger.error(f"Error starting enforcer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_enforcer(request: EnforcerStopRequest):
    """
    Stop the system enforcer and end the focus session
    
    Args:
        request: EnforcerStopRequest with session_id
        
    Returns:
        APIResponse with session summary
    """
    try:
        # End the session
        session = session_manager.end_session(request.session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Clear blocked domains and processes
        success, msg = hosts_manager.clear_all_blockstate_entries()
        logger.info(f"Cleared hosts file: {msg}")
        
        # Update enforcer state
        enforcer_state["is_active"] = False
        enforcer_state["current_session_id"] = None
        enforcer_state["workflow_id"] = None
        enforcer_state["start_time"] = None
        
        logger.info(f"Enforcer stopped for session {request.session_id}")
        
        return APIResponse(
            success=True,
            message="Enforcer stopped successfully",
            data={
                "session_id": request.session_id,
                "status": session["status"],
                "distractions_blocked": session["distractions_blocked"],
                "processes_terminated": len(session["processes_terminated"])
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error stopping enforcer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_enforcer_status() -> EnforcerStatus:
    """
    Get current enforcer status
    
    Returns:
        EnforcerStatus with current state
    """
    try:
        blocked_procs = process_enforcer.find_blocked_processes()
        blocked_domains = hosts_manager.get_blocked_domains()
        
        return EnforcerStatus(
            is_active=enforcer_state["is_active"],
            current_session_id=enforcer_state["current_session_id"],
            workflow_id=enforcer_state["workflow_id"],
            blocked_processes=[p["name"] for p in blocked_procs],
            blocked_domains=blocked_domains,
            processes_monitored=len(process_enforcer.get_running_processes()),
            uptime_seconds=0  # TODO: Calculate from start_time
        )
    except Exception as e:
        logger.error(f"Error getting enforcer status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enforce")
async def enforce_now():
    """
    Manually trigger enforcement check and process termination
    
    Returns:
        APIResponse with enforcement results
    """
    try:
        if not enforcer_state["is_active"]:
            raise HTTPException(status_code=400, detail="Enforcer is not active")
        
        # Monitor and enforce
        stats = process_enforcer.monitor_and_enforce()
        
        # Update session with terminated processes
        session_id = enforcer_state["current_session_id"]
        for proc_name in stats["processes_terminated"]:
            session_manager.add_process_terminated(session_id, proc_name)
        
        # Increment distraction count
        if stats["blocked_terminated"] > 0:
            session = session_manager.get_session(session_id)
            session_manager.update_session(session_id, {
                "distractions_blocked": session["distractions_blocked"] + stats["blocked_terminated"]
            })
        
        logger.info(f"Enforcement executed: {stats}")
        
        return APIResponse(
            success=True,
            message="Enforcement executed",
            data=stats
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during enforcement: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/processes/blocked")
async def get_blocked_processes():
    """Get list of currently running blocked processes"""
    try:
        blocked = process_enforcer.find_blocked_processes()
        return APIResponse(
            success=True,
            message=f"Found {len(blocked)} blocked processes",
            data={"processes": blocked}
        )
    except Exception as e:
        logger.error(f"Error getting blocked processes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/processes/all")
async def get_all_processes():
    """Get list of all running processes"""
    try:
        processes = process_enforcer.get_running_processes()
        return APIResponse(
            success=True,
            message=f"Found {len(processes)} running processes",
            data={"processes": processes}
        )
    except Exception as e:
        logger.error(f"Error getting all processes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/domains/block")
async def block_domains(domains: List[str]):
    """
    Add domains to the hosts file to block them
    
    Args:
        domains: List of domains to block
        
    Returns:
        APIResponse with result
    """
    try:
        success, message = hosts_manager.add_blocked_domains(domains)
        
        if success:
            return APIResponse(
                success=True,
                message=message,
                data={"domains_blocked": len(domains)}
            )
        else:
            raise HTTPException(status_code=500, detail=message)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error blocking domains: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/domains/unblock")
async def unblock_domains(domains: List[str]):
    """
    Remove domains from the hosts file to unblock them
    
    Args:
        domains: List of domains to unblock
        
    Returns:
        APIResponse with result
    """
    try:
        success, message = hosts_manager.remove_blocked_domains(domains)
        
        if success:
            return APIResponse(
                success=True,
                message=message,
                data={"domains_unblocked": len(domains)}
            )
        else:
            raise HTTPException(status_code=500, detail=message)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error unblocking domains: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/domains/blocked")
async def get_blocked_domains():
    """Get list of currently blocked domains"""
    try:
        domains = hosts_manager.get_blocked_domains()
        return APIResponse(
            success=True,
            message=f"Found {len(domains)} blocked domains",
            data={"domains": domains}
        )
    except Exception as e:
        logger.error(f"Error getting blocked domains: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_enforcer_stats():
    """Get enforcer statistics"""
    try:
        stats = process_enforcer.get_enforcement_stats()
        return APIResponse(
            success=True,
            message="Enforcer statistics",
            data=stats
        )
    except Exception as e:
        logger.error(f"Error getting enforcer stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
