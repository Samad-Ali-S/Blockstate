"""
Categorization Routes
API endpoints for AI-powered URL and app categorization
"""

from fastapi import APIRouter, HTTPException
from typing import List
import logging

from models import APIResponse
from services.ai_categorizer import ai_categorizer

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/url")
async def categorize_url(url: str):
    """
    Categorize a URL as productive or distracting
    
    Args:
        url: URL to categorize
        
    Returns:
        APIResponse with categorization result
    """
    try:
        result = ai_categorizer.categorize_url(url)
        
        return APIResponse(
            success=True,
            message="URL categorized successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Error categorizing URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/app")
async def categorize_app(app_name: str):
    """
    Categorize an application as productive or distracting
    
    Args:
        app_name: Application name or executable
        
    Returns:
        APIResponse with categorization result
    """
    try:
        result = ai_categorizer.categorize_app(app_name)
        
        return APIResponse(
            success=True,
            message="App categorized successfully",
            data=result
        )
    except Exception as e:
        logger.error(f"Error categorizing app: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/urls/batch")
async def categorize_urls_batch(urls: List[str]):
    """
    Categorize multiple URLs at once
    
    Args:
        urls: List of URLs to categorize
        
    Returns:
        APIResponse with categorization results
    """
    try:
        results = []
        for url in urls:
            result = ai_categorizer.categorize_url(url)
            results.append(result)
        
        return APIResponse(
            success=True,
            message=f"Categorized {len(results)} URLs",
            data={"results": results}
        )
    except Exception as e:
        logger.error(f"Error categorizing URLs batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/apps/batch")
async def categorize_apps_batch(apps: List[str]):
    """
    Categorize multiple applications at once
    
    Args:
        apps: List of app names to categorize
        
    Returns:
        APIResponse with categorization results
    """
    try:
        results = []
        for app in apps:
            result = ai_categorizer.categorize_app(app)
            results.append(result)
        
        return APIResponse(
            success=True,
            message=f"Categorized {len(results)} apps",
            data={"results": results}
        )
    except Exception as e:
        logger.error(f"Error categorizing apps batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def submit_feedback(item: str, item_type: str, actual_category: str, 
                         predicted_category: str, confidence: float):
    """
    Submit user feedback for continuous learning
    
    Args:
        item: URL or app name
        item_type: "url" or "app"
        actual_category: Actual category (productive/distracting)
        predicted_category: Predicted category
        confidence: Prediction confidence
        
    Returns:
        APIResponse with feedback confirmation
    """
    try:
        if item_type not in ["url", "app"]:
            raise HTTPException(status_code=400, detail="item_type must be 'url' or 'app'")
        
        if actual_category not in ["productive", "distracting", "neutral"]:
            raise HTTPException(status_code=400, detail="actual_category must be productive, distracting, or neutral")
        
        ai_categorizer.add_user_feedback(item, item_type, actual_category, predicted_category, confidence)
        
        return APIResponse(
            success=True,
            message="Feedback recorded successfully",
            data={
                "item": item,
                "type": item_type,
                "actual_category": actual_category
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_categorization_stats():
    """Get categorization engine statistics"""
    try:
        stats = ai_categorizer.get_categorization_stats()
        
        return APIResponse(
            success=True,
            message="Categorization statistics retrieved",
            data=stats
        )
    except Exception as e:
        logger.error(f"Error getting categorization stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/categories")
async def get_all_categories():
    """Get all known categories"""
    try:
        categories = {
            "productive_domains": list(ai_categorizer.categories["productive_domains"].keys()),
            "distracting_domains": list(ai_categorizer.categories["distracting_domains"].keys()),
            "productive_apps": list(ai_categorizer.categories["productive_apps"].keys()),
            "distracting_apps": list(ai_categorizer.categories["distracting_apps"].keys()),
        }
        
        return APIResponse(
            success=True,
            message="Categories retrieved",
            data=categories
        )
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/categories/add-url")
async def add_url_category(url: str, domain: str, category: str, score: float, reason: str):
    """
    Add a new URL to the categorization database
    
    Args:
        url: URL to add
        domain: Domain name
        category: Category (productive/distracting)
        score: Confidence score (0-1)
        reason: Reason for categorization
        
    Returns:
        APIResponse with confirmation
    """
    try:
        if category not in ["productive", "distracting"]:
            raise HTTPException(status_code=400, detail="category must be productive or distracting")
        
        if not (0 <= score <= 1):
            raise HTTPException(status_code=400, detail="score must be between 0 and 1")
        
        category_dict = "productive_domains" if category == "productive" else "distracting_domains"
        
        ai_categorizer.categories[category_dict][domain] = {
            "category": category,
            "score": score,
            "reason": reason
        }
        
        ai_categorizer._save_categories()
        
        return APIResponse(
            success=True,
            message=f"Added {domain} to {category} categories",
            data={
                "domain": domain,
                "category": category,
                "score": score
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding URL category: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/categories/add-app")
async def add_app_category(app_name: str, category: str, score: float, reason: str):
    """
    Add a new app to the categorization database
    
    Args:
        app_name: Application name
        category: Category (productive/distracting)
        score: Confidence score (0-1)
        reason: Reason for categorization
        
    Returns:
        APIResponse with confirmation
    """
    try:
        if category not in ["productive", "distracting"]:
            raise HTTPException(status_code=400, detail="category must be productive or distracting")
        
        if not (0 <= score <= 1):
            raise HTTPException(status_code=400, detail="score must be between 0 and 1")
        
        category_dict = "productive_apps" if category == "productive" else "distracting_apps"
        
        ai_categorizer.categories[category_dict][app_name] = {
            "category": category,
            "score": score,
            "reason": reason
        }
        
        ai_categorizer._save_categories()
        
        return APIResponse(
            success=True,
            message=f"Added {app_name} to {category} categories",
            data={
                "app": app_name,
                "category": category,
                "score": score
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding app category: {e}")
        raise HTTPException(status_code=500, detail=str(e))
