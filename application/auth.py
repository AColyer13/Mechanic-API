"""Authentication utilities for JWT token handling."""

import jwt
from functools import wraps
from flask import request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import Customer
from application.extensions import db


def encode_token(customer_id):
    """Generate a JWT token for the given customer_id."""
    payload = {'customer_id': customer_id}
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token


def token_required(f):
    """Decorator to require a valid JWT token and extract customer_id."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return {'error': 'Token is missing'}, 401
        
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            customer_id = payload['customer_id']
            # Verify customer exists
            customer = Customer.query.get(customer_id)
            if not customer:
                return {'error': 'Invalid token'}, 401
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}, 401
        
        # Pass customer_id to the decorated function
        return f(customer_id, *args, **kwargs)
    
    return decorated_function


def hash_password(password):
    """Hash a password for storage."""
    return generate_password_hash(password)


def check_password(password_hash, password):
    """Check a password against its hash."""
    return check_password_hash(password_hash, password)
