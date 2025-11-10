"""Application factory for creating Flask app instances."""

from flask import Flask
from config import config
from .extensions import db, ma, migrate


def create_app(config_name='development'):
    """Create and configure Flask application instance."""
    
    # Create Flask app
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they're registered with SQLAlchemy
    from . import models
    
    # Register blueprints
    from .blueprints.customer import customer_bp
    from .blueprints.mechanic import mechanic_bp
    from .blueprints.service_ticket import service_ticket_bp
    
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def index():
        return {
            'message': 'Welcome to Mechanic Shop API',
            'endpoints': {
                'customers': '/customers',
                'mechanics': '/mechanics',
                'service_tickets': '/service-tickets'
            }
        }
    
    return app