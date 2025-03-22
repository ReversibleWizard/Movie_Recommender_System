import os
import requests
from db_handler import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

class MovieFetcher:
    def __init__(self):
        self.genre_mapping = self.get_genre_mapping()

    def get_genre_mapping(self):
        """Fetches genre mappings from TMDB API."""
        url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url).json()
        return {genre["id"]: genre["name"] for genre in response.get("genres", [])}

    def fetch_movies_by_actor(self, actor_name):
        """Fetches movies where the given actor appeared."""
        url = f"https://api.themoviedb.org/3/search/person?api_key={TMDB_API_KEY}&query={actor_name}"
        response = requests.get(url).json()

        if not response.get("results"):
            return []

        actor_id = response["results"][0]["id"]
        movie_url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_cast={actor_id}"
        movies = requests.get(movie_url).json().get("results", [])

        return movies

    def fetch_movies_by_director(self, director_name):
        """Fetches movies where the given director worked."""
        url = f"https://api.themoviedb.org/3/search/person?api_key={TMDB_API_KEY}&query={director_name}"
        response = requests.get(url).json()

        if not response.get("results"):
            return []

        director_id = response["results"][0]["id"]
        movie_url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_crew={director_id}"
        movies = requests.get(movie_url).json().get("results", [])

        return movies

    def fetch_movie_details(self, movie_id):
        """Fetches detailed information (actors, director, rating, popularity) using the TMDB API."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits"
        response = requests.get(url).json()

        # Extract actors (Top 5)
        actors = [cast["name"] for cast in response.get("credits", {}).get("cast", [])[:5]]

        # Extract director
        director = "Unknown"
        for crew_member in response.get("credits", {}).get("crew", []):
            if crew_member["job"] == "Director":
                director = crew_member["name"]
                break

        # Extract rating & popularity (Fix: Ensure correct key)
        rating = response.get("vote_average", 0)  # Ensure rating is fetched correctly
        popularity = response.get("popularity", 0)  # Ensure popularity is fetched correctly

        print(f"🎬 Movie: {response.get('title', 'Unknown')}, Rating: {rating}, Popularity: {popularity}")

        return actors, director, rating, popularity

    def fetch_and_store_movies(self, actor_name=None, director_name=None):
        """Fetch and store movies automatically for an actor or a director."""

        if actor_name:
            existing_movies = list(db.movies_collection.find({"actors": actor_name}, {"_id": 0}))
            if existing_movies:
                print(f"✅ Movies for actor {actor_name} already exist in the database.")
                return {"message": f"Movies for actor {actor_name} already exist!"}
            movies = self.fetch_movies_by_actor(actor_name)

        elif director_name:
            existing_movies = list(db.movies_collection.find({"director": director_name}, {"_id": 0}))
            if existing_movies:
                print(f"✅ Movies for director {director_name} already exist in the database.")
                return {"message": f"Movies for director {director_name} already exist!"}
            movies = self.fetch_movies_by_director(director_name)

        else:
            return {"error": "Provide at least an actor or a director name!"}

        if not movies:
            print(f"❌ No movies found for {actor_name or director_name}")
            return {"error": f"No movies found for {actor_name or director_name}"}

        formatted_movies = []
        for movie in movies:
            movie_id = movie.get("id")
            actors, director, rating, popularity = self.fetch_movie_details(movie_id)  # Fetch full details

            formatted_movies.append({
                "id": movie_id,
                "title": movie.get("title"),
                "overview": movie.get("overview", ""),
                "release_year": movie.get("release_date", "")[:4],
                "genres": [self.genre_mapping.get(genre_id, "Unknown") for genre_id in movie.get("genre_ids", [])],
                "actors": actors,  # List of actors
                "director": director,  # Single director name
                "rating": rating,  # Movie rating
                "popularity": popularity  # Movie popularity
            })

        # Insert movies into MongoDB
        db.movies_collection.insert_many(formatted_movies)
        print(f"✅ Stored {len(formatted_movies)} movies for {actor_name or director_name}")

        return {"message": f"Movies for {actor_name or director_name} stored successfully!"}

fetcher = MovieFetcher()
