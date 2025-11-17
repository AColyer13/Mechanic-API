"""Inventory routes for CRUD operations."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from application.extensions import db
from application.models import Inventory
from .schemas import inventory_schema, inventories_schema, inventory_simple_schema, inventories_simple_schema
from . import inventory_bp


@inventory_bp.route('/', methods=['POST'])
def create_inventory_part():
    """Create a new inventory part."""
    try:
        # Validate and deserialize input
        inventory_data = inventory_schema.load(request.json)
        
        # Save to database
        db.session.add(inventory_data)
        db.session.commit()
        
        # Return serialized inventory part
        return inventory_simple_schema.dump(inventory_data), 201
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while creating the inventory part'}, 500


@inventory_bp.route('/', methods=['GET'])
def get_inventory_parts():
    """Retrieve all inventory parts."""
    try:
        parts = Inventory.query.all()
        return inventories_simple_schema.dump(parts), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving inventory parts'}, 500


@inventory_bp.route('/<int:part_id>', methods=['GET'])
def get_inventory_part(part_id):
    """Retrieve a specific inventory part by ID."""
    try:
        part = Inventory.query.get(part_id)
        if not part:
            return {'error': 'Inventory part not found'}, 404
            
        return inventory_schema.dump(part), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving the inventory part'}, 500


@inventory_bp.route('/<int:part_id>', methods=['PUT'])
def update_inventory_part(part_id):
    """Update a specific inventory part."""
    try:
        part = Inventory.query.get(part_id)
        if not part:
            return {'error': 'Inventory part not found'}, 404
        
        # Validate and update part data
        part_data = inventory_schema.load(request.json, instance=part, partial=True)
        
        # Save changes
        db.session.commit()
        
        return inventory_simple_schema.dump(part_data), 200
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while updating the inventory part'}, 500


@inventory_bp.route('/<int:part_id>', methods=['DELETE'])
def delete_inventory_part(part_id):
    """Delete a specific inventory part."""
    try:
        part = Inventory.query.get(part_id)
        if not part:
            return {'error': 'Inventory part not found'}, 404
        
        # Check if part is used in any service tickets
        if part.service_tickets.count() > 0:
            return {'error': 'Cannot delete inventory part that is used in service tickets'}, 409
        
        db.session.delete(part)
        db.session.commit()
        
        return {'message': f'Inventory part {part_id} deleted successfully'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while deleting the inventory part'}, 500
