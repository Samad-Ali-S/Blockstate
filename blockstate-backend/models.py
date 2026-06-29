"""
Database models for BlockState
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

# ============================================================================
# WORKFLOW MODELS
# ============================================================================

class WorkflowCreate(BaseModel):
    """Model for creating a new workflow"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    allowed_apps: List[str] = Field(default_factory=list)
    allowed_sites: List[str] = Field(default_factory=list)
    blocked_processes: List[str] = Field(default_factory=list)
    blocked_domains: List[str] = Field(default_factory=list)

class WorkflowUpdate(BaseModel):
    """Model for updating a workflow"""
    name: Optional[str] = None
    description: Optional[str] = None
    allowed_apps: Optional[List[str]] = None
    allowed_sites: Optional[List[str]] = None
    blocked_processes: Optional[List[str]] = None
    blocked_domains: Optional[List[str]] = None

class Workflow(WorkflowCreate):
    """Complete workflow model"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ============================================================================
# SESSION MODELS
# ============================================================================

class SessionStatus(str, Enum):
    """Session status enumeration"""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"

class SessionCreate(BaseModel):
    """Model for creating a new session"""
    workflow_id: str
    duration_minutes: int = Field(..., gt=0, le=480)
    target_focus_time: int = Field(default=25)

class SessionUpdate(BaseModel):
    """Model for updating a session"""
    status: Optional[SessionStatus] = None
    distractions_blocked: Optional[int] = None
    apps_used: Optional[List[str]] = None

class Session(SessionCreate):
    """Complete session model"""
    id: str
    status: SessionStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    elapsed_time: int = 0
    distractions_blocked: int = 0
    apps_used: List[str] = Field(default_factory=list)
    processes_terminated: List[str] = Field(default_factory=list)
    
    class Config:
        from_attributes = True

# ============================================================================
# ENFORCER MODELS
# ============================================================================

class EnforcerStatus(BaseModel):
    """Current enforcer status"""
    is_active: bool
    current_session_id: Optional[str] = None
    workflow_id: Optional[str] = None
    blocked_processes: List[str] = Field(default_factory=list)
    blocked_domains: List[str] = Field(default_factory=list)
    processes_monitored: int = 0
    uptime_seconds: int = 0

class EnforcerStartRequest(BaseModel):
    """Request to start the enforcer"""
    workflow_id: str
    duration_minutes: int = Field(..., gt=0, le=480)
    strict_mode: bool = False

class EnforcerStopRequest(BaseModel):
    """Request to stop the enforcer"""
    session_id: str
    reason: Optional[str] = None

class EnforcerAction(BaseModel):
    """Log of enforcer action"""
    timestamp: datetime
    action_type: str  # "block", "terminate", "warn"
    target: str  # process name or domain
    details: Optional[str] = None

# ============================================================================
# SYSTEM MODELS
# ============================================================================

class ProcessInfo(BaseModel):
    """Information about a running process"""
    pid: int
    name: str
    status: str
    memory_mb: float
    cpu_percent: float

class HostsFileEntry(BaseModel):
    """Entry in the hosts file"""
    ip_address: str = "127.0.0.1"
    domain: str
    is_blocked: bool = True

class SystemStats(BaseModel):
    """System statistics"""
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    running_processes: int
    blocked_processes: int

# ============================================================================
# API RESPONSE MODELS
# ============================================================================

class APIResponse(BaseModel):
    """Standard API response"""
    success: bool
    message: str
    data: Optional[dict] = None
    error: Optional[str] = None

class PaginatedResponse(BaseModel):
    """Paginated response model"""
    items: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int
