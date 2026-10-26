from flask import Flask, request, jsonify
app = Flask(__name__)
cart = []

@app.get("/")
def home():
    return jsonify(message="Cart Service")

@app.get("/health")
def health():
    return jsonify(status="healthy", service="cart")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
