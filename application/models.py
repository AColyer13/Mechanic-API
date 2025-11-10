from application.extensions import db
from datetime import datetime

# Association table for many-to-many relationship between service tickets and mechanics
service_ticket_mechanics = db.Table('service_ticket_mechanics',
    db.Column('service_ticket_id', db.Integer, db.ForeignKey('service_ticket.id'), primary_key=True),
    db.Column('mechanic_id', db.Integer, db.ForeignKey('mechanic.id'), primary_key=True)
)

class Customer(db.Model):
    """Customer model for the mechanic shop"""
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to service tickets
    service_tickets = db.relationship('ServiceTicket', back_populates='customer', lazy=True)
    
    def __repr__(self):
        return f'<Customer {self.first_name} {self.last_name}>'

class Mechanic(db.Model):
    """Mechanic model for the mechanic shop"""
    __tablename__ = 'mechanic'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    specialty = db.Column(db.String(100), nullable=True)
    hourly_rate = db.Column(db.Float, nullable=True)
    hire_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Many-to-many relationship with service tickets
    service_tickets = db.relationship('ServiceTicket', 
                                    secondary=service_ticket_mechanics, 
                                    back_populates='mechanics',
                                    lazy='dynamic')
    
    def __repr__(self):
        return f'<Mechanic {self.first_name} {self.last_name}>'

class ServiceTicket(db.Model):
    """Service ticket model for tracking repair jobs"""
    __tablename__ = 'service_ticket'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    vehicle_year = db.Column(db.Integer, nullable=True)
    vehicle_make = db.Column(db.String(50), nullable=True)
    vehicle_model = db.Column(db.String(50), nullable=True)
    vehicle_vin = db.Column(db.String(17), nullable=True)
    description = db.Column(db.Text, nullable=False)
    estimated_cost = db.Column(db.Float, nullable=True)
    actual_cost = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='Open', nullable=False)  # Open, In Progress, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    customer = db.relationship('Customer', back_populates='service_tickets')
    mechanics = db.relationship('Mechanic', 
                               secondary=service_ticket_mechanics, 
                               back_populates='service_tickets',
                               lazy='dynamic')
    
    def __repr__(self):
        return f'<ServiceTicket {self.id} - {self.status}>'