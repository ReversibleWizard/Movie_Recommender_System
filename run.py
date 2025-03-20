from app import app
from db_handler import db
from fetch_movies import fetcher
from movie_recommender import recommender

if __name__ == "__main__":
    print("🚀 Starting Movie Recommendation System...")

    # Ensure database connection
    if db.check_connection():
        print("✅ Database connected successfully!")
    else:
        print("❌ Failed to connect to the database!")
        exit(1)

    # Fetch movies if database is empty
    if db.count_movies() == 0:
        print("📡 Fetching movies from TMDb API...")
        fetcher.fetch_and_store_movies()
    else:
        print("✅ Movies already exist in the database!")

    # Train the recommender model
    print("🧠 Training recommendation model...")
    recommender.train_model()

    # Start the Flask app
    print("🚀 Starting Flask API...")
    app.run(debug=True)
