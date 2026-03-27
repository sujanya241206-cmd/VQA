import json
import hashlib
from pathlib import Path
from datetime import datetime

class AuthManager:
    def __init__(self, users_file="data/users.json"):
        self.users_file = Path(users_file)
        self.users_file.parent.mkdir(exist_ok=True)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create users file if it doesn't exist"""
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self):
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_users(self, users):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=4)
    
    def register_user(self, username, password, email=""):
        """Register a new user"""
        users = self._load_users()
        
        if username in users:
            return False, "Username already exists"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        users[username] = {
            "password": self._hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        
        self._save_users(users)
        return True, "Registration successful"
    
    def login_user(self, username, password):
        """Authenticate user"""
        users = self._load_users()
        
        if username not in users:
            return False, "Invalid username or password"
        
        if users[username]["password"] != self._hash_password(password):
            return False, "Invalid username or password"
        
        # Update last login
        users[username]["last_login"] = datetime.now().isoformat()
        self._save_users(users)
        
        return True, "Login successful"
    
    def get_user_info(self, username):
        """Get user information"""
        users = self._load_users()
        return users.get(username, None)
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        users = self._load_users()
        
        if username not in users:
            return False, "User not found"
        
        if users[username]["password"] != self._hash_password(old_password):
            return False, "Invalid current password"
        
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters"
        
        users[username]["password"] = self._hash_password(new_password)
        self._save_users(users)
        
        return True, "Password changed successfully"
