"""
Process Enforcer
Handles process monitoring, termination, and enforcement of blocked applications
"""

import psutil
import logging
from typing import List, Dict, Tuple
from datetime import datetime
import time

logger = logging.getLogger(__name__)

class ProcessEnforcer:
    """Manages system processes for focus enforcement"""
    
    def __init__(self):
        """Initialize ProcessEnforcer"""
        self.blocked_processes = []
        self.monitored_pids = {}
        self.terminated_count = 0
        logger.info("ProcessEnforcer initialized")
    
    def set_blocked_processes(self, process_names: List[str]) -> None:
        """
        Set the list of processes to block
        
        Args:
            process_names: List of process names/executables to block (e.g., ["Discord.exe", "Steam.exe"])
        """
        self.blocked_processes = [name.lower() for name in process_names]
        logger.info(f"Blocked processes updated: {self.blocked_processes}")
    
    def get_running_processes(self) -> List[Dict]:
        """
        Get list of all running processes
        
        Returns:
            List of process information dictionaries
        """
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_info', 'cpu_percent']):
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name', 'status', 'memory_info', 'cpu_percent'])
                    processes.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'status': pinfo['status'],
                        'memory_mb': pinfo['memory_info'].rss / (1024 * 1024),
                        'cpu_percent': pinfo['cpu_percent'] or 0
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            logger.error(f"Error getting running processes: {e}")
        
        return processes
    
    def find_blocked_processes(self) -> List[Dict]:
        """
        Find all currently running processes that are blocked
        
        Returns:
            List of blocked process information
        """
        blocked = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.name().lower()
                    if any(blocked_name.lower() in proc_name for blocked_name in self.blocked_processes):
                        pinfo = proc.as_dict(attrs=['pid', 'name', 'status', 'memory_info', 'cpu_percent'])
                        blocked.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'status': pinfo['status'],
                            'memory_mb': pinfo['memory_info'].rss / (1024 * 1024),
                            'cpu_percent': pinfo['cpu_percent'] or 0
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        except Exception as e:
            logger.error(f"Error finding blocked processes: {e}")
        
        return blocked
    
    def terminate_process(self, pid: int, force: bool = False) -> Tuple[bool, str]:
        """
        Terminate a specific process
        
        Args:
            pid: Process ID to terminate
            force: If True, use SIGKILL instead of SIGTERM
            
        Returns:
            Tuple of (success, message)
        """
        try:
            proc = psutil.Process(pid)
            proc_name = proc.name()
            
            if force:
                proc.kill()
                logger.info(f"Force killed process {proc_name} (PID: {pid})")
                self.terminated_count += 1
                return True, f"Force terminated {proc_name}"
            else:
                proc.terminate()
                # Wait for process to terminate
                try:
                    proc.wait(timeout=3)
                    logger.info(f"Terminated process {proc_name} (PID: {pid})")
                    self.terminated_count += 1
                    return True, f"Terminated {proc_name}"
                except psutil.TimeoutExpired:
                    # If process doesn't terminate, force kill it
                    proc.kill()
                    logger.info(f"Force killed process {proc_name} (PID: {pid}) after timeout")
                    self.terminated_count += 1
                    return True, f"Force terminated {proc_name}"
                    
        except psutil.NoSuchProcess:
            logger.warning(f"Process with PID {pid} not found")
            return False, f"Process not found"
        except psutil.AccessDenied:
            logger.error(f"Access denied terminating process {pid}")
            return False, "Access denied - administrator privileges required"
        except Exception as e:
            logger.error(f"Error terminating process {pid}: {e}")
            return False, f"Error terminating process: {str(e)}"
    
    def terminate_all_blocked_processes(self) -> Tuple[int, List[str]]:
        """
        Terminate all currently running blocked processes
        
        Returns:
            Tuple of (count_terminated, list_of_terminated_names)
        """
        blocked = self.find_blocked_processes()
        terminated = []
        
        for proc_info in blocked:
            success, msg = self.terminate_process(proc_info['pid'])
            if success:
                terminated.append(proc_info['name'])
        
        logger.info(f"Terminated {len(terminated)} blocked processes")
        return len(terminated), terminated
    
    def monitor_and_enforce(self) -> Dict:
        """
        Monitor for blocked processes and enforce termination
        
        Returns:
            Dictionary with enforcement statistics
        """
        stats = {
            'timestamp': datetime.now().isoformat(),
            'blocked_found': 0,
            'blocked_terminated': 0,
            'processes_terminated': []
        }
        
        try:
            blocked = self.find_blocked_processes()
            stats['blocked_found'] = len(blocked)
            
            for proc_info in blocked:
                success, msg = self.terminate_process(proc_info['pid'])
                if success:
                    stats['blocked_terminated'] += 1
                    stats['processes_terminated'].append(proc_info['name'])
            
            logger.info(f"Enforcement check: Found {stats['blocked_found']}, Terminated {stats['blocked_terminated']}")
            
        except Exception as e:
            logger.error(f"Error during enforcement monitoring: {e}")
        
        return stats
    
    def get_process_info(self, pid: int) -> Dict:
        """
        Get detailed information about a specific process
        
        Args:
            pid: Process ID
            
        Returns:
            Dictionary with process information
        """
        try:
            proc = psutil.Process(pid)
            return {
                'pid': proc.pid,
                'name': proc.name(),
                'status': proc.status(),
                'memory_mb': proc.memory_info().rss / (1024 * 1024),
                'cpu_percent': proc.cpu_percent(interval=1),
                'create_time': proc.create_time(),
                'num_threads': proc.num_threads(),
                'exe': proc.exe() if hasattr(proc, 'exe') else None
            }
        except Exception as e:
            logger.error(f"Error getting process info for PID {pid}: {e}")
            return {}
    
    def get_enforcement_stats(self) -> Dict:
        """
        Get enforcement statistics
        
        Returns:
            Dictionary with enforcement stats
        """
        return {
            'blocked_processes_configured': len(self.blocked_processes),
            'total_terminated': self.terminated_count,
            'currently_blocked_running': len(self.find_blocked_processes()),
            'timestamp': datetime.now().isoformat()
        }


# Global instance
process_enforcer = ProcessEnforcer()
