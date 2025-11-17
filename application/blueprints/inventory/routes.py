"""Inventory routes for CRUD operations."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from application.extensions import db, limiter, cache
from application.models import Inventory
from .schemas import inventory_schema, inventories_schema, inventory_simple_schema, inventories_simple_schema
from . import inventory_bp


@inventory_bp.route('/', methods=['POST'])
@limiter.limit("20 per minute")  # Rate limiting: max 20 inventory creations per minute
def create_inventory():
    """Create a new inventory part."""
    try:
        # Validate and deserialize input
        inventory_data = inventory_schema.load(request.json)
        
        # Save to database
        db.session.add(inventory_data)
        db.session.commit()
        
        # Clear the cache for all inventory list
        cache.delete('all_inventory')
        
        # Return serialized inventory
        return inventory_simple_schema.dump(inventory_data), 201
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while creating the inventory part'}, 500


@inventory_bp.route('/', methods=['GET'])
@cache.cached(timeout=300, key_prefix='all_inventory')  # Cache for 5 minutes
def get_inventory():
    """Retrieve all inventory parts."""
    try:
        inventory_items = Inventory.query.all()
        return inventories_simple_schema.dump(inventory_items), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving inventory'}, 500


@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    """Retrieve a specific inventory part by ID."""
    try:
        inventory_item = Inventory.query.get(inventory_id)
        if not inventory_item:
            return {'error': 'Inventory part not found'}, 404
            
        return inventory_schema.dump(inventory_item), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving the inventory part'}, 500


@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    """Update a specific inventory part."""
    try:
        inventory_item = Inventory.query.get(inventory_id)
        if not inventory_item:
            return {'error': 'Inventory part not found'}, 404
        
        # Validate and update inventory data
        inventory_data = inventory_schema.load(request.json, instance=inventory_item, partial=True)
        
        # Save changes
        db.session.commit()
        
        # Clear the cache
        cache.delete('all_inventory')
        
        return inventory_simple_schema.dump(inventory_data), 200
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while updating the inventory part'}, 500


@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    """Delete a specific inventory part."""
    try:
        inventory_item = Inventory.query.get(inventory_id)
        if not inventory_item:
            return {'error': 'Inventory part not found'}, 404
        
        # Check if inventory part is used in service tickets
        if inventory_item.service_tickets:
            return {'error': 'Cannot delete inventory part that is used in service tickets'}, 409
        
        db.session.delete(inventory_item)
        db.session.commit()
        
        # Clear the cache
        cache.delete('all_inventory')
        
        return {'message': f'Inventory part {inventory_id} deleted successfully'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while deleting the inventory part'}, 500
