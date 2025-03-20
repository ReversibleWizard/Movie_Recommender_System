from db_handler import db
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class MovieRecommender:
    def __init__(self):
        self.movies = pd.DataFrame(db.fetch_movies())
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.movie_matrix = None

    def train_model(self):
        if self.movies.empty:
            print("❌ No movies found in database!")
            return

        # Ensure genres are converted to strings
        self.movies["genres"] = self.movies["genres"].apply(
            lambda x: " ".join(map(str, x)) if isinstance(x, list) else str(x))

        # Create searchable text for recommendation
        self.movies["searchable_text"] = (
                self.movies["title"].fillna("") + " " + self.movies["genres"].fillna("")
        )

        self.movie_matrix = self.vectorizer.fit_transform(self.movies["searchable_text"])
        print("✅ Movie recommendation model trained successfully!")

    def recommend_movies(self, user_query):
        """Recommend movies based on genres."""
        query_text = " ".join(user_query.get("genres", []))
        if not query_text:
            return {"error": "Provide genres!"}

        query_vector = self.vectorizer.transform([query_text])
        similarity_scores = cosine_similarity(query_vector, self.movie_matrix).flatten()
        self.movies["match_score"] = similarity_scores
        recommended_movies = self.movies.sort_values(by="match_score", ascending=False).head(5)[["title", "genres"]]
        return recommended_movies.to_dict(orient="records")

recommender = MovieRecommender()
