"""Customer blueprint initialization."""

from flask import Blueprint

# Create the customer blueprint
customer_bp = Blueprint('customer', __name__)

# Import routes to register them with the blueprint
from . import routes