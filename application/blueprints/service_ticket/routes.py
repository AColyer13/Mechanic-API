"""Service ticket routes for CRUD operations and mechanic assignment."""

from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from application.extensions import db
from application.models import ServiceTicket, Mechanic, Customer, Inventory
from .schemas import service_ticket_schema, service_tickets_schema, service_ticket_simple_schema, service_tickets_simple_schema
from . import service_ticket_bp


@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    """Create a new service ticket."""
    try:
        # Validate customer exists
        customer_id = request.json.get('customer_id')
        if not Customer.query.get(customer_id):
            return {'error': 'Customer not found'}, 404
        
        ticket_data = service_ticket_schema.load(request.json)
        db.session.add(ticket_data)
        db.session.commit()
        return service_ticket_simple_schema.dump(ticket_data), 201
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while creating the service ticket'}, 500


@service_ticket_bp.route('/', methods=['GET'])
def get_service_tickets():
    """Retrieve all service tickets."""
    try:
        tickets = ServiceTicket.query.all()
        return service_tickets_schema.dump(tickets), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving service tickets'}, 500


@service_ticket_bp.route('/<int:ticket_id>', methods=['GET'])
def get_service_ticket(ticket_id):
    """Retrieve a specific service ticket by ID."""
    try:
        ticket = ServiceTicket.query.get(ticket_id)
        if not ticket:
            return {'error': 'Service ticket not found'}, 404
        return service_ticket_schema.dump(ticket), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving the service ticket'}, 500


@service_ticket_bp.route('/<int:ticket_id>', methods=['PUT'])
def update_service_ticket(ticket_id):
    """Update a specific service ticket."""
    try:
        ticket = ServiceTicket.query.get(ticket_id)
        if not ticket:
            return {'error': 'Service ticket not found'}, 404
        
        update_data = service_ticket_schema.load(request.json, instance=ticket, partial=True)
        
        # Set completed_at if status changes to 'Completed'
        if 'status' in request.json and request.json['status'] == 'Completed' and ticket.status != 'Completed':
            update_data.completed_at = datetime.utcnow()
        
        db.session.commit()
        return service_ticket_simple_schema.dump(update_data), 200
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while updating the service ticket'}, 500


@service_ticket_bp.route('/<int:ticket_id>', methods=['DELETE'])
def delete_service_ticket(ticket_id):
    """Delete a specific service ticket."""
    try:
        ticket = ServiceTicket.query.get(ticket_id)
        if not ticket:
            return {'error': 'Service ticket not found'}, 404
        
        db.session.delete(ticket)
        db.session.commit()
        return {'message': f'Service ticket {ticket_id} deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while deleting the service ticket'}, 500


@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    """Assign a mechanic to a service ticket."""
    try:
        ticket = ServiceTicket.query.get(ticket_id)
        mechanic = Mechanic.query.get(mechanic_id)
        if not ticket or not mechanic:
            return {'error': 'Service ticket or mechanic not found'}, 404
        
        if mechanic in ticket.mechanics:
            return {'error': 'Mechanic already assigned'}, 409
        
        ticket.mechanics.append(mechanic)
        # Auto-update status to 'In Progress' if 'Open'
        if ticket.status == 'Open':
            ticket.status = 'In Progress'
        db.session.commit()
        return {'message': f'Mechanic {mechanic_id} assigned to ticket {ticket_id}'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while assigning the mechanic'}, 500


@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    """Remove a mechanic from a service ticket."""
    try:
        ticket = ServiceTicket.query.get(ticket_id)
        mechanic = Mechanic.query.get(mechanic_id)
        if not ticket or not mechanic:
            return {'error': 'Service ticket or mechanic not found'}, 404
        
        if mechanic not in ticket.mechanics:
            return {'error': 'Mechanic not assigned to this ticket'}, 409
        
        ticket.mechanics.remove(mechanic)
        db.session.commit()
        return {'message': f'Mechanic {mechanic_id} removed from ticket {ticket_id}'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while removing the mechanic'}, 500


@service_ticket_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_tickets_by_customer(customer_id):
    """Get all service tickets for a customer."""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        return service_tickets_simple_schema.dump(customer.service_tickets), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving tickets'}, 500


@service_ticket_bp.route('/mechanic/<int:mechanic_id>', methods=['GET'])
def get_tickets_by_mechanic(mechanic_id):
    """Get all service tickets for a mechanic."""
    try:
        mechanic = Mechanic.query.get(mechanic_id)
        if not mechanic:
            return {'error': 'Mechanic not found'}, 404
        return service_tickets_simple_schema.dump(mechanic.service_tickets), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving tickets'}, 500


@service_ticket_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, inventory_id):
    """Add a single inventory part to a service ticket."""
    try:
        ticket = ServiceTicket.query.get(ticket_id)
        inventory = Inventory.query.get(inventory_id)
        if not ticket or not inventory:
            return {'error': 'Service ticket or inventory item not found'}, 404
        
        if inventory in ticket.inventories:
            return {'error': 'Part already added to this ticket'}, 409
        
        ticket.inventories.append(inventory)
        db.session.commit()
        return {'message': f'Part {inventory_id} added to ticket {ticket_id}'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while adding the part'}, 500