# Movie Recommendation System

## Overview
The **Movie Recommendation System** is a Flask-based web application that suggests movies based on user preferences, including genres, actors, and directors. It fetches movie data from **The Movie Database (TMDb) API** and stores it in **MongoDB**. The recommendation engine uses **TF-IDF vectorization** and **cosine similarity** for movie matching.

## Features
- **Movie Recommendations** based on genres, actors, and directors.
- **User Authentication** using JWT for secure access.
- **MongoDB Integration** for storing movie and user data.
- **API Endpoints** for fetching movies, recommendations, and tracking history.
- **Machine Learning Model** trained on fetched movie data.

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** MongoDB (via PyMongo)
- **Machine Learning:** Scikit-learn (TF-IDF, Cosine Similarity)
- **API Integration:** TMDb API
- **Authentication:** JWT-based authentication
- **Containerization:** Docker (optional)

---

## Machine Learning Algorithms Used

### 1. **TF-IDF Vectorization**
TF-IDF (**Term Frequency-Inverse Document Frequency**) is a statistical measure used to evaluate how important a word is to a document relative to a collection of documents. It helps in understanding the significance of words when analyzing text data.
- **Term Frequency (TF):** Measures how frequently a word appears in a document.
- **Inverse Document Frequency (IDF):** Weighs words based on their rarity across all documents.
- In this system, TF-IDF is applied to movie metadata (title, overview, genres, actors, director) to convert text into numerical representations.

### 2. **Cosine Similarity**
Cosine similarity measures the similarity between two vectors based on the cosine of the angle between them.
- If two vectors are perfectly aligned, their cosine similarity is **1** (i.e., they are identical).
- If two vectors are completely different, their cosine similarity is **0**.
- In this project, cosine similarity is used to find movies with the most similar metadata representations.

#### **How It Works in the Project:**
1. Convert movie metadata (title, genres, actors, director, and overview) into a numerical format using **TF-IDF Vectorization**.
2. Compute the **cosine similarity** between the input query and all available movies.
3. Retrieve the top `N` movies with the highest similarity scores as recommendations.

---

## Installation & Setup

### 1. Clone the Repository
```sh
 git clone https://github.com/your-username/movie-recommendation-system.git
 cd movie-recommendation-system
```

### 2. Create a Virtual Environment
```sh
 python -m venv venv
 source venv/bin/activate  # Mac/Linux
 venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
```sh
 pip install -r requirements.txt
```

### 4. Set Up MongoDB
#### **Using Local MongoDB**
1. Install MongoDB from [MongoDB Official Website](https://www.mongodb.com/try/download/community).
2. Start MongoDB Server:
   ```sh
   mongod --dbpath /path/to/data/db
   ```
3. Create a database named `movie_db` and collections:
   ```sh
   mongo
   use movie_db
   db.createCollection("movies")
   db.createCollection("users")
   db.createCollection("recommendation_history")
   ```

#### **Using MongoDB Atlas (Cloud Database)**
1. Create an account on [MongoDB Atlas](https://www.mongodb.com/atlas/database).
2. Create a new cluster and get the **connection string**.
3. Replace `MONGO_URI` in `.env` with:
   ```sh
   MONGO_URI=mongodb+srv://your_username:your_password@yourcluster.mongodb.net/movie_db
   ```

### 5. Configure Environment Variables
Create a `.env` file in the root directory and add:
```env
MONGO_URI=mongodb://localhost:27017/movie_db  # or MongoDB Atlas URI
TMDB_API_KEY=your_tmdb_api_key
SECRET_KEY=your_secret_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin_password
```

### 6. Run the Application
```sh
 python run.py
```
The API will start at `http://127.0.0.1:5000/`.

---

## API Endpoints
### 1. User Authentication
- **Register:** `POST /register`
  - Request Body: `{ "username": "user", "password": "pass", "email": "email@example.com" }`
  - Response: `{ "message": "User registered successfully!" }`

- **Login:** `POST /login`
  - Request Body: `{ "username": "user", "password": "pass" }`
  - Response: `{ "message": "Login successful", "token": "jwt_token" }`

### 2. Movie Recommendations
- **Recommend Movies:** `POST /recommend`
  - Request Body: `{ "genres": ["Action", "Sci-Fi"], "actor": "Leonardo DiCaprio", "director": "Christopher Nolan" }`
  - Response: `{ "recommendations": [{ "title": "Movie Name", "genres": ["Action"] }] }`

- **Fetch Movies by Actor:** `POST /fetch_movies`
  - Request Body: `{ "actor": "Tom Hanks" }`
  - Response: `{ "message": "Movies for Tom Hanks fetched successfully!" }`

### 3. User History
- **View Recommendation History:** `GET /history`
  - Response: `{ "history": [{ "query": {"genres": ["Drama"]}, "movies": [...] }] }`

---

## Project Structure
```
📂 movie-recommendation-system
│── app.py            # Main Flask app
│── run.py            # Starts the application
│── routes.py         # API routes
│── auth.py           # User authentication
│── db_handler.py     # Database connection
│── fetch_movies.py   # Fetches movies from TMDb API
│── movie_recommender.py  # Recommendation engine
│── .env              # Environment variables
│── requirements.txt  # Dependencies
```

---

## License
This project is licensed under the MIT License.

## Author
Sayak Mitra Majumder
