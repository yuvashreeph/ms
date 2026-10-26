from flask import Flask, request, jsonify
app = Flask(__name__)

@app.get("/")
def home():
    return jsonify(message="Checkout Service")

@app.get("/health")
def health():
    return jsonify(status="healthy", service="checkout")

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
