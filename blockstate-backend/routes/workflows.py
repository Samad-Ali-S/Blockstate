"""
Workflows Routes
API endpoints for managing focus workflows
"""

from fastapi import APIRouter, HTTPException
import logging
import json
from pathlib import Path
import uuid
from datetime import datetime

from models import WorkflowCreate, WorkflowUpdate, APIResponse
from services.process_enforcer import process_enforcer

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory workflow storage (can be replaced with database)
workflows_file = Path("./data/workflows.json")
workflows_file.parent.mkdir(exist_ok=True)

def load_workflows():
    """Load workflows from file"""
    try:
        if workflows_file.exists():
            with open(workflows_file, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading workflows: {e}")
    return []

def save_workflows(workflows):
    """Save workflows to file"""
    try:
        with open(workflows_file, "w") as f:
            json.dump(workflows, f, indent=2, default=str)
        return True
    except Exception as e:
        logger.error(f"Error saving workflows: {e}")
        return False

@router.post("/")
async def create_workflow(workflow: WorkflowCreate):
    """
    Create a new workflow
    
    Args:
        workflow: WorkflowCreate model
        
    Returns:
        APIResponse with created workflow
    """
    try:
        workflows = load_workflows()
        
        new_workflow = {
            "id": str(uuid.uuid4()),
            "name": workflow.name,
            "description": workflow.description,
            "allowed_apps": workflow.allowed_apps,
            "allowed_sites": workflow.allowed_sites,
            "blocked_processes": workflow.blocked_processes,
            "blocked_domains": workflow.blocked_domains,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        workflows.append(new_workflow)
        save_workflows(workflows)
        
        logger.info(f"Created workflow {new_workflow['id']}")
        
        return APIResponse(
            success=True,
            message="Workflow created successfully",
            data=new_workflow
        )
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_workflows():
    """Get all workflows"""
    try:
        workflows = load_workflows()
        return APIResponse(
            success=True,
            message=f"Retrieved {len(workflows)} workflows",
            data={"workflows": workflows}
        )
    except Exception as e:
        logger.error(f"Error getting workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    """
    Get a specific workflow
    
    Args:
        workflow_id: ID of the workflow
        
    Returns:
        APIResponse with workflow data
    """
    try:
        workflows = load_workflows()
        
        for workflow in workflows:
            if workflow["id"] == workflow_id:
                return APIResponse(
                    success=True,
                    message="Workflow retrieved",
                    data=workflow
                )
        
        raise HTTPException(status_code=404, detail="Workflow not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{workflow_id}")
async def update_workflow(workflow_id: str, updates: WorkflowUpdate):
    """
    Update a workflow
    
    Args:
        workflow_id: ID of the workflow
        updates: WorkflowUpdate model
        
    Returns:
        APIResponse with updated workflow
    """
    try:
        workflows = load_workflows()
        
        for workflow in workflows:
            if workflow["id"] == workflow_id:
                # Update only provided fields
                update_data = updates.dict(exclude_unset=True)
                workflow.update(update_data)
                workflow["updated_at"] = datetime.now().isoformat()
                
                save_workflows(workflows)
                logger.info(f"Updated workflow {workflow_id}")
                
                return APIResponse(
                    success=True,
                    message="Workflow updated successfully",
                    data=workflow
                )
        
        raise HTTPException(status_code=404, detail="Workflow not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """
    Delete a workflow
    
    Args:
        workflow_id: ID of the workflow
        
    Returns:
        APIResponse with deletion confirmation
    """
    try:
        workflows = load_workflows()
        
        for i, workflow in enumerate(workflows):
            if workflow["id"] == workflow_id:
                deleted = workflows.pop(i)
                save_workflows(workflows)
                logger.info(f"Deleted workflow {workflow_id}")
                
                return APIResponse(
                    success=True,
                    message="Workflow deleted successfully",
                    data={"deleted_workflow_id": workflow_id}
                )
        
        raise HTTPException(status_code=404, detail="Workflow not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{workflow_id}/apply")
async def apply_workflow(workflow_id: str):
    """
    Apply a workflow (set blocked processes and domains)
    
    Args:
        workflow_id: ID of the workflow to apply
        
    Returns:
        APIResponse with application result
    """
    try:
        workflows = load_workflows()
        
        workflow = None
        for w in workflows:
            if w["id"] == workflow_id:
                workflow = w
                break
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        # Set blocked processes in the enforcer
        process_enforcer.set_blocked_processes(workflow["blocked_processes"])
        
        logger.info(f"Applied workflow {workflow_id}")
        
        return APIResponse(
            success=True,
            message="Workflow applied successfully",
            data={
                "workflow_id": workflow_id,
                "blocked_processes": len(workflow["blocked_processes"]),
                "blocked_domains": len(workflow["blocked_domains"])
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error applying workflow {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{workflow_id}/stats")
async def get_workflow_stats(workflow_id: str):
    """
    Get statistics for a workflow
    
    Args:
        workflow_id: ID of the workflow
        
    Returns:
        APIResponse with workflow statistics
    """
    try:
        workflows = load_workflows()
        
        workflow = None
        for w in workflows:
            if w["id"] == workflow_id:
                workflow = w
                break
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return APIResponse(
            success=True,
            message="Workflow statistics retrieved",
            data={
                "workflow_id": workflow_id,
                "name": workflow["name"],
                "allowed_apps_count": len(workflow["allowed_apps"]),
                "allowed_sites_count": len(workflow["allowed_sites"]),
                "blocked_processes_count": len(workflow["blocked_processes"]),
                "blocked_domains_count": len(workflow["blocked_domains"])
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting workflow stats {workflow_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
