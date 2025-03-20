import os
import pymongo
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

class DatabaseHandler:
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.db = self.client["movie_db"]
        self.movies_collection = self.db["movies"]
        self.users_collection = self.db["users"]
        self.history_collection = self.db["history"]

    def check_connection(self):
        """Check if the database is connected."""
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"❌ Database Connection Error: {e}")
            return False

    def count_movies(self):
        """Check the number of movies in the database."""
        return self.movies_collection.count_documents({})

    def insert_movie(self, movie_data):
        """Insert or update a movie record."""
        self.movies_collection.update_one({"id": movie_data["id"]}, {"$set": movie_data}, upsert=True)

    def fetch_movies(self):
        """Retrieve all movies from the database."""
        return list(self.movies_collection.find({}, {"_id": 0}))

db = DatabaseHandler()
