"""Extensions module for initializing Flask extensions."""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Initialize extensions
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

# Initialize Flask-Limiter with remote address as key function
limiter = Limiter(key_func=get_remote_address)

# Initialize Flask-Caching with SimpleCache (in-memory caching)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})