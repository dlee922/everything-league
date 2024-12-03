# Initialize Flask app, MongoDB, and routes
from flask import Flask
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Flask App Factory
def create_app():
    app = Flask(__name__)
    CORS(app)
    # load environment variables
    load_dotenv()

    # mongodb connection
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise ValueError("MONGO_URI is not set in .env file")
    client = MongoClient(uri, server_api=ServerApi('1'))

    # check mongodb connection
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