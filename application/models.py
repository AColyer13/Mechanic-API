"""Models for the Mechanic Shop API."""

from datetime import datetime
from application.extensions import db

# Association table for many-to-many relationship between Mechanic and ServiceTicket
mechanic_service_ticket = db.Table('mechanic_service_ticket',
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanic.id'), primary_key=True),
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_ticket.id'), primary_key=True)
)

# Association table for many-to-many relationship between Inventory and ServiceTicket
inventory_service_ticket = db.Table('inventory_service_ticket',
    db.Column('inventory_id', db.Integer, db.ForeignKey('inventory.id'), primary_key=True),
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_ticket.id'), primary_key=True)
)

class Customer(db.Model):
    """Customer model."""
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Hashed password
    phone = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to service tickets
    service_tickets = db.relationship('ServiceTicket', backref='customer', lazy=True)

class Mechanic(db.Model):
    """Mechanic model."""
    __tablename__ = 'mechanic'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    specialty = db.Column(db.String(100))
    hourly_rate = db.Column(db.Float)
    hire_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with service tickets
    service_tickets = db.relationship('ServiceTicket', secondary=mechanic_service_ticket, back_populates='mechanics')

class ServiceTicket(db.Model):
    """Service ticket model."""
    __tablename__ = 'service_ticket'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    vehicle_year = db.Column(db.Integer)
    vehicle_make = db.Column(db.String(50))
    vehicle_model = db.Column(db.String(50))
    vehicle_vin = db.Column(db.String(17))
    description = db.Column(db.Text, nullable=False)
    estimated_cost = db.Column(db.Float)
    actual_cost = db.Column(db.Float)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Many-to-many relationship with mechanics
    mechanics = db.relationship('Mechanic', secondary=mechanic_service_ticket, back_populates='service_tickets')
    
    # Many-to-many relationship with inventory parts
    inventory_parts = db.relationship('Inventory', secondary=inventory_service_ticket, back_populates='service_tickets')

class Inventory(db.Model):
    """Inventory model for parts."""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Many-to-many relationship with service tickets
    service_tickets = db.relationship('ServiceTicket', secondary=inventory_service_ticket, back_populates='inventory_parts')