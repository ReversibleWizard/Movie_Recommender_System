from flask import Blueprint, request, jsonify
from auth import auth, auth_required
from db_handler import db
from movie_recommender import recommender
from fetch_movies import fetcher


class Routes:
    """Encapsulates all API routes in an object-oriented format."""

    def __init__(self):
        self.api_blueprint = Blueprint("api", __name__)
        self.setup_routes()

    def setup_routes(self):
        """Define all API routes."""

        @self.api_blueprint.route("/register", methods=["POST"])
        def register():
            """Registers a new user."""
            data = request.json
            if not data or "username" not in data or "password" not in data or "email" not in data:
                return jsonify({"error": "Username, password, and email are required!"}), 400

            result = db.create_user(data["username"], data["password"], data["email"])
            return jsonify(result)

        @self.api_blueprint.route("/login", methods=["POST"])
        def login():
            """User login - Returns JWT token on success."""
            data = request.json
            if "username" not in data or "password" not in data:
                return jsonify({"error": "Username and password are required!"}), 400

            user = db.authenticate_user(data["username"], data["password"])
            if not user:
                return jsonify({"error": "Invalid username or password!"}), 401

            token = auth.generate_token(data["username"])
            return jsonify({"message": "Login successful", "token": token})

        @self.api_blueprint.route("/profile", methods=["GET"])
        @auth_required
        def get_profile(user):
            """Returns user profile details (except password)."""
            profile = db.get_user_profile(user)
            return jsonify(profile) if profile else jsonify({"error": "User not found!"}), 404

        @self.api_blueprint.route("/update_profile", methods=["POST"])
        @auth_required
        def update_profile(user):
            """Update user's favorite genres or watchlist."""
            data = request.json
            db.update_user_preferences(user, data.get("favorite_genres"), data.get("watchlist"))
            return jsonify({"message": "Profile updated successfully!"})

        @self.api_blueprint.route("/fetch_movies", methods=["POST"])
        @auth_required
        def fetch_movies(user):
            """Fetch movies for a given actor (Requires JWT)."""
            data = request.json
            actor_name = data.get("actor", "").strip()

            if not actor_name:
                return jsonify({"error": "Actor name is required!"}), 400

            fetcher.fetch_and_store_movies(actor_name)
            return jsonify({"message": f"Movies for {actor_name} fetched successfully!"})

        @self.api_blueprint.route("/recommend", methods=["POST"])
        @auth_required
        def recommend(current_user):
            """Recommends movies based on user input and stores history."""
            user_query = request.json
            if not user_query:
                return jsonify({"error": "Invalid request format!"}), 400

            # ✅ Pass username to `recommend_movies()`
            recommendations = recommender.recommend_movies(user_query, current_user["username"])
            return jsonify(recommendations)

        @self.api_blueprint.route("/history", methods=["GET"])
        @auth_required
        def recommendation_history(current_user):
            """Retrieves the recommendation history for a user."""
            history = db.get_recommendation_history(current_user["username"])
            return jsonify(history)

        @self.api_blueprint.route("/check_db", methods=["GET"])
        def check_db():
            """Check if the database connection is working."""
            if db.check_connection():
                return jsonify({"message": "✅ Database is connected!"})
            return jsonify({"error": "❌ Database connection failed!"}), 500


# ✅ Instantiate the Routes class to create the blueprint
routes = Routes().api_blueprint
