import jwt
import datetime
import os
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
from db_handler import db

# Load environment variables from .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")  # Fallback if .env is missing


class AuthHandler:
    def generate_token(self, username):
        """Generate JWT token for authenticated users"""
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def verify_token(self, token):
        """Verify JWT token and extract user data"""
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return decoded["username"]
        except jwt.ExpiredSignatureError:
            return None  # Token expired
        except jwt.InvalidTokenError:
            return None  # Invalid token

    def authenticate_user(self, username, password):
        """Mock authentication function (Replace with DB check)"""
        users = {"admin": "password"}  # Replace with DB lookup
        return username if username in users and users[username] == password else None


auth = AuthHandler()


def auth_required(func):
    """Decorator to ensure the user is authenticated."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"error": "Unauthorized! Token is missing."}), 401

        try:
            token = token.split("Bearer ")[1]  # Extract the actual token
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = decoded_token["username"]

            # ✅ Ensure we return a dictionary, not just a string
            user = db.users_collection.find_one({"username": username}, {"_id": 0, "password": 0})

            if not user:
                return jsonify({"error": "Invalid token. User not found!"}), 401

            return func(user, *args, **kwargs)  # Pass user dictionary, not just username

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401
        except Exception as e:
            return jsonify({"error": f"Authentication error: {str(e)}"}), 401

    return wrapper