"""
Session Manager
Handles creation, tracking, and storage of focus sessions
"""

import json
import logging
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path
import uuid

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages focus sessions and session data"""
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize SessionManager
        
        Args:
            data_dir: Directory to store session data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.sessions_file = self.data_dir / "sessions.json"
        self.current_session = None
        logger.info(f"SessionManager initialized with data directory: {self.data_dir}")
    
    def _load_sessions(self) -> List[Dict]:
        """Load all sessions from file"""
        try:
            if self.sessions_file.exists():
                with open(self.sessions_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading sessions: {e}")
        return []
    
    def _save_sessions(self, sessions: List[Dict]) -> bool:
        """Save sessions to file"""
        try:
            with open(self.sessions_file, "w") as f:
                json.dump(sessions, f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Error saving sessions: {e}")
            return False
    
    def create_session(self, workflow_id: str, duration_minutes: int, 
                      strict_mode: bool = False) -> Dict:
        """
        Create a new focus session
        
        Args:
            workflow_id: ID of the workflow to use
            duration_minutes: Duration of the session in minutes
            strict_mode: If True, session cannot be paused
            
        Returns:
            Dictionary with session data
        """
        session_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        session = {
            'id': session_id,
            'workflow_id': workflow_id,
            'status': 'active',
            'start_time': now,
            'end_time': None,
            'duration_minutes': duration_minutes,
            'elapsed_time': 0,
            'strict_mode': strict_mode,
            'distractions_blocked': 0,
            'processes_terminated': [],
            'apps_used': [],
            'domains_blocked': []
        }
        
        self.current_session = session
        sessions = self._load_sessions()
        sessions.append(session)
        self._save_sessions(sessions)
        
        logger.info(f"Created session {session_id} for workflow {workflow_id}")
        return session
    
    def update_session(self, session_id: str, updates: Dict) -> Optional[Dict]:
        """
        Update an existing session
        
        Args:
            session_id: ID of the session to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated session dictionary or None if not found
        """
        sessions = self._load_sessions()
        
        for session in sessions:
            if session['id'] == session_id:
                session.update(updates)
                session['updated_at'] = datetime.now().isoformat()
                self._save_sessions(sessions)
                logger.info(f"Updated session {session_id}")
                return session
        
        logger.warning(f"Session {session_id} not found")
        return None
    
    def end_session(self, session_id: str) -> Optional[Dict]:
        """
        End a focus session
        
        Args:
            session_id: ID of the session to end
            
        Returns:
            Completed session dictionary or None if not found
        """
        return self.update_session(session_id, {
            'status': 'completed',
            'end_time': datetime.now().isoformat()
        })
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get a specific session
        
        Args:
            session_id: ID of the session
            
        Returns:
            Session dictionary or None if not found
        """
        sessions = self._load_sessions()
        for session in sessions:
            if session['id'] == session_id:
                return session
        return None
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all sessions"""
        return self._load_sessions()
    
    def get_sessions_by_workflow(self, workflow_id: str) -> List[Dict]:
        """Get all sessions for a specific workflow"""
        sessions = self._load_sessions()
        return [s for s in sessions if s['workflow_id'] == workflow_id]
    
    def get_sessions_by_date(self, date_str: str) -> List[Dict]:
        """
        Get all sessions for a specific date
        
        Args:
            date_str: Date string in format YYYY-MM-DD
            
        Returns:
            List of sessions for that date
        """
        sessions = self._load_sessions()
        return [s for s in sessions if s['start_time'].startswith(date_str)]
    
    def add_distraction_blocked(self, session_id: str) -> Optional[Dict]:
        """
        Increment distraction count for a session
        
        Args:
            session_id: ID of the session
            
        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)
        if session:
            session['distractions_blocked'] += 1
            return self.update_session(session_id, {'distractions_blocked': session['distractions_blocked']})
        return None
    
    def add_process_terminated(self, session_id: str, process_name: str) -> Optional[Dict]:
        """
        Add a terminated process to the session log
        
        Args:
            session_id: ID of the session
            process_name: Name of the terminated process
            
        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)
        if session:
            if process_name not in session['processes_terminated']:
                session['processes_terminated'].append(process_name)
                return self.update_session(session_id, {'processes_terminated': session['processes_terminated']})
        return None
    
    def add_app_used(self, session_id: str, app_name: str) -> Optional[Dict]:
        """
        Add an app to the apps used list
        
        Args:
            session_id: ID of the session
            app_name: Name of the app
            
        Returns:
            Updated session or None if not found
        """
        session = self.get_session(session_id)
        if session:
            if app_name not in session['apps_used']:
                session['apps_used'].append(app_name)
                return self.update_session(session_id, {'apps_used': session['apps_used']})
        return None
    
    def get_session_stats(self, session_id: str) -> Optional[Dict]:
        """
        Get statistics for a session
        
        Args:
            session_id: ID of the session
            
        Returns:
            Dictionary with session statistics
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        return {
            'session_id': session_id,
            'workflow_id': session['workflow_id'],
            'status': session['status'],
            'duration_minutes': session['duration_minutes'],
            'elapsed_time': session['elapsed_time'],
            'distractions_blocked': session['distractions_blocked'],
            'processes_terminated': len(session['processes_terminated']),
            'apps_used': len(session['apps_used']),
            'start_time': session['start_time'],
            'end_time': session['end_time']
        }
    
    def get_current_session(self) -> Optional[Dict]:
        """Get the current active session"""
        return self.current_session
    
    def clear_current_session(self) -> None:
        """Clear the current session"""
        self.current_session = None


# Global instance
session_manager = SessionManager()
