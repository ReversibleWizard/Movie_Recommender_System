from app import app
from db_handler import db
from movie_recommender import recommender

if __name__ == "__main__":
    print("🚀 Starting Movie Recommendation System...")

    # Ensure database connection
    if db.check_connection():
        print("✅ Database connected successfully!")
    else:
        print("❌ Failed to connect to the database! Exiting...")
        exit(1)  # Stop the application if the database is not connected

    # Train the recommender model
    print("🧠 Training recommendation model...")
    recommender.train_model()

    # Start the Flask API
    print("🚀 Starting Flask API...")
    app.run(debug=True)
