"""Customer routes for CRUD operations."""

from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from application.extensions import db
from application.models import Customer
from .customerSchemas import customer_schema, customers_schema, customer_simple_schema, customers_simple_schema
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
def update_customer(customer_id):
    """Update a specific customer."""
    try:
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
def delete_customer(customer_id):
    """Delete a specific customer."""
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