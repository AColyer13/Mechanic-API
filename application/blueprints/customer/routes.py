"""Customer routes for CRUD operations."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt
from application.extensions import db, limiter, cache, encode_token, token_required
from application.models import Customer, ServiceTicket
from .customerSchemas import customer_schema, customers_schema, customer_simple_schema, customers_simple_schema, login_schema
from . import customer_bp


@customer_bp.route('/login', methods=['POST'])
def login():
    """Customer login endpoint - returns JWT token."""
    try:
        # Validate input
        credentials = login_schema.load(request.json)
        
        # Find customer by email
        customer = Customer.query.filter_by(email=credentials['email']).first()
        
        if not customer:
            return {'error': 'Invalid email or password'}, 401
        
        # Verify password
        if not bcrypt.verify(credentials['password'], customer.password):
            return {'error': 'Invalid email or password'}, 401
        
        # Generate token
        token = encode_token(customer.id)
        
        return {
            'message': 'Login successful',
            'token': token,
            'customer': customer_simple_schema.dump(customer)
        }, 200
        
    except ValidationError as err:
        return {'errors': err.messages}, 400
    except Exception as e:
        return {'error': 'An error occurred during login'}, 500


@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
def get_my_tickets(customer_id):
    """Get service tickets for the authenticated customer - requires Bearer token."""
    try:
        # Query service tickets for this customer
        tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
        
        # Import schema here to avoid circular import
        from application.blueprints.service_ticket.schemas import service_tickets_schema
        
        return service_tickets_schema.dump(tickets), 200
        
    except Exception as e:
        return {'error': 'An error occurred while retrieving tickets'}, 500


@customer_bp.route('/', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limiting: max 10 customer creations per minute
def create_customer():
    """Create a new customer."""
    try:
        # Validate and deserialize input
        customer_data = customer_schema.load(request.json)
        
        # Save to database
        db.session.add(customer_data)
        db.session.commit()
        
        # Clear the cache for all customers list
        cache.delete('all_customers')
        
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
@cache.cached(timeout=300, key_prefix='all_customers')  # Cache for 5 minutes
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
def update_customer(authenticated_customer_id, customer_id):
    """Update a specific customer - requires token and must be own account."""
    try:
        # Ensure customer can only update their own account
        if authenticated_customer_id != customer_id:
            return {'error': 'You can only update your own account'}, 403
        
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        # Validate and update customer data
        customer_data = customer_schema.load(request.json, instance=customer, partial=True)
        
        # Save changes
        db.session.commit()
        
        return customer_simple_schema.dump(customer_data), 200
        
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
def delete_customer(authenticated_customer_id, customer_id):
    """Delete a specific customer - requires token and must be own account."""
    try:
        # Ensure customer can only delete their own account
        if authenticated_customer_id != customer_id:
            return {'error': 'You can only delete your own account'}, 403
        
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