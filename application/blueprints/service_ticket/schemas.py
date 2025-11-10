"""Service Ticket schemas for serialization and deserialization."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, ValidationError, pre_load, validates_schema
from application.models import ServiceTicket, Customer
from application.extensions import db, ma


class ServiceTicketSchema(SQLAlchemyAutoSchema):
    """Schema for ServiceTicket model with validation."""
    
    class Meta:
        model = ServiceTicket
        load_instance = True
        sqla_session = db.session
        include_fk = True
        
    # Custom field validations
    customer_id = fields.Int(required=True)
    vehicle_year = fields.Int(validate=validate.Range(min=1900, max=2030))
    vehicle_make = fields.Str(validate=validate.Length(max=50))
    vehicle_model = fields.Str(validate=validate.Length(max=50))
    vehicle_vin = fields.Str(validate=validate.Length(max=17))
    description = fields.Str(required=True, validate=validate.Length(min=1))
    estimated_cost = fields.Float(validate=validate.Range(min=0))
    actual_cost = fields.Float(validate=validate.Range(min=0))
    status = fields.Str(validate=validate.OneOf(['Open', 'In Progress', 'Completed', 'Cancelled']))
    
    # Read-only fields
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    completed_at = fields.DateTime(dump_only=True)
    
    # Nested relationships
    customer = fields.Nested('CustomerSchema', dump_only=True, exclude=['service_tickets'])
    mechanics = fields.Nested('MechanicSchema', many=True, dump_only=True, exclude=['service_tickets'])
    
    @validates_schema
    def validate_customer_exists(self, data, **kwargs):
        """Validate that the customer exists."""
        if 'customer_id' in data:
            customer = Customer.query.get(data['customer_id'])
            if not customer:
                raise ValidationError('Customer not found', 'customer_id')
    
    @pre_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip()
        return data


# Schema instances
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

# Schema without nested relationships for simpler responses
service_ticket_simple_schema = ServiceTicketSchema(exclude=['customer', 'mechanics'])
service_tickets_simple_schema = ServiceTicketSchema(many=True, exclude=['customer', 'mechanics'])