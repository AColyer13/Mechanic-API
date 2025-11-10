"""Extensions module for initializing Flask extensions."""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()