from db_handler import db
from werkzeug.security import generate_password_hash, check_password_hash

class Auth:
    def register_user(self, username, password):
        hashed_password = generate_password_hash(password)
        db.users_collection.insert_one({"username": username, "password": hashed_password})

    def login_user(self, username, password):
        user = db.users_collection.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            return True
        return False

auth = Auth()
