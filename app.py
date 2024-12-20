from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.order_routes import order_bp
from routes.product_routes import product_bp

load_dotenv()  # This will load variables from the .env file
app = Flask(__name__)
CORS(app)

# Configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = Config().SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = Config().SQLALCHEMY_TRACK_MODIFICATIONS
db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(order_bp, url_prefix="/orders")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if not using migrations
    app.run(debug=True)
