"""
AI Categorization Engine
Intelligently classifies URLs and applications as productive or distracting
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urlparse
from datetime import datetime

logger = logging.getLogger(__name__)

class AICategorizer:
    """AI-powered categorization engine for URLs and applications"""
    
    def __init__(self, data_dir: str = "./data"):
        """
        Initialize AICategorizer
        
        Args:
            data_dir: Directory to store categorization data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.categories_file = self.data_dir / "categories.json"
        self.ml_model_file = self.data_dir / "ml_model.json"
        
        # Load or initialize categories
        self.categories = self._load_categories()
        self.ml_model = self._load_ml_model()
        
        logger.info("AICategorizer initialized")
    
    def _load_categories(self) -> Dict:
        """Load categorization database"""
        try:
            if self.categories_file.exists():
                with open(self.categories_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading categories: {e}")
        
        # Default categories if file doesn't exist
        return self._get_default_categories()
    
    def _get_default_categories(self) -> Dict:
        """Get default category database"""
        return {
            "productive_domains": {
                "github.com": {"category": "productive", "score": 0.95, "reason": "code_repository"},
                "stackoverflow.com": {"category": "productive", "score": 0.90, "reason": "programming_help"},
                "documentation.com": {"category": "productive", "score": 0.92, "reason": "technical_docs"},
                "python.org": {"category": "productive", "score": 0.93, "reason": "programming_language"},
                "nodejs.org": {"category": "productive", "score": 0.93, "reason": "programming_language"},
                "developer.mozilla.org": {"category": "productive", "score": 0.91, "reason": "web_development"},
                "leetcode.com": {"category": "productive", "score": 0.88, "reason": "coding_practice"},
                "udemy.com": {"category": "productive", "score": 0.85, "reason": "learning_platform"},
                "coursera.org": {"category": "productive", "score": 0.85, "reason": "learning_platform"},
                "medium.com": {"category": "productive", "score": 0.75, "reason": "technical_articles"},
                "arxiv.org": {"category": "productive", "score": 0.92, "reason": "research_papers"},
                "google.com": {"category": "productive", "score": 0.60, "reason": "search_engine"},
                "notion.so": {"category": "productive", "score": 0.88, "reason": "productivity_tool"},
                "trello.com": {"category": "productive", "score": 0.87, "reason": "project_management"},
                "asana.com": {"category": "productive", "score": 0.87, "reason": "project_management"},
                "slack.com": {"category": "productive", "score": 0.80, "reason": "communication_tool"},
                "gmail.com": {"category": "productive", "score": 0.70, "reason": "email_service"},
                "office365.com": {"category": "productive", "score": 0.85, "reason": "productivity_suite"},
                "figma.com": {"category": "productive", "score": 0.90, "reason": "design_tool"},
                "aws.amazon.com": {"category": "productive", "score": 0.92, "reason": "cloud_platform"},
                "cloud.google.com": {"category": "productive", "score": 0.92, "reason": "cloud_platform"},
                "azure.microsoft.com": {"category": "productive", "score": 0.92, "reason": "cloud_platform"},
            },
            "distracting_domains": {
                "twitter.com": {"category": "distracting", "score": 0.98, "reason": "social_media"},
                "facebook.com": {"category": "distracting", "score": 0.98, "reason": "social_media"},
                "instagram.com": {"category": "distracting", "score": 0.98, "reason": "social_media"},
                "tiktok.com": {"category": "distracting", "score": 0.99, "reason": "social_media"},
                "reddit.com": {"category": "distracting", "score": 0.85, "reason": "social_media"},
                "youtube.com": {"category": "distracting", "score": 0.90, "reason": "video_streaming"},
                "twitch.tv": {"category": "distracting", "score": 0.95, "reason": "live_streaming"},
                "netflix.com": {"category": "distracting", "score": 0.98, "reason": "entertainment"},
                "hulu.com": {"category": "distracting", "score": 0.98, "reason": "entertainment"},
                "discord.com": {"category": "distracting", "score": 0.75, "reason": "communication_app"},
                "telegram.org": {"category": "distracting", "score": 0.70, "reason": "messaging_app"},
                "whatsapp.com": {"category": "distracting", "score": 0.65, "reason": "messaging_app"},
                "pinterest.com": {"category": "distracting", "score": 0.92, "reason": "social_media"},
                "snapchat.com": {"category": "distracting", "score": 0.96, "reason": "social_media"},
                "9gag.com": {"category": "distracting", "score": 0.95, "reason": "entertainment"},
                "imgur.com": {"category": "distracting", "score": 0.80, "reason": "image_sharing"},
                "tumblr.com": {"category": "distracting", "score": 0.85, "reason": "social_media"},
                "quora.com": {"category": "distracting", "score": 0.70, "reason": "q_and_a"},
                "buzzfeed.com": {"category": "distracting", "score": 0.95, "reason": "entertainment"},
                "cnn.com": {"category": "distracting", "score": 0.75, "reason": "news"},
                "bbc.com": {"category": "distracting", "score": 0.75, "reason": "news"},
            },
            "productive_apps": {
                "Visual Studio Code": {"category": "productive", "score": 0.98, "reason": "code_editor"},
                "PyCharm": {"category": "productive", "score": 0.97, "reason": "ide"},
                "IntelliJ IDEA": {"category": "productive", "score": 0.97, "reason": "ide"},
                "Sublime Text": {"category": "productive", "score": 0.96, "reason": "code_editor"},
                "Vim": {"category": "productive", "score": 0.95, "reason": "text_editor"},
                "Emacs": {"category": "productive", "score": 0.95, "reason": "text_editor"},
                "Git": {"category": "productive", "score": 0.98, "reason": "version_control"},
                "Docker": {"category": "productive", "score": 0.96, "reason": "containerization"},
                "Terminal": {"category": "productive", "score": 0.95, "reason": "command_line"},
                "Notion": {"category": "productive", "score": 0.88, "reason": "note_taking"},
                "Obsidian": {"category": "productive", "score": 0.90, "reason": "note_taking"},
                "Figma": {"category": "productive", "score": 0.92, "reason": "design_tool"},
                "Photoshop": {"category": "productive", "score": 0.90, "reason": "image_editor"},
                "Blender": {"category": "productive", "score": 0.92, "reason": "3d_modeling"},
                "Slack": {"category": "productive", "score": 0.75, "reason": "communication"},
                "Zoom": {"category": "productive", "score": 0.80, "reason": "video_conferencing"},
                "Excel": {"category": "productive", "score": 0.85, "reason": "spreadsheet"},
                "Word": {"category": "productive", "score": 0.85, "reason": "word_processor"},
                "PowerPoint": {"category": "productive", "score": 0.85, "reason": "presentation"},
            },
            "distracting_apps": {
                "Discord": {"category": "distracting", "score": 0.80, "reason": "communication"},
                "Steam": {"category": "distracting", "score": 0.95, "reason": "gaming"},
                "Spotify": {"category": "distracting", "score": 0.70, "reason": "music_streaming"},
                "Netflix": {"category": "distracting", "score": 0.98, "reason": "video_streaming"},
                "YouTube": {"category": "distracting", "score": 0.92, "reason": "video_streaming"},
                "TikTok": {"category": "distracting", "score": 0.99, "reason": "social_media"},
                "Instagram": {"category": "distracting", "score": 0.98, "reason": "social_media"},
                "Twitter": {"category": "distracting", "score": 0.95, "reason": "social_media"},
                "Facebook": {"category": "distracting", "score": 0.98, "reason": "social_media"},
                "Telegram": {"category": "distracting", "score": 0.75, "reason": "messaging"},
                "WhatsApp": {"category": "distracting", "score": 0.70, "reason": "messaging"},
                "Twitch": {"category": "distracting", "score": 0.96, "reason": "live_streaming"},
                "Reddit": {"category": "distracting", "score": 0.85, "reason": "social_media"},
                "Roblox": {"category": "distracting", "score": 0.98, "reason": "gaming"},
                "Fortnite": {"category": "distracting", "score": 0.99, "reason": "gaming"},
                "Valorant": {"category": "distracting", "score": 0.98, "reason": "gaming"},
                "League of Legends": {"category": "distracting", "score": 0.98, "reason": "gaming"},
                "World of Warcraft": {"category": "distracting", "score": 0.99, "reason": "gaming"},
            }
        }
    
    def _load_ml_model(self) -> Dict:
        """Load machine learning model data"""
        try:
            if self.ml_model_file.exists():
                with open(self.ml_model_file, "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading ML model: {e}")
        
        return {
            "keyword_weights": self._get_default_keyword_weights(),
            "domain_features": {},
            "app_features": {},
            "user_feedback": []
        }
    
    def _get_default_keyword_weights(self) -> Dict:
        """Get default keyword weights for classification"""
        return {
            # Productive keywords
            "code": 0.95,
            "programming": 0.95,
            "development": 0.90,
            "documentation": 0.92,
            "tutorial": 0.85,
            "learning": 0.88,
            "education": 0.90,
            "research": 0.92,
            "academic": 0.90,
            "technical": 0.85,
            "framework": 0.90,
            "library": 0.90,
            "api": 0.88,
            "database": 0.90,
            "server": 0.88,
            "deployment": 0.88,
            "productivity": 0.90,
            "project": 0.75,
            "management": 0.70,
            "collaboration": 0.75,
            
            # Distracting keywords
            "social": 0.95,
            "media": 0.90,
            "entertainment": 0.98,
            "gaming": 0.99,
            "streaming": 0.95,
            "video": 0.85,
            "music": 0.70,
            "news": 0.75,
            "shopping": 0.90,
            "dating": 0.98,
            "meme": 0.95,
            "game": 0.98,
            "chat": 0.65,
            "messaging": 0.65,
            "forum": 0.70,
            "discussion": 0.65,
        }
    
    def _save_categories(self) -> None:
        """Save categories to file"""
        try:
            with open(self.categories_file, "w") as f:
                json.dump(self.categories, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving categories: {e}")
    
    def _save_ml_model(self) -> None:
        """Save ML model to file"""
        try:
            with open(self.ml_model_file, "w") as f:
                json.dump(self.ml_model, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving ML model: {e}")
    
    def categorize_url(self, url: str) -> Dict:
        """
        Categorize a URL as productive or distracting
        
        Args:
            url: URL to categorize
            
        Returns:
            Dictionary with category, confidence score, and reasoning
        """
        try:
            # Parse URL
            parsed = urlparse(url)
            domain = parsed.netloc.replace("www.", "")
            
            # Check exact match in database
            if domain in self.categories["productive_domains"]:
                entry = self.categories["productive_domains"][domain]
                return {
                    "url": url,
                    "domain": domain,
                    "category": "productive",
                    "confidence": entry["score"],
                    "reason": entry["reason"],
                    "source": "exact_match"
                }
            
            if domain in self.categories["distracting_domains"]:
                entry = self.categories["distracting_domains"][domain]
                return {
                    "url": url,
                    "domain": domain,
                    "category": "distracting",
                    "confidence": entry["score"],
                    "reason": entry["reason"],
                    "source": "exact_match"
                }
            
            # If no exact match, use keyword analysis
            return self._categorize_by_keywords(url, domain)
            
        except Exception as e:
            logger.error(f"Error categorizing URL {url}: {e}")
            return {
                "url": url,
                "category": "unknown",
                "confidence": 0.0,
                "reason": "categorization_error",
                "error": str(e)
            }
    
    def categorize_app(self, app_name: str) -> Dict:
        """
        Categorize an application as productive or distracting
        
        Args:
            app_name: Application name or executable
            
        Returns:
            Dictionary with category, confidence score, and reasoning
        """
        try:
            # Normalize app name
            normalized_name = app_name.replace(".exe", "").replace(".app", "").strip()
            
            # Check exact match in database
            for app, entry in self.categories["productive_apps"].items():
                if normalized_name.lower() == app.lower():
                    return {
                        "app": app_name,
                        "category": "productive",
                        "confidence": entry["score"],
                        "reason": entry["reason"],
                        "source": "exact_match"
                    }
            
            for app, entry in self.categories["distracting_apps"].items():
                if normalized_name.lower() == app.lower():
                    return {
                        "app": app_name,
                        "category": "distracting",
                        "confidence": entry["score"],
                        "reason": entry["reason"],
                        "source": "exact_match"
                    }
            
            # If no exact match, use keyword analysis
            return self._categorize_app_by_keywords(app_name, normalized_name)
            
        except Exception as e:
            logger.error(f"Error categorizing app {app_name}: {e}")
            return {
                "app": app_name,
                "category": "unknown",
                "confidence": 0.0,
                "reason": "categorization_error",
                "error": str(e)
            }
    
    def _categorize_by_keywords(self, url: str, domain: str) -> Dict:
        """Categorize URL by keyword analysis"""
        keywords = self.ml_model["keyword_weights"]
        
        productive_score = 0.0
        distracting_score = 0.0
        matched_keywords = []
        
        # Analyze URL and domain for keywords
        text_to_analyze = f"{url} {domain}".lower()
        
        for keyword, weight in keywords.items():
            if keyword in text_to_analyze:
                matched_keywords.append(keyword)
                
                # Determine if keyword is productive or distracting
                if keyword in ["code", "programming", "development", "documentation", "tutorial", 
                              "learning", "education", "research", "academic", "technical"]:
                    productive_score += weight
                else:
                    distracting_score += weight
        
        # Determine category based on scores
        if productive_score > distracting_score and productive_score > 0.5:
            category = "productive"
            confidence = min(productive_score / (productive_score + distracting_score + 0.1), 0.95)
        elif distracting_score > productive_score and distracting_score > 0.5:
            category = "distracting"
            confidence = min(distracting_score / (productive_score + distracting_score + 0.1), 0.95)
        else:
            category = "neutral"
            confidence = 0.5
        
        return {
            "url": url,
            "domain": domain,
            "category": category,
            "confidence": confidence,
            "matched_keywords": matched_keywords,
            "source": "keyword_analysis"
        }
    
    def _categorize_app_by_keywords(self, app_name: str, normalized_name: str) -> Dict:
        """Categorize app by keyword analysis"""
        keywords = self.ml_model["keyword_weights"]
        
        productive_score = 0.0
        distracting_score = 0.0
        matched_keywords = []
        
        # Analyze app name for keywords
        text_to_analyze = f"{app_name} {normalized_name}".lower()
        
        for keyword, weight in keywords.items():
            if keyword in text_to_analyze:
                matched_keywords.append(keyword)
                
                if keyword in ["code", "programming", "development", "editor", "ide"]:
                    productive_score += weight
                else:
                    distracting_score += weight
        
        # Determine category based on scores
        if productive_score > distracting_score and productive_score > 0.5:
            category = "productive"
            confidence = min(productive_score / (productive_score + distracting_score + 0.1), 0.95)
        elif distracting_score > productive_score and distracting_score > 0.5:
            category = "distracting"
            confidence = min(distracting_score / (productive_score + distracting_score + 0.1), 0.95)
        else:
            category = "neutral"
            confidence = 0.5
        
        return {
            "app": app_name,
            "category": category,
            "confidence": confidence,
            "matched_keywords": matched_keywords,
            "source": "keyword_analysis"
        }
    
    def add_user_feedback(self, item: str, item_type: str, actual_category: str, 
                         predicted_category: str, confidence: float) -> None:
        """
        Record user feedback for continuous learning
        
        Args:
            item: URL or app name
            item_type: "url" or "app"
            actual_category: Actual category (productive/distracting)
            predicted_category: Predicted category
            confidence: Prediction confidence
        """
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "item": item,
            "type": item_type,
            "actual": actual_category,
            "predicted": predicted_category,
            "confidence": confidence,
            "was_correct": actual_category == predicted_category
        }
        
        self.ml_model["user_feedback"].append(feedback)
        self._save_ml_model()
        
        logger.info(f"Recorded user feedback for {item}: {actual_category}")
    
    def get_categorization_stats(self) -> Dict:
        """Get statistics about categorization"""
        total_urls = len(self.categories["productive_domains"]) + len(self.categories["distracting_domains"])
        total_apps = len(self.categories["productive_apps"]) + len(self.categories["distracting_apps"])
        total_feedback = len(self.ml_model["user_feedback"])
        
        correct_predictions = sum(1 for f in self.ml_model["user_feedback"] if f["was_correct"])
        accuracy = correct_predictions / total_feedback if total_feedback > 0 else 0
        
        return {
            "total_categorized_urls": total_urls,
            "productive_urls": len(self.categories["productive_domains"]),
            "distracting_urls": len(self.categories["distracting_domains"]),
            "total_categorized_apps": total_apps,
            "productive_apps": len(self.categories["productive_apps"]),
            "distracting_apps": len(self.categories["distracting_apps"]),
            "total_user_feedback": total_feedback,
            "model_accuracy": accuracy,
            "timestamp": datetime.now().isoformat()
        }


# Global instance
ai_categorizer = AICategorizer()
