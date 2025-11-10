"""Mechanic schemas for serialization and deserialization."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, ValidationError, pre_load
from datetime import date
from application.models import Mechanic
from application.extensions import db, ma


class MechanicSchema(SQLAlchemyAutoSchema):
    """Schema for Mechanic model with validation."""
    
    class Meta:
        model = Mechanic
        load_instance = True
        sqla_session = db.session
        include_fk = True
        
    # Custom field validations
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    email = fields.Email(required=True)
    phone = fields.Str(validate=validate.Length(max=20))
    specialty = fields.Str(validate=validate.Length(max=100))
    hourly_rate = fields.Float(validate=validate.Range(min=0))
    hire_date = fields.Date()
    
    # Read-only fields
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    # Include service tickets when needed
    service_tickets = fields.Nested('ServiceTicketSchema', many=True, dump_only=True, exclude=('mechanics',))
    
    @pre_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip()
        return data


# Schema instances
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

# Schema without service tickets for simpler responses
mechanic_simple_schema = MechanicSchema(exclude=['service_tickets'])
mechanics_simple_schema = MechanicSchema(many=True, exclude=['service_tickets'])