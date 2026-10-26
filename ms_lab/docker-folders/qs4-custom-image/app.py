
from flask import Flask
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "mydatabase")

@app.route("/")
def home():
    return "Application running successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
