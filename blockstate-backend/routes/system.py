"""
System Routes
API endpoints for system monitoring and information
"""

from fastapi import APIRouter, HTTPException
import logging
import psutil

from models import APIResponse
from services.process_enforcer import process_enforcer

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/info")
async def get_system_info():
    """Get system information"""
    try:
        return APIResponse(
            success=True,
            message="System information retrieved",
            data={
                "platform": psutil.os.name,
                "processor_count": psutil.cpu_count(),
                "total_memory_gb": psutil.virtual_memory().total / (1024**3),
                "total_disk_gb": psutil.disk_usage("/").total / (1024**3)
            }
        )
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_system_stats():
    """Get current system statistics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        
        return APIResponse(
            success=True,
            message="System statistics retrieved",
            data={
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024**3),
                "running_processes": len(psutil.pids())
            }
        )
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/processes")
async def get_processes(limit: int = 50):
    """
    Get top processes by memory usage
    
    Args:
        limit: Maximum number of processes to return
        
    Returns:
        APIResponse with process list
    """
    try:
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'memory_percent'])
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        # Sort by memory usage and limit
        processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:limit]
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(processes)} processes",
            data={"processes": processes}
        )
    except Exception as e:
        logger.error(f"Error getting processes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/process/{pid}")
async def get_process_info(pid: int):
    """
    Get detailed information about a specific process
    
    Args:
        pid: Process ID
        
    Returns:
        APIResponse with process information
    """
    try:
        proc_info = process_enforcer.get_process_info(pid)
        
        if not proc_info:
            raise HTTPException(status_code=404, detail="Process not found")
        
        return APIResponse(
            success=True,
            message="Process information retrieved",
            data=proc_info
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting process info for PID {pid}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process/{pid}/kill")
async def kill_process(pid: int, force: bool = False):
    """
    Terminate a process
    
    Args:
        pid: Process ID to terminate
        force: If True, use SIGKILL instead of SIGTERM
        
    Returns:
        APIResponse with termination result
    """
    try:
        success, message = process_enforcer.terminate_process(pid, force=force)
        
        if success:
            return APIResponse(
                success=True,
                message=message,
                data={"pid": pid, "terminated": True}
            )
        else:
            raise HTTPException(status_code=500, detail=message)
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error terminating process {pid}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/network/connections")
async def get_network_connections(limit: int = 50):
    """
    Get active network connections
    
    Args:
        limit: Maximum number of connections to return
        
    Returns:
        APIResponse with network connections
    """
    try:
        connections = []
        
        for conn in psutil.net_connections()[:limit]:
            connections.append({
                "family": str(conn.family),
                "type": str(conn.type),
                "local_address": f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                "remote_address": f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                "status": conn.status,
                "pid": conn.pid
            })
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(connections)} network connections",
            data={"connections": connections}
        )
    except Exception as e:
        logger.error(f"Error getting network connections: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/disk/usage")
async def get_disk_usage():
    """Get disk usage information"""
    try:
        disk_usage = psutil.disk_usage("/")
        
        return APIResponse(
            success=True,
            message="Disk usage retrieved",
            data={
                "total_gb": disk_usage.total / (1024**3),
                "used_gb": disk_usage.used / (1024**3),
                "free_gb": disk_usage.free / (1024**3),
                "percent_used": disk_usage.percent
            }
        )
    except Exception as e:
        logger.error(f"Error getting disk usage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/memory/usage")
async def get_memory_usage():
    """Get memory usage information"""
    try:
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return APIResponse(
            success=True,
            message="Memory usage retrieved",
            data={
                "total_gb": memory.total / (1024**3),
                "used_gb": memory.used / (1024**3),
                "available_gb": memory.available / (1024**3),
                "percent_used": memory.percent,
                "swap_total_gb": swap.total / (1024**3),
                "swap_used_gb": swap.used / (1024**3),
                "swap_percent": swap.percent
            }
        )
    except Exception as e:
        logger.error(f"Error getting memory usage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cpu/usage")
async def get_cpu_usage():
    """Get CPU usage information"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_freq = psutil.cpu_freq()
        
        return APIResponse(
            success=True,
            message="CPU usage retrieved",
            data={
                "total_cores": psutil.cpu_count(),
                "per_core_usage": cpu_percent,
                "average_usage": sum(cpu_percent) / len(cpu_percent),
                "frequency_mhz": cpu_freq.current if cpu_freq else None
            }
        )
    except Exception as e:
        logger.error(f"Error getting CPU usage: {e}")
        raise HTTPException(status_code=500, detail=str(e))
