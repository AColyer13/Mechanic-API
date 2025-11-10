"""Mechanic blueprint initialization."""

from flask import Blueprint

# Create the mechanic blueprint
mechanic_bp = Blueprint('mechanic', __name__)

# Import routes to register them with the blueprint
from . import routes