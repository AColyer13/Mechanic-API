"""Service ticket routes for CRUD operations and mechanic assignment."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from application.extensions import db
from application.models import ServiceTicket, Customer, Mechanic, Inventory
from .schemas import (service_ticket_schema, service_tickets_schema, 
                     service_ticket_simple_schema, service_tickets_simple_schema)
from . import service_ticket_bp


@service_ticket_bp.route('/', methods=['POST'])
def create_service_ticket():
    """Create a new service ticket."""
    try:
        # Validate and deserialize input
        ticket_data = service_ticket_schema.load(request.json)
        
        # Verify customer exists
        customer = Customer.query.get(ticket_data.customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        # Save to database
        db.session.add(ticket_data)
        db.session.commit()
        
        # Return serialized ticket
        return service_ticket_schema.dump(ticket_data), 201
        
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
        
        # Get the current status before update
        old_status = ticket.status
        
        # Validate and update ticket data
        ticket_data = service_ticket_schema.load(request.json, instance=ticket, partial=True)
        
        # Handle status change to completed
        if hasattr(ticket_data, 'status') and ticket_data.status == 'Completed' and old_status != 'Completed':
            ticket_data.completed_at = datetime.utcnow()
        # Clear completed_at if status changes away from Completed
        elif hasattr(ticket_data, 'status') and ticket_data.status != 'Completed' and old_status == 'Completed':
            ticket_data.completed_at = None
        
        # Save changes
        db.session.commit()
        
        return service_ticket_schema.dump(ticket_data), 200
        
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
        if not ticket:
            return {'error': 'Service ticket not found'}, 404
        
        mechanic = Mechanic.query.get(mechanic_id)
        if not mechanic:
            return {'error': 'Mechanic not found'}, 404
        
        # Check if mechanic is already assigned
        if mechanic in ticket.mechanics:
            return {'error': 'Mechanic is already assigned to this ticket'}, 409
        
        # Assign mechanic
        ticket.mechanics.append(mechanic)
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
        if not ticket:
            return {'error': 'Service ticket not found'}, 404
        
        mechanic = Mechanic.query.get(mechanic_id)
        if not mechanic:
            return {'error': 'Mechanic not found'}, 404
        
        # Check if mechanic is assigned
        if mechanic not in ticket.mechanics:
            return {'error': 'Mechanic is not assigned to this ticket'}, 409
        
        # Remove mechanic
        ticket.mechanics.remove(mechanic)
        db.session.commit()
        
        return {'message': f'Mechanic {mechanic_id} removed from ticket {ticket_id}'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while removing the mechanic'}, 500


@service_ticket_bp.route('/customer/<int:customer_id>', methods=['GET'])
def get_tickets_by_customer(customer_id):
    """Get all service tickets for a specific customer."""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
        return service_tickets_schema.dump(tickets), 200
        
    except Exception as e:
        return {'error': 'An error occurred while retrieving customer tickets'}, 500


@service_ticket_bp.route('/mechanic/<int:mechanic_id>', methods=['GET'])
def get_tickets_by_mechanic(mechanic_id):
    """Get all service tickets assigned to a specific mechanic."""
    try:
        mechanic = Mechanic.query.get(mechanic_id)
        if not mechanic:
            return {'error': 'Mechanic not found'}, 404
        
        tickets = mechanic.service_tickets.all()
        return service_tickets_schema.dump(tickets), 200
        
    except Exception as e:
        return {'error': 'An error occurred while retrieving mechanic tickets'}, 500


@service_ticket_bp.route('/<int:ticket_id>/add-part/<int:inventory_id>', methods=['PUT'])
def add_part_to_ticket(ticket_id, inventory_id):
    """Add a single inventory part to an existing service ticket."""
    try:
        ticket = ServiceTicket.query.get(ticket_id)
        if not ticket:
            return {'error': 'Service ticket not found'}, 404
        
        inventory_part = Inventory.query.get(inventory_id)
        if not inventory_part:
            return {'error': 'Inventory part not found'}, 404
        
        # Check if part is already added
        if inventory_part in ticket.inventory_parts:
            return {'error': 'Part is already added to this ticket'}, 409
        
        # Add part to ticket
        ticket.inventory_parts.append(inventory_part)
        db.session.commit()
        
        return {'message': f'Part {inventory_id} added to ticket {ticket_id}'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while adding the part'}, 500