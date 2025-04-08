from flask import Flask
from routes.auth_routes import auth  # ← Absolute
from config import Config
from utils.database import init_db
from routes.auth_routes import auth  # Now this will work

app = Flask(__name__)
app.config.from_object(Config)

# Initialize DB
init_db(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix='/api/auth')

@app.route('/')
def home():
    return "PowerRent API is running!"


if __name__ == '__main__':
    app.run(debug=True)