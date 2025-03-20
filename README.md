# Movie Recommendation System

## Overview
The **Movie Recommendation System** is a Flask-based web application that suggests movies to users based on their preferred genres. The system utilizes **TF-IDF vectorization** and **cosine similarity** to recommend similar movies from a database populated with data from **The Movie Database (TMDb) API**.

## Features
- **Movie Recommendation:** Provides movie suggestions based on genre similarity.
- **User Authentication:** Secure user registration and login.
- **API Integration:** Fetches movie data from TMDb API and stores it in MongoDB.
- **Database Management:** Stores user and movie data efficiently.
- **Machine Learning Model:** Uses NLP techniques for similarity analysis.

## Tech Stack
- **Backend:** Flask (Python)
- **Database:** MongoDB (via PyMongo)
- **Machine Learning:** Scikit-learn (TF-IDF, Cosine Similarity)
- **API Integration:** TMDb API
- **Authentication:** Werkzeug (Password Hashing)

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

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add:
```env
MONGO_URI=mongodb://localhost:27017/movie_db
TMDB_API_KEY=your_tmdb_api_key
SECRET_KEY=your_secret_key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin_password
```

### 5. Run the Application
```sh
 python run.py
```
The API will start at `http://127.0.0.1:5000/`.

## API Endpoints
### 1. User Authentication
- **Register:** `POST /register`
  - Request Body: `{ "username": "user", "password": "pass" }`
  - Response: `{ "message": "User registered successfully!" }`

- **Login:** `POST /login`
  - Request Body: `{ "username": "user", "password": "pass" }`
  - Response: `{ "message": "Login successful", "token": "jwt_token" }`

### 2. Movie Recommendations
- **Recommend Movies:** `POST /recommend`
  - Request Body: `{ "genres": ["Action", "Sci-Fi"] }`
  - Response: `{ "recommendations": [{ "title": "Movie Name", "genres": ["Action"] }] }`

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

## License
This project is licensed under the MIT License.

## Author
[Your Name]

