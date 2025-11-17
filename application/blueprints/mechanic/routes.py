"""Mechanic routes for CRUD operations."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, desc
from application.extensions import db, limiter, cache
from application.models import Mechanic, ServiceTicket, service_ticket_mechanics
from .schemas import mechanic_schema, mechanics_schema, mechanic_simple_schema, mechanics_simple_schema
from . import mechanic_bp


@mechanic_bp.route('/', methods=['POST'])
@limiter.limit("5 per hour")  # Rate limit: only 5 mechanic registrations per hour
def create_mechanic():
    """Create a new mechanic with rate limiting to prevent spam registration."""
    try:
        # Validate and deserialize input
        mechanic_data = mechanic_schema.load(request.json)
        
        # Save to database
        db.session.add(mechanic_data)
        db.session.commit()
        
        # Return serialized mechanic
        return mechanic_simple_schema.dump(mechanic_data), 201
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Mechanic with this email already exists'}, 409
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while creating the mechanic'}, 500


@mechanic_bp.route('/', methods=['GET'])
@cache.cached(timeout=300)  # Cache for 5 minutes (300 seconds)
def get_mechanics():
    """
    Retrieve all mechanics with caching.
    Caching is important here because the list of mechanics doesn't change frequently
    and this endpoint might be called often for display purposes.
    """
    try:
        mechanics = Mechanic.query.all()
        return mechanics_simple_schema.dump(mechanics), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving mechanics'}, 500


@mechanic_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    """Retrieve a specific mechanic by ID."""
    try:
        mechanic = Mechanic.query.get(mechanic_id)
        if not mechanic:
            return {'error': 'Mechanic not found'}, 404
            
        return mechanic_schema.dump(mechanic), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving the mechanic'}, 500


@mechanic_bp.route('/<int:mechanic_id>', methods=['PUT'])
def update_mechanic(mechanic_id):
    """Update a specific mechanic."""
    try:
        mechanic = Mechanic.query.get(mechanic_id)
        if not mechanic:
            return {'error': 'Mechanic not found'}, 404
        
        # Validate and update mechanic data
        mechanic_data = mechanic_schema.load(request.json, instance=mechanic, partial=True)
        
        # Save changes
        db.session.commit()
        
        return mechanic_simple_schema.dump(mechanic_data), 200
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Mechanic with this email already exists'}, 409
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while updating the mechanic'}, 500


@mechanic_bp.route('/<int:mechanic_id>', methods=['DELETE'])
def delete_mechanic(mechanic_id):
    """Delete a specific mechanic."""
    try:
        mechanic = Mechanic.query.get(mechanic_id)
        if not mechanic:
            return {'error': 'Mechanic not found'}, 404
        
        # Check if mechanic is assigned to any service tickets
        if mechanic.service_tickets.count() > 0:
            return {'error': 'Cannot delete mechanic who is assigned to service tickets'}, 409
        
        db.session.delete(mechanic)
        db.session.commit()
        
        return {'message': f'Mechanic {mechanic_id} deleted successfully'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while deleting the mechanic'}, 500


@mechanic_bp.route('/by-workload', methods=['GET'])
def get_mechanics_by_workload():
    """Get mechanics ordered by the number of tickets they've worked on (most to least)."""
    try:
        # Query mechanics with ticket count using LEFT JOIN and GROUP BY
        mechanics_with_counts = db.session.query(
            Mechanic,
            func.count(service_ticket_mechanics.c.service_ticket_id).label('ticket_count')
        ).outerjoin(
            service_ticket_mechanics, 
            Mechanic.id == service_ticket_mechanics.c.mechanic_id
        ).group_by(Mechanic.id).order_by(desc('ticket_count')).all()
        
        # Format the response
        result = []
        for mechanic, ticket_count in mechanics_with_counts:
            mechanic_data = mechanic_simple_schema.dump(mechanic)
            mechanic_data['ticket_count'] = ticket_count
            result.append(mechanic_data)
        
        return {
            'mechanics': result,
            'total_mechanics': len(result),
            'message': 'Mechanics ordered by workload (most tickets first)'
        }, 200
        
    except Exception as e:
        return {'error': 'An error occurred while retrieving mechanics by workload'}, 500