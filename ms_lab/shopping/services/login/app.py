from flask import Flask, request, jsonify
app = Flask(__name__)

@app.get("/")
def home():
    return jsonify(message="Login Service")

@app.get("/health")
def health():
    return jsonify(status="healthy", service="login")

@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    if data.get("username") == "admin" and data.get("password") == "1234":
        return jsonify(message="Login successful", username="admin"), 200
    return jsonify(message="Invalid credentials"), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
