"""Service Ticket blueprint initialization."""

from flask import Blueprint

# Create the service ticket blueprint
service_ticket_bp = Blueprint('service_ticket', __name__)

# Import routes to register them with the blueprint
from . import routes