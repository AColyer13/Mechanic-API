"""Customer schemas for serialization and deserialization."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, ValidationError, pre_load, post_load
from werkzeug.security import generate_password_hash
from application.models import Customer
from application.extensions import db, ma


class CustomerSchema(SQLAlchemyAutoSchema):
    """Schema for Customer model with validation."""
    
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session
        include_fk = True
        
    # Custom field validations
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6), load_only=True)  # Never dump password
    phone = fields.Str(validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=200))
    
    # Read-only fields
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Include service tickets when needed
    service_tickets = fields.Nested('ServiceTicketSchema', many=True, dump_only=True, exclude=('customer',))
    
    @pre_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip()
        return data
    
    @post_load
    def hash_password(self, data, **kwargs):
        """Hash password before saving to database."""
        if hasattr(data, 'password') and data.password:
            data.password = generate_password_hash(data.password)
        elif isinstance(data, dict) and 'password' in data:
            data['password'] = generate_password_hash(data['password'])
        return data


# Schema instances
customer_schema = CustomerSchema(exclude=['password'])  # Exclude password from regular operations
customers_schema = CustomerSchema(many=True, exclude=['password'])  # Exclude password from list operations

# Schema without service tickets for simpler responses
customer_simple_schema = CustomerSchema(exclude=['service_tickets', 'password'])
customers_simple_schema = CustomerSchema(many=True, exclude=['service_tickets', 'password'])

# Schema for customer registration (includes password)
customer_registration_schema = CustomerSchema(exclude=['service_tickets'])

# Login schema - only email and password fields
login_schema = CustomerSchema(only=('email', 'password'))