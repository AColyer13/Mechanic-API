"""Customer routes for CRUD operations."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from application.extensions import db
from application.models import Customer, ServiceTicket
from .customerSchemas import customer_schema, customers_schema, customer_simple_schema, customers_simple_schema, login_schema
from . import customer_bp
from application.auth import encode_token, token_required
from application.blueprints.service_ticket.schemas import service_tickets_schema


@customer_bp.route('/', methods=['POST'])
def create_customer():
    """Create a new customer."""
    try:
        # Validate and deserialize input
        customer_data = customer_schema.load(request.json)
        
        # Hash the password
        customer_data.password = generate_password_hash(customer_data.password)
        
        # Save to database
        db.session.add(customer_data)
        db.session.commit()
        
        # Return serialized customer
        return customer_simple_schema.dump(customer_data), 201
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Customer with this email already exists'}, 409
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while creating the customer'}, 500


@customer_bp.route('/', methods=['GET'])
def get_customers():
    """Retrieve all customers."""
    try:
        customers = Customer.query.all()
        return customers_simple_schema.dump(customers), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving customers'}, 500


@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Retrieve a specific customer by ID."""
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
            
        return customer_schema.dump(customer), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving the customer'}, 500


@customer_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer(token_customer_id, customer_id):
    """Update a specific customer."""
    if token_customer_id != customer_id:
        return {'error': 'Unauthorized to update this customer'}, 403
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        # Validate and update customer data
        update_data = customer_schema.load(request.json, instance=customer, partial=True)
        
        # Hash password if provided
        if 'password' in request.json:
            update_data.password = generate_password_hash(update_data.password)
        
        # Save changes
        db.session.commit()
        
        return customer_simple_schema.dump(update_data), 200
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {'error': 'Customer with this email already exists'}, 409
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while updating the customer'}, 500


@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
@token_required
def delete_customer(token_customer_id, customer_id):
    """Delete a specific customer."""
    if token_customer_id != customer_id:
        return {'error': 'Unauthorized to delete this customer'}, 403
    try:
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        # Check if customer has service tickets
        if customer.service_tickets:
            return {'error': 'Cannot delete customer with active service tickets'}, 409
        
        db.session.delete(customer)
        db.session.commit()
        
        return {'message': f'Customer {customer_id} deleted successfully'}, 200
        
    except Exception as e:
        db.session.rollback()
        return {'error': 'An error occurred while deleting the customer'}, 500


@customer_bp.route('/login', methods=['POST'])
def login():
    """Authenticate customer and return JWT token."""
    try:
        # Validate input
        data = login_schema.load(request.json)
        
        # Find customer by email
        customer = Customer.query.filter_by(email=data.email).first()
        if not customer or not check_password_hash(customer.password, data.password):
            return {'error': 'Invalid email or password'}, 401
        
        # Generate token
        token = encode_token(customer.id)
        return {'token': token}, 200
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        return {'error': 'An error occurred during login'}, 500


@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    """Retrieve service tickets for the authenticated customer."""
    try:
        tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
        return service_tickets_schema.dump(tickets), 200
    except Exception as e:
        return {'error': 'An error occurred while retrieving tickets'}, 500