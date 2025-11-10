import jwt
from functools import wraps
from flask import request, current_app
from werkzeug.security import check_password_hash

def encode_token(customer_id):
    """Encode a JWT token for the given customer_id."""
    payload = {'customer_id': customer_id}
    secret = current_app.config['SECRET_KEY']
    return jwt.encode(payload, secret, algorithm='HS256')

def token_required(f):
    """Decorator to require a valid JWT token and extract customer_id."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'error': 'Token is missing or invalid'}, 401
        try:
            token = auth_header.split()[1]
            secret = current_app.config['SECRET_KEY']
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            customer_id = payload['customer_id']
        except jwt.ExpiredSignatureError:
            return {'error': 'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'error': 'Token is invalid'}, 401
        return f(customer_id, *args, **kwargs)
    return decorated
