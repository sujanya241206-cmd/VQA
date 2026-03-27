import json
from pathlib import Path
from datetime import datetime
import pandas as pd

class StorageManager:
    def __init__(self, history_file="data/history.json"):
        self.history_file = Path(history_file)
        self.history_file.parent.mkdir(exist_ok=True)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create history file if it doesn't exist"""
        if not self.history_file.exists():
            with open(self.history_file, 'w') as f:
                json.dump([], f)
    
    def _load_history(self):
        """Load history from file"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_history(self, history):
        """Save history to file"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=4)
    
    def add_interaction(self, username, image_name, question, answer, confidence, story=None, story_style=None):
        """Add a new interaction to history"""
        history = self._load_history()
        
        interaction = {
            "id": len(history) + 1,
            "username": username,
            "image_name": image_name,
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "story": story,
            "story_style": story_style,
            "timestamp": datetime.now().isoformat()
        }
        
        history.append(interaction)
        self._save_history(history)
        
        return interaction
    
    def get_user_history(self, username):
        """Get history for a specific user"""
        history = self._load_history()
        return [h for h in history if h["username"] == username]
    
    def get_all_history(self):
        """Get all history"""
        return self._load_history()
    
    def get_history_dataframe(self, username=None):
        """Get history as pandas DataFrame"""
        history = self._load_history()
        
        if username:
            history = [h for h in history if h["username"] == username]
        
        if not history:
            return pd.DataFrame()
        
        df = pd.DataFrame(history)
        
        # Convert timestamp to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        return df
    
    def get_statistics(self, username=None):
        """Get usage statistics"""
        df = self.get_history_dataframe(username)
        
        if df.empty:
            return {
                "total_queries": 0,
                "average_confidence": 0,
                "unique_images": 0,
                "most_recent": None
            }
        
        stats = {
            "total_queries": len(df),
            "average_confidence": df['confidence'].mean() if 'confidence' in df.columns else 0,
            "unique_images": df['image_name'].nunique() if 'image_name' in df.columns else 0,
            "most_recent": df['timestamp'].max().strftime("%Y-%m-%d %H:%M") if 'timestamp' in df.columns else None
        }
        
        return stats
    
    def clear_user_history(self, username):
        """Clear history for a specific user"""
        history = self._load_history()
        history = [h for h in history if h["username"] != username]
        self._save_history(history)
        
        return True
    
    def delete_interaction(self, interaction_id):
        """Delete a specific interaction"""
        history = self._load_history()
        history = [h for h in history if h.get("id") != interaction_id]
        self._save_history(history)
        
        return True
