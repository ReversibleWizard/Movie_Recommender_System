import os
import pymongo
import bcrypt
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")


class DatabaseHandler:
    def __init__(self):
        """Initialize the database connection."""
        try:
            self.client = pymongo.MongoClient(MONGO_URI)
            self.db = self.client["movie_db"]
            self.movies_collection = self.db["movies"]
            self.users_collection = self.db["users"]
            self.history_collection = self.db["recommendation_history"]  # ✅ Ensure this is initialized
            print("✅ Database connected successfully!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")

    def check_connection(self):
        """Check if the database is connected properly."""
        try:
            self.client.server_info()  # This will raise an error if the DB is not connected
            return {"status": "Database connected successfully!"}
        except Exception as e:
            return {"status": f"Database connection error: {e}"}

    def create_user(self, username, password, email):
        """Creates a new user with hashed password."""
        if self.users_collection.find_one({"username": username}):
            return {"error": "Username already exists!"}

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        user_data = {
            "username": username,
            "password": hashed_password,
            "email": email
        }

        self.users_collection.insert_one(user_data)
        return {"message": "User registered successfully!"}

    def authenticate_user(self, username, password):
        """Authenticates a user by checking their credentials."""
        user = self.users_collection.find_one({"username": username})

        if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            return None  # Invalid login

        return user  # Valid user

    def store_recommendation(self, username, query, recommendations):
        """Stores the user's recommendation history."""
        if not hasattr(self, "history_collection"):
            self.history_collection = self.db["recommendation_history"]  # ✅ Ensure it's set before use

        history_entry = {
            "username": username,
            "query": query,
            "recommendations": recommendations,
            "timestamp": datetime.utcnow()
        }
        self.history_collection.insert_one(history_entry)
        print(f"✅ Stored recommendation history for {username}")

    def get_recommendation_history(self, username):
        """Retrieves the recommendation history of a user."""
        if not hasattr(self, "history_collection"):
            self.history_collection = self.db["recommendation_history"]  # ✅ Ensure it's set before use

        history = list(self.history_collection.find({"username": username}, {"_id": 0}))
        return history if history else {"message": "No recommendation history found!"}

    def fetch_movies(self):
        """Retrieve all movies from the database."""
        return list(self.movies_collection.find({}, {"_id": 0}))  # Exclude MongoDB `_id`

db = DatabaseHandler()
