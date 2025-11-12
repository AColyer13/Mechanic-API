from flask import Blueprint, request, jsonify
from application.extensions import limiter, cache
from application.models import Mechanic
from application import db

mechanics_bp = Blueprint('mechanics', __name__)

@mechanics_bp.route('/mechanics', methods=['POST'])
@limiter.limit("5 per hour")  # Rate limit: only 5 mechanic registrations per hour
def create_mechanic():
    # Rate limiting is important here to prevent spam registration of fake mechanics
    # and protect against potential abuse of the registration system
    data = request.get_json()
    new_mechanic = Mechanic(
        name=data['name'],
        phone=data['phone'],
        email=data['email'],
        location=data['location']
    )
    db.session.add(new_mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic registered successfully"}), 201

@mechanics_bp.route('/mechanics', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes (300 seconds)
def get_mechanics():
    # Caching is important here because the list of mechanics doesn't change frequently
    # and this endpoint might be called often for display purposes
    # Reduces database load and improves response time
    mechanics = Mechanic.query.all()
    return jsonify([mechanic.serialize() for mechanic in mechanics]), 200