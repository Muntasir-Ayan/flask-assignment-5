import jwt
import functools
from flask import request, current_app
from flask_restx import abort
from datetime import datetime, timedelta
import hashlib
import uuid

# In-memory storage for tokens
TOKEN_STORAGE = {}

def generate_token(user_id, role):
    """Generate JWT token for a user"""
    # Token expires in 1 hour
    expiration = datetime.utcnow() + timedelta(hours=1)
    
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': expiration
    }
    
    token = jwt.encode(payload, 'SECRET_KEY', algorithm='HS256')
    
    # Store token details
    TOKEN_STORAGE[token] = {
        'user_id': user_id,
        'role': role,
        'exp': expiration
    }
    
    return token

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify provided password against stored hash"""
    return stored_password == hash_password(provided_password)

def token_required(roles=None):
    """
    Decorator to require authentication and optional role-based access
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            # Get token from Authorization header
            token = request.headers.get('Authorization')
            if not token:
                abort(401, 'Token is missing')
            
            try:
                # Check if token exists and is not expired
                token_info = TOKEN_STORAGE.get(token)
                if not token_info:
                    abort(401, 'Invalid token')
                
                # Check token expiration
                if datetime.utcnow() > token_info['exp']:
                    del TOKEN_STORAGE[token]
                    abort(401, 'Token has expired')
                
                # Check role if specified
                if roles and token_info['role'] not in roles:
                    abort(403, 'Insufficient permissions')
                
                return fn(*args, **kwargs)
            
            except Exception as e:
                abort(401, str(e))
        
        return wrapper
    return decorator