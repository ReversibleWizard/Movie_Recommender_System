import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from db_handler import db
from fetch_movies import fetcher


class MovieRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.movie_matrix = None
        self.movies = pd.DataFrame()
        self.train_model()

    def fetch_and_train(self, actor=None, director=None, genres=None):
        """Automatically fetch movies and train the model if necessary."""
        if actor:
            fetcher.fetch_and_store_movies(actor_name=actor)
        if director:
            fetcher.fetch_and_store_movies(director_name=director)

        self.train_model()

    def train_model(self):
        """Trains the recommendation model only if new movies are added."""
        new_movies = pd.DataFrame(db.fetch_movies())

        if new_movies.empty:
            print("❌ No movies found in database! Fetching is required.")
            return

        if self.movies.equals(new_movies):
            print("✅ Model is already trained with the latest data.")
            return

        self.movies = new_movies
        print(f"🧠 Training model with {len(self.movies)} movies...")

        # ✅ Convert lists to strings before concatenation
        self.movies["genres"] = self.movies["genres"].apply(lambda x: " ".join(x) if isinstance(x, list) else str(x))
        self.movies["actors"] = self.movies["actors"].apply(lambda x: " ".join(x) if isinstance(x, list) else str(x))

        # ✅ Ensure rating and popularity exist
        if "rating" not in self.movies:
            self.movies["rating"] = 0  # Default rating
        if "popularity" not in self.movies:
            self.movies["popularity"] = 0  # Default popularity

        self.movies["searchable_text"] = (
                self.movies["title"].fillna("") + " " +
                self.movies["overview"].fillna("") + " " +
                self.movies["genres"].fillna("") + " " +
                self.movies["actors"].fillna("") + " " +
                self.movies["director"].fillna("")
        )

        self.movie_matrix = self.vectorizer.fit_transform(self.movies["searchable_text"])
        print("✅ Movie recommendation model trained successfully!")

    def recommend_movies(self, user_query, username):
        """Automatically fetch and train if needed before recommending movies."""
        actor = user_query.get("actor", "").strip()
        director = user_query.get("director", "").strip()
        genres = user_query.get("genres", [])

        # Auto-fetch and train if any key parameter is provided
        if actor or director or genres:
            self.fetch_and_train(actor, director, genres)

        if self.movies.empty or self.movie_matrix is None:
            return {"error": "Recommendation model is not trained. Please fetch movies first!"}

        # Construct the query string based on available parameters
        query_text = " ".join(filter(None, [
            actor,
            " ".join(genres) if isinstance(genres, list) else genres,
            director
        ])).strip()

        if not query_text:
            return {"error": "Provide at least an actor, genre, or director!"}

        query_vector = self.vectorizer.transform([query_text])
        similarity_scores = cosine_similarity(query_vector, self.movie_matrix).flatten()
        self.movies["match_score"] = similarity_scores

        # ✅ Sort by match_score first, then by rating (descending), then by popularity (descending)
        recommended_movies = (
            self.movies.sort_values(by=["match_score", "rating", "popularity"], ascending=[False, False, False])
            .head(10)[["title", "actors", "director", "genres", "rating", "popularity", "match_score"]]
            .to_dict(orient="records")
        )

        # ✅ Store the recommendation in history
        db.store_recommendation(username, user_query, recommended_movies)

        return {"recommendations": recommended_movies if recommended_movies else "No matching movies found!"}


recommender = MovieRecommender()
