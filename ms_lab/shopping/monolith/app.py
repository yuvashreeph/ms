from flask import Flask, request, jsonify

app = Flask(__name__)
cart = []

@app.get("/")
def home():
    return jsonify(
        application="Shopping App Monolith",
        services=["login", "cart", "checkout"]
    )

@app.get("/health")
def health():
    return jsonify(status="healthy", application="shopping-monolith")

@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    if data.get("username") == "admin" and data.get("password") == "1234":
        return jsonify(message="Login successful", username="admin"), 200
    return jsonify(message="Invalid credentials"), 401

@app.get("/cart")
def get_cart():
    return jsonify(cart=cart)

@app.post("/cart")
def add_to_cart():
    data = request.get_json(silent=True) or {}
    item, price = data.get("item"), data.get("price")
    if not isinstance(item, str) or not item.strip():
        return jsonify(error="item is required"), 400
    if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
        return jsonify(error="price must be a non-negative number"), 400
    product = {"item": item.strip(), "price": price}
    cart.append(product)
    return jsonify(message="Item added", product=product, cart=cart), 201

@app.post("/checkout")
def checkout():
    data = request.get_json(silent=True) or {}
    items = data.get("items")
    if not isinstance(items, list) or not items:
        return jsonify(error="items must be a non-empty list"), 400
    total = 0
    for product in items:
        if not isinstance(product, dict):
            return jsonify(error="each item must be an object"), 400
        price = product.get("price")
        if isinstance(price, bool) or not isinstance(price, (int, float)) or price < 0:
            return jsonify(error="each item needs a valid price"), 400
        total += price
    return jsonify(message="Checkout successful", items=items,
                   total=round(total, 2), order_status="confirmed"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
