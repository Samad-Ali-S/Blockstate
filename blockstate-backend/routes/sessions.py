"""
Sessions Routes
API endpoints for managing focus sessions and retrieving session data
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
import logging

from models import APIResponse, PaginatedResponse
from services.session_manager import session_manager

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
async def get_all_sessions(skip: int = 0, limit: int = 50):
    """
    Get all sessions with pagination
    
    Args:
        skip: Number of sessions to skip
        limit: Maximum number of sessions to return
        
    Returns:
        PaginatedResponse with sessions
    """
    try:
        all_sessions = session_manager.get_all_sessions()
        total = len(all_sessions)
        
        # Apply pagination
        paginated = all_sessions[skip:skip + limit]
        
        return PaginatedResponse(
            items=paginated,
            total=total,
            page=skip // limit + 1,
            page_size=limit,
            total_pages=(total + limit - 1) // limit
        )
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}")
async def get_session(session_id: str):
    """
    Get a specific session
    
    Args:
        session_id: ID of the session
        
    Returns:
        APIResponse with session data
    """
    try:
        session = session_manager.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return APIResponse(
            success=True,
            message="Session retrieved",
            data=session
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}/stats")
async def get_session_stats(session_id: str):
    """
    Get statistics for a session
    
    Args:
        session_id: ID of the session
        
    Returns:
        APIResponse with session statistics
    """
    try:
        stats = session_manager.get_session_stats(session_id)
        
        if not stats:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return APIResponse(
            success=True,
            message="Session statistics retrieved",
            data=stats
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session stats {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/workflow/{workflow_id}")
async def get_sessions_by_workflow(workflow_id: str, skip: int = 0, limit: int = 50):
    """
    Get all sessions for a specific workflow
    
    Args:
        workflow_id: ID of the workflow
        skip: Number of sessions to skip
        limit: Maximum number of sessions to return
        
    Returns:
        PaginatedResponse with sessions
    """
    try:
        sessions = session_manager.get_sessions_by_workflow(workflow_id)
        total = len(sessions)
        
        # Apply pagination
        paginated = sessions[skip:skip + limit]
        
        return PaginatedResponse(
            items=paginated,
            total=total,
            page=skip // limit + 1,
            page_size=limit,
            total_pages=(total + limit - 1) // limit
        )
    except Exception as e:
        logger.error(f"Error getting sessions for workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/date/{date_str}")
async def get_sessions_by_date(date_str: str, skip: int = 0, limit: int = 50):
    """
    Get all sessions for a specific date
    
    Args:
        date_str: Date string in format YYYY-MM-DD
        skip: Number of sessions to skip
        limit: Maximum number of sessions to return
        
    Returns:
        PaginatedResponse with sessions
    """
    try:
        sessions = session_manager.get_sessions_by_date(date_str)
        total = len(sessions)
        
        # Apply pagination
        paginated = sessions[skip:skip + limit]
        
        return PaginatedResponse(
            items=paginated,
            total=total,
            page=skip // limit + 1,
            page_size=limit,
            total_pages=(total + limit - 1) // limit
        )
    except Exception as e:
        logger.error(f"Error getting sessions for date {date_str}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/current/active")
async def get_current_session():
    """
    Get the current active session
    
    Returns:
        APIResponse with current session or null
    """
    try:
        session = session_manager.get_current_session()
        
        return APIResponse(
            success=True,
            message="Current session retrieved",
            data={"session": session}
        )
    except Exception as e:
        logger.error(f"Error getting current session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{session_id}/distraction")
async def add_distraction_blocked(session_id: str):
    """
    Increment distraction count for a session
    
    Args:
        session_id: ID of the session
        
    Returns:
        APIResponse with updated session
    """
    try:
        session = session_manager.add_distraction_blocked(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return APIResponse(
            success=True,
            message="Distraction count incremented",
            data={"distractions_blocked": session["distractions_blocked"]}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding distraction for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{session_id}/process-terminated")
async def add_process_terminated(session_id: str, process_name: str):
    """
    Add a terminated process to the session log
    
    Args:
        session_id: ID of the session
        process_name: Name of the terminated process
        
    Returns:
        APIResponse with updated session
    """
    try:
        session = session_manager.add_process_terminated(session_id, process_name)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return APIResponse(
            success=True,
            message="Process added to session log",
            data={"processes_terminated": session["processes_terminated"]}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding process for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{session_id}/app-used")
async def add_app_used(session_id: str, app_name: str):
    """
    Add an app to the apps used list
    
    Args:
        session_id: ID of the session
        app_name: Name of the app
        
    Returns:
        APIResponse with updated session
    """
    try:
        session = session_manager.add_app_used(session_id, app_name)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return APIResponse(
            success=True,
            message="App added to session log",
            data={"apps_used": session["apps_used"]}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding app for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/summary")
async def get_sessions_summary():
    """
    Get summary statistics for all sessions
    
    Returns:
        APIResponse with summary stats
    """
    try:
        sessions = session_manager.get_all_sessions()
        
        total_sessions = len(sessions)
        completed_sessions = len([s for s in sessions if s["status"] == "completed"])
        total_focus_time = sum(s["duration_minutes"] for s in sessions)
        total_distractions = sum(s["distractions_blocked"] for s in sessions)
        
        return APIResponse(
            success=True,
            message="Sessions summary retrieved",
            data={
                "total_sessions": total_sessions,
                "completed_sessions": completed_sessions,
                "total_focus_time_minutes": total_focus_time,
                "total_distractions_blocked": total_distractions,
                "average_distractions_per_session": total_distractions / total_sessions if total_sessions > 0 else 0
            }
        )
    except Exception as e:
        logger.error(f"Error getting sessions summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
