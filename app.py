from application import create_app
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

# Get configuration environment
config_name = os.environ.get('FLASK_ENV', 'development')

# Create the Flask app
app = create_app(config_name)

# Initialize rate limiter with default limits
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Initialize cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

if __name__ == '__main__':
    app.run(debug=True)



