from flask import Flask
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

@app.route("/")
def home():
    return "Application running successfully"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)