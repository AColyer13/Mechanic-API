from functools import wraps
from flask import request, jsonify, current_app
from jose import jwt, JWTError
from datetime import datetime, timedelta

def encode_token(customer_id):
    payload = {
        'customer_id': customer_id,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            customer_id = payload['customer_id']
        except JWTError:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(customer_id, *args, **kwargs)
    
    return decorated_function
