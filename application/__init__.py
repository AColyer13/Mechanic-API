"""Application factory for creating Flask app instances."""

from flask import Flask
from config import config
from .extensions import db, ma, migrate, limiter, cache


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
    limiter.init_app(app)  # Initialize Flask-Limiter
    cache.init_app(app)    # Initialize Flask-Caching
    
    # Import models to ensure they're registered with SQLAlchemy
    from . import models
    
    # Register blueprints
    from .blueprints.customer import customer_bp
    from .blueprints.mechanic import mechanic_bp
    from .blueprints.service_ticket import service_ticket_bp
    from .blueprints.inventory import inventory_bp
    
    app.register_blueprint(customer_bp, url_prefix='/customers')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanics')
    app.register_blueprint(service_ticket_bp, url_prefix='/service-tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    
    # Create database tables with error handling
    with app.app_context():
        try:
            db.create_all()
            print("✓ Database tables created successfully")
        except Exception as e:
            print(f"⚠️  Database connection failed: {e}")
            print("📝 Please check your MySQL configuration:")
            print("   1. Ensure MySQL server is running")
            print("   2. Create database: CREATE DATABASE mechanicshopdata;")
            print("   3. Check MySQL root password")
            print("   4. Update .env file with correct DATABASE_URL")
            print("   5. Or uncomment SQLite fallback in .env")
    
    @app.route('/')
    def index():
        return {
            'message': 'Welcome to Mechanic Shop API',
            'endpoints': {
                'customers': '/customers',
                'mechanics': '/mechanics',
                'service_tickets': '/service-tickets',
                'inventory': '/inventory'
            },
            'database_status': 'Check console for database connection status'
        }
    
    return app