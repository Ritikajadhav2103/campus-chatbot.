"""
Authentication utilities for Solapur Colleges Chatbot
Handles user registration, login, and password hashing
"""

import json
import hashlib
import os
import re
from datetime import datetime

# User database file
USER_DB_FILE = "users_database.json"

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def load_users():
    """Load users from database"""
    if os.path.exists(USER_DB_FILE):
        try:
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to database"""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_user(name, email, password):
    """Register a new user"""
    users = load_users()
    
    # Check if email already exists
    if email in users:
        return False, "Email already registered!"
    
    # Validate email
    if not validate_email(email):
        return False, "Invalid email format!"
    
    # Validate password length
    if len(password) < 6:
        return False, "Password must be at least 6 characters!"
    
    # Hash password and store user
    users[email] = {
        'name': name,
        'email': email,
        'password': hash_password(password),
        'created_at': datetime.now().isoformat()
    }
    
    save_users(users)
    return True, "Registration successful!"

def verify_login(email, password):
    """Verify user login credentials"""
    users = load_users()
    
    if email not in users:
        return False, "Email not found!"
    
    if users[email]['password'] != hash_password(password):
        return False, "Incorrect password!"
    
    return True, users[email]['name']

def get_user_info(email):
    """Get user information"""
    users = load_users()
    return users.get(email, None)
