"""Service ticket schemas for serialization and deserialization."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, ValidationError, pre_load, post_load
from datetime import datetime
from application.models import ServiceTicket
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
    vehicle_year = fields.Int(validate=validate.Range(min=1900, max=2050))
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
    customer = fields.Nested('CustomerSchema', dump_only=True, exclude=('service_tickets',))
    mechanics = fields.Nested('MechanicSchema', many=True, dump_only=True, exclude=('service_tickets',))
    inventory_parts = fields.Nested('InventorySchema', many=True, dump_only=True, exclude=('service_tickets',))
    
    @pre_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip()
        return data
    
    @post_load
    def set_completed_at(self, data, **kwargs):
        """Set completed_at timestamp when status changes to Completed."""
        if hasattr(data, 'status') and data.status == 'Completed':
            # Only set completed_at if it's not already set
            if not hasattr(data, 'completed_at') or data.completed_at is None:
                data.completed_at = datetime.utcnow()
        return data


# Schema instances
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)

# Schema without relationships for simpler responses
service_ticket_simple_schema = ServiceTicketSchema(exclude=['customer', 'mechanics'])
service_tickets_simple_schema = ServiceTicketSchema(many=True, exclude=['customer', 'mechanics'])