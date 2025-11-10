from application import create_app
import os

# Get configuration environment
config_name = os.environ.get('FLASK_ENV', 'development')

# Create the Flask app
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True)