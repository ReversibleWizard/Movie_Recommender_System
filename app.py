from flask import Flask
from routes import routes  # ✅ Importing 'routes' object from the Routes class

app = Flask(__name__)
app.register_blueprint(routes)  # ✅ Registering Blueprint

if __name__ == "__main__":
    app.run(debug=True)
