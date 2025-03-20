from flask import Blueprint, request, jsonify
from movie_recommender import recommender
from auth import auth

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/recommend", methods=["POST"])
def recommend():
    user_query = request.json
    recommendations = recommender.recommend_movies(user_query)
    return jsonify({"recommendations": recommendations})

@api_blueprint.route("/register", methods=["POST"])
def register():
    data = request.json
    auth.register_user(data["username"], data["password"])
    return jsonify({"message": "User registered successfully!"})

@api_blueprint.route("/login", methods=["POST"])
def login():
    """User login route - Returns JWT token on success."""
    data = request.json  # Get JSON data from request

    # ✅ Validate input
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Missing 'username' or 'password' in request"}), 400

    username = data["username"]
    password = data["password"]

    # ✅ Authenticate user
    token = auth.login_user(username, password)

    if token:
        return jsonify({"message": "Login successful", "token": token})  # ✅ Send token in response
    else:
        return jsonify({"error": "Invalid username or password"}), 401  # 401 Unauthorized
