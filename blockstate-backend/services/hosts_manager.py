"""
Hosts File Manager
Handles reading, writing, and managing the system hosts file for domain blocking
"""

import os
import logging
from typing import List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class HostsManager:
    """Manages the system hosts file for domain blocking"""
    
    # Platform-specific hosts file paths
    HOSTS_FILE_PATHS = {
        "linux": "/etc/hosts",
        "darwin": "/etc/hosts",  # macOS
        "win32": "C:\\Windows\\System32\\drivers\\etc\\hosts",
    }
    
    BLOCKSTATE_MARKER = "# BlockState Managed Entries"
    
    def __init__(self):
        """Initialize HostsManager"""
        self.hosts_path = self._get_hosts_path()
        logger.info(f"HostsManager initialized with hosts file: {self.hosts_path}")
    
    def _get_hosts_path(self) -> str:
        """Get the system hosts file path based on OS"""
        import sys
        
        if sys.platform.startswith("win"):
            return self.HOSTS_FILE_PATHS["win32"]
        elif sys.platform == "darwin":
            return self.HOSTS_FILE_PATHS["darwin"]
        else:
            return self.HOSTS_FILE_PATHS["linux"]
    
    def _read_hosts_file(self) -> str:
        """Read the current hosts file"""
        try:
            with open(self.hosts_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            logger.warning(f"Hosts file not found at {self.hosts_path}")
            return ""
        except PermissionError:
            logger.error(f"Permission denied reading hosts file at {self.hosts_path}")
            raise PermissionError("Cannot read hosts file - administrator privileges required")
    
    def _write_hosts_file(self, content: str) -> bool:
        """Write to the hosts file"""
        try:
            with open(self.hosts_path, "w") as f:
                f.write(content)
            logger.info("Hosts file updated successfully")
            return True
        except PermissionError:
            logger.error(f"Permission denied writing to hosts file at {self.hosts_path}")
            raise PermissionError("Cannot write to hosts file - administrator privileges required")
        except Exception as e:
            logger.error(f"Error writing hosts file: {e}")
            raise
    
    def add_blocked_domains(self, domains: List[str]) -> Tuple[bool, str]:
        """
        Add domains to the hosts file to block them
        
        Args:
            domains: List of domain names to block
            
        Returns:
            Tuple of (success, message)
        """
        try:
            content = self._read_hosts_file()
            
            # Check if BlockState section exists
            if self.BLOCKSTATE_MARKER not in content:
                content += f"\n\n{self.BLOCKSTATE_MARKER}\n"
            
            # Add each domain
            new_entries = []
            for domain in domains:
                if domain not in content:
                    new_entries.append(f"127.0.0.1 {domain}")
            
            if new_entries:
                content += "\n".join(new_entries) + "\n"
                self._write_hosts_file(content)
                logger.info(f"Added {len(new_entries)} domains to hosts file")
                return True, f"Successfully blocked {len(new_entries)} domains"
            else:
                logger.info("All domains already blocked")
                return True, "All domains already blocked"
                
        except Exception as e:
            logger.error(f"Error adding blocked domains: {e}")
            return False, f"Error blocking domains: {str(e)}"
    
    def remove_blocked_domains(self, domains: List[str]) -> Tuple[bool, str]:
        """
        Remove domains from the hosts file to unblock them
        
        Args:
            domains: List of domain names to unblock
            
        Returns:
            Tuple of (success, message)
        """
        try:
            content = self._read_hosts_file()
            original_lines = content.split("\n")
            
            # Filter out the blocked domains
            new_lines = []
            removed_count = 0
            
            for line in original_lines:
                should_remove = False
                for domain in domains:
                    if f"127.0.0.1 {domain}" in line:
                        should_remove = True
                        removed_count += 1
                        break
                
                if not should_remove:
                    new_lines.append(line)
            
            new_content = "\n".join(new_lines)
            
            # Remove empty BlockState section if no entries left
            if self.BLOCKSTATE_MARKER in new_content:
                blockstate_section = new_content.split(self.BLOCKSTATE_MARKER)[1].strip()
                if not blockstate_section:
                    new_content = new_content.split(self.BLOCKSTATE_MARKER)[0].rstrip()
            
            self._write_hosts_file(new_content)
            logger.info(f"Removed {removed_count} domains from hosts file")
            return True, f"Successfully unblocked {removed_count} domains"
            
        except Exception as e:
            logger.error(f"Error removing blocked domains: {e}")
            return False, f"Error unblocking domains: {str(e)}"
    
    def get_blocked_domains(self) -> List[str]:
        """
        Get list of currently blocked domains
        
        Returns:
            List of blocked domain names
        """
        try:
            content = self._read_hosts_file()
            blocked_domains = []
            
            if self.BLOCKSTATE_MARKER in content:
                blockstate_section = content.split(self.BLOCKSTATE_MARKER)[1]
                for line in blockstate_section.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split()
                        if len(parts) >= 2 and parts[0] == "127.0.0.1":
                            blocked_domains.append(parts[1])
            
            return blocked_domains
        except Exception as e:
            logger.error(f"Error reading blocked domains: {e}")
            return []
    
    def clear_all_blockstate_entries(self) -> Tuple[bool, str]:
        """
        Remove all BlockState entries from the hosts file
        
        Returns:
            Tuple of (success, message)
        """
        try:
            content = self._read_hosts_file()
            
            if self.BLOCKSTATE_MARKER in content:
                # Split and keep only the part before BlockState marker
                content = content.split(self.BLOCKSTATE_MARKER)[0].rstrip()
                self._write_hosts_file(content)
                logger.info("Cleared all BlockState entries from hosts file")
                return True, "All BlockState entries cleared"
            else:
                return True, "No BlockState entries found"
                
        except Exception as e:
            logger.error(f"Error clearing BlockState entries: {e}")
            return False, f"Error clearing entries: {str(e)}"
    
    def is_domain_blocked(self, domain: str) -> bool:
        """
        Check if a specific domain is blocked
        
        Args:
            domain: Domain name to check
            
        Returns:
            True if domain is blocked, False otherwise
        """
        blocked_domains = self.get_blocked_domains()
        return domain in blocked_domains


# Global instance
hosts_manager = HostsManager()
