import os
import requests
from db_handler import db
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

class MovieFetcher:
    def fetch_and_store_movies(self, pages=5):
        """Fetch movies from multiple pages of the TMDb API and store them in the database."""
        new_movies = 0

        for page in range(1, pages + 1):
            print(f"📡 Fetching page {page} from TMDb API...")
            url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&page={page}"
            response = requests.get(url).json()

            movies = response.get("results", [])
            for movie in movies:
                db.insert_movie({
                    "id": movie["id"],
                    "title": movie["title"],
                    "genres": [g["name"] for g in movie.get("genre_ids", [])],
                    "release_year": movie.get("release_date", "").split("-")[0] if "release_date" in movie else "Unknown"
                })
                new_movies += 1

        print(f"✅ {new_movies} movies added to the database!")

fetcher = MovieFetcher()
