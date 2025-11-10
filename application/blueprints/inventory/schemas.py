"""Inventory schemas for serialization and deserialization."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate, pre_load
from application.models import Inventory
from application.extensions import db, ma


class InventorySchema(SQLAlchemyAutoSchema):
    """Schema for Inventory model with validation."""
    
    class Meta:
        model = Inventory
        load_instance = True
        sqla_session = db.session
        
    # Custom field validations
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    
    # Read-only fields
    id = fields.Int(dump_only=True)
    
    # Include service tickets when needed
    service_tickets = fields.Nested('ServiceTicketSchema', many=True, dump_only=True, exclude=('inventories',))
    
    @pre_load
    def strip_whitespace(self, data, **kwargs):
        """Strip whitespace from string fields."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = value.strip()
        return data


# Schema instances
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)

# Schema without service tickets for simpler responses
inventory_simple_schema = InventorySchema(exclude=['service_tickets'])
inventories_simple_schema = InventorySchema(many=True, exclude=['service_tickets'])
