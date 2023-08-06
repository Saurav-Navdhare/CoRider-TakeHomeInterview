from User import User
from flask import Flask
from flask_restful import Resource, Api, reqparse
import re
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
api = Api(app)

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

class UsersResource(Resource):
    def get(self):
        users = list(collection.find())
        users = [parse_object_id(user) for user in users]
        return users

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="Name is required")
        parser.add_argument("email", type=str, required=True, help="Email is required")
        parser.add_argument("password", type=str, required=True, help="Password is required")
        args = parser.parse_args()

        try:
            user = User(args["name"], args["email"], args["password"])
            user = user.to_dict()
        except Exception as e:
            return {"message": str(e) + " missing"}, 400

        # check if email is already in use
        existing_user = collection.find_one({"email": user["email"]})
        if existing_user:
            return {"message": "Email already in use"}, 400

        user_id = collection.insert_one(user).inserted_id
        return {"message": "User created successfully", "user_id": str(user_id)}, 201


class UserResource(Resource):
    def get(self, user_id):
        try:
            user = collection.find_one({"_id": ObjectId(user_id)})
            if user:
                user = parse_object_id(user)
                return user
            else:
                return {"message": "User not found"}, 404
        except Exception as e:
            return {"message": "Invalid User ID"}, 400

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str)
        args = parser.parse_args()

        if "password" in args and args["password"]:
            args["password"] = args["password"].strip()

            if len(args["password"]) < 6 or " " in args["password"]:
                return {"message": "Password must be at least 6 characters and cannot contain spaces"}, 400
            args["password"] = User.hash_password(args["password"])

        if "email" in args and args["email"]:
            args["email"] = args["email"].strip()
            # check if email is valid
            if not re.match(r"[^@]+@[^@]+\.[^@]+", args["email"]) or " " in args["email"]:
                return {"message": "Invalid email"}, 400
            # check if email is already in use
            existing_user = collection.find_one({"email": args["email"]})
            if existing_user:
                return {"message": "Email already in use"}, 400

        if "name" in args and args["name"]:
            args["name"] = args["name"].strip()
            if len(args["name"]) == 0:
                return {"message": "Name cannot be empty"}, 400

        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": args})
        if result.modified_count == 1:
            return {"message": "User updated successfully"}, 200
        else:
            return {"message": "User not found"}, 404

    def delete(self, user_id):
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 1:
            return {"message": "User deleted successfully"}, 200
        else:
            return {"message": "User not found"}, 404

# Your existing User class goes here
# ...

api.add_resource(UsersResource, "/users")
api.add_resource(UserResource, "/users/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
