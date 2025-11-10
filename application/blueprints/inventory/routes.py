"""Inventory routes for CRUD operations."""

from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from application.extensions import db
from application.models import Inventory
from .schemas import inventory_schema, inventories_schema, inventory_simple_schema, inventories_simple_schema
from . import inventory_bp


@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    """Add a new part to inventory."""
    try:
        inventory_data = inventory_schema.load(request.json)
        db.session.add(inventory_data)
        db.session.commit()
        return inventory_simple_schema.dump(inventory_data), 201
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while adding the part'}, 500


@inventory_bp.route('/', methods=['GET'])
def get_inventories():
    """Get all inventory items."""
    try:
        inventories = Inventory.query.all()
        return inventories_simple_schema.dump(inventories), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving inventory'}, 500


@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory(inventory_id):
    """Get a specific inventory item by ID."""
    try:
        inventory = Inventory.query.get(inventory_id)
        if not inventory:
            return {'error': 'Inventory item not found'}, 404
        return inventory_schema.dump(inventory), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving the inventory item'}, 500


@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
def update_inventory(inventory_id):
    """Update an inventory item."""
    try:
        inventory = Inventory.query.get(inventory_id)
        if not inventory:
            return {'error': 'Inventory item not found'}, 404
        
        update_data = inventory_schema.load(request.json, instance=inventory, partial=True)
        db.session.commit()
        return inventory_simple_schema.dump(update_data), 200
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while updating the inventory item'}, 500


@inventory_bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    """Delete an inventory item."""
    try:
        inventory = Inventory.query.get(inventory_id)
        if not inventory:
            return {'error': 'Inventory item not found'}, 404
        
        db.session.delete(inventory)
        db.session.commit()
        return {'message': f'Inventory item {inventory_id} deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while deleting the inventory item'}, 500
