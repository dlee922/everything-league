# Authentication logic
import datetime
from flask import current_app, jsonify, request
from flask_jwt_extended import create_access_token

def register_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # MongoDB Collection
    mongo_collection = current_app.mongo_client["everything-league"]["users"]

    # Check if user already exists
    if mongo_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    # Save user to the database
    mongo_collection.insert_one({
        "username": username,
        "password": password,
        "created_at": datetime.utcnow(),
    })

    return jsonify({"message": "User registered successfully"}), 201

def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Validate input
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # MongoDB Collection
    mongo_collection = current_app.mongo_client["everything-league"]["users"]

    # Find user in the database
    user = mongo_collection.find_one({"username": username})
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    # Generate a JWT
    access_token = create_access_token(identity={"username": username})
    return jsonify({"access_token": access_token}), 200
