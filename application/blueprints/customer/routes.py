"""Customer routes for CRUD operations."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from application.extensions import db, limiter, cache, encode_token, token_required
from application.models import Customer, ServiceTicket
from werkzeug.security import check_password_hash
from .customerSchemas import customer_schema, customers_schema, customer_simple_schema, customers_simple_schema, login_schema
from . import customer_bp


@customer_bp.route('/', methods=['POST'])
def create_customer():
    """Create a new customer."""
    try:
        # Validate and deserialize input
        customer_data = customer_schema.load(request.json)
        
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
    """Retrieve all customers with pagination support."""
    try:
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:  # Limit max per_page to prevent abuse
            per_page = 10
        
        # Query customers with pagination
        customers_pagination = Customer.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Serialize the customers
        customers_data = customers_simple_schema.dump(customers_pagination.items)
        
        # Build response with pagination metadata
        response = {
            'customers': customers_data,
            'pagination': {
                'page': customers_pagination.page,
                'per_page': customers_pagination.per_page,
                'total_pages': customers_pagination.pages,
                'total_customers': customers_pagination.total,
                'has_next': customers_pagination.has_next,
                'has_prev': customers_pagination.has_prev,
                'next_page': customers_pagination.next_num if customers_pagination.has_next else None,
                'prev_page': customers_pagination.prev_num if customers_pagination.has_prev else None
            }
        }
        
        return response, 200
        
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


@customer_bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit login attempts to prevent brute force
def login():
    """
    Customer login endpoint - validates credentials and returns JWT token.
    Rate limited to prevent brute force attacks on login.
    """
    try:
        # Validate input using login schema
        credentials = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Find customer by email
    query = select(Customer).where(Customer.email == credentials['email'])
    customer = db.session.execute(query).scalar_one_or_none()
    
    # Verify customer exists and password is correct
    if customer and check_password_hash(customer.password, credentials['password']):
        # Generate token for the customer
        token = encode_token(customer.id)
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'customer_id': customer.id
        }), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@customer_bp.route('/my-tickets', methods=['GET'])
@token_required
@cache.cached(timeout=180)  # Cache customer's tickets for 3 minutes
def get_my_tickets(customer_id):
    """
    Get all service tickets for the authenticated customer.
    Requires Bearer Token authorization.
    Caching improves performance for frequent ticket status checks.
    """
    from application.blueprints.service_ticket.schemas import service_tickets_schema
    
    # Query service tickets for the authenticated customer
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(tickets), 200


# Apply token protection to sensitive customer routes
@customer_bp.route('/<int:customer_id>', methods=['PUT'])
@token_required
def update_customer_protected(authenticated_customer_id, customer_id):
    """
    Update customer - requires token authentication.
    Customers can only update their own information.
    """
    # Ensure customer can only update their own information
    if authenticated_customer_id != customer_id:
        return jsonify({'message': 'Unauthorized - can only update your own information'}), 403
    
    # ...existing update logic...
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalar_one_or_none()
    
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    
    # Update customer fields
    for field, value in customer_data.items():
        setattr(customer, field, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200


@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
@token_required
def delete_customer_protected(authenticated_customer_id, customer_id):
    """
    Delete customer - requires token authentication.
    Customers can only delete their own account.
    """
    # Ensure customer can only delete their own account
    if authenticated_customer_id != customer_id:
        return jsonify({'message': 'Unauthorized - can only delete your own account'}), 403
    
    # ...existing delete logic...
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalar_one_or_none()
    
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200