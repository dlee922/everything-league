from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)
    # CORS(app)
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    # # Configure Flask extensions
    # bcrypt = Bcrypt(app)
    # jwt = JWTManager(app)

    # # Ensure critical configurations are set
    # # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    # if not app.config['JWT_SECRET_KEY']:
    #     raise ValueError("JWT_SECRET_KEY is not set in .env file")

    # MongoDB connection
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise ValueError("MONGO_URI is not set in .env file")
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Test MongoDB connection
    try:
        client.admin.command('ping')
        print("Connected to MongoDB!")
    except Exception as e:
        raise Exception(f"Failed to connect to MongoDB: {e}")

    app.mongo_client = client

    # Register Blueprints
    from app.routes import register_routes
    register_routes(app)

    return app
