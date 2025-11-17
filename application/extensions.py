"""Extensions module for initializing Flask extensions."""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

# Initialize Flask-Limiter with remote address as key function
limiter = Limiter(key_func=get_remote_address)

# Initialize Flask-Caching with SimpleCache (in-memory caching)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

# JWT Authentication Functions
def encode_token(customer_id):
    """
    Creates a JWT token for a specific customer.
    
    Args:
        customer_id (int): The ID of the customer
        
    Returns:
        str: JWT token string
    """
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.utcnow(),  # Token issued at
        'sub': customer_id  # Subject (customer ID)
    }
    
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY', 'your-secret-key'),
        algorithm='HS256'
    )

def token_required(f):
    """
    Decorator that validates JWT token and extracts customer_id.
    
    The decorated function will receive customer_id as its first argument.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Expected format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'message': 'Token format invalid. Expected: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Decode the token
            payload = jwt.decode(
                token,
                current_app.config.get('SECRET_KEY', 'your-secret-key'),
                algorithms=['HS256']
            )
            customer_id = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        # Pass customer_id as first argument to the decorated function
        return f(customer_id, *args, **kwargs)
    
    return decorated