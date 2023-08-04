from flask import Flask, request, jsonify
from pymongo import MongoClient
from User import User
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import re

load_dotenv()


app = Flask(__name__)

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = "users"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


# Helper function to convert ObjectId to string
def parse_object_id(user):
    user["_id"] = str(user["_id"])
    return user


# REST API endpoints

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Users API"})

@app.route("/users", methods=["GET"])
def get_all_users():
    users = list(collection.find())
    users = [parse_object_id(user) for user in users]
    return jsonify(users)


@app.route("/users/<string:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user = parse_object_id(user)
            return jsonify(user)
        else:
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"message": "Invalid User ID"}), 400

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        user = User(data["name"], data["email"], data["password"])
        user = user.to_dict()
    except Exception as e:
        return jsonify({"message": str(e)+" missing"}), 400  
    # check if email is already in use
    existing_user = collection.find_one({"email": user["email"]})
    if(existing_user):
        return jsonify({"message": "Email already in use"}), 400  
    user_id = collection.insert_one(user).inserted_id
    return jsonify({"message": "User created successfully", "user_id": str(user_id)}), 201


@app.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    if("password" in data):
        data["password"] = data["password"].strip()

        if(len(data["password"]) < 6 or " " in data["password"]):
            return jsonify({"message": "Password must be at least 6 characters and cannot contain spaces"}), 400
        data["password"] = User.hash_password(data["password"])

    if("email" in data):
        data["email"] = data["email"].strip()
        # check if email is valid
        if(not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]) or " " in data["email"]):
            return jsonify({"message": "Invalid email"}), 400
        # check if email is already in use
        existing_user = collection.find_one({"email": data["email"]})
        if(existing_user):
            return jsonify({"message": "Email already in use"}), 400
        
    if("name" in data):
        data["name"] = data["name"].strip()
        if(len(data["name"])==0):
            return jsonify({"message": "Name cannot be empty"}), 400
        
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    if result.modified_count == 1:
        return jsonify({"message": "User updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
