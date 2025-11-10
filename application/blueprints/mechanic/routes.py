"""Mechanic routes for CRUD operations."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from application.extensions import db
from application.models import Mechanic
from .schemas import mechanic_schema, mechanics_schema, mechanic_simple_schema, mechanics_simple_schema
from . import mechanic_bp


@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    """Create a new mechanic."""
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
def get_mechanics():
    """Retrieve all mechanics."""
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
        assigned_tickets = mechanic.service_tickets.all()
        if assigned_tickets:
            blocking_tickets = [{'id': t.id, 'description': t.description} for t in assigned_tickets]
            return {'error': 'Cannot delete mechanic who is assigned to service tickets', 'assigned_tickets': blocking_tickets}, 409
        
        db.session.delete(mechanic)
        db.session.commit()
        
        return {'message': f'Mechanic {mechanic_id} deleted successfully'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while deleting the mechanic'}, 500