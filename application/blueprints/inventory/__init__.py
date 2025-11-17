"""Inventory blueprint initialization."""

from flask import Blueprint

inventory_bp = Blueprint('inventory', __name__)

# Import routes to register them with the blueprint
from . import routes
