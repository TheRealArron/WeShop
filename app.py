from flask import Flask, render_template, request, jsonify, session
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'your_secret_key'

PRODUCTS = [
    {"id": 1, "name": "Banana", "price": 0.99, "emoji": "🍌", "color": "#fff176"},
    {"id": 2, "name": "Strawberry", "price": 2.99, "emoji": "🍓", "color": "#ef5350"},
    {"id": 3, "name": "Watermelon", "price": 4.99, "emoji": "🍉", "color": "#81c784"},
    {"id": 4, "name": "Orange", "price": 1.99, "emoji": "🍊", "color": "#ffb74d"},
    {"id": 5, "name": "Grapes", "price": 3.49, "emoji": "🍇", "color": "#9575cd"},
    {"id": 6, "name": "Apple", "price": 1.49, "emoji": "🍎", "color": "#e57373"}
]

@app.route('/')
def index():
    return render_template("index.html", products=PRODUCTS)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.get_json()
    cart = session.get('cart', [])

    for i in cart:
        if i['id'] == item['id']:
            i['quantity'] += 1
            break
    else:
        item['quantity'] = 1
        cart.append(item)

    session['cart'] = cart
    return jsonify(success=True)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = request.get_json().get('cart', [])
    session['cart'] = cart
    return jsonify(success=True)

@app.route('/get_cart')
def get_cart():
    return jsonify(cart=session.get('cart', []))

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    cart = session.get('cart', [])

    if not cart:
        return jsonify(success=False, error="Cart is empty.")

    if not data.get("payment_info"):
        return jsonify(success=False, error="Payment information is missing.")

    total = sum(item['price'] * item['quantity'] for item in cart)
    order_id = str(uuid4())[:8]
    session.pop('cart', None)

    return jsonify(success=True, message="Payment successful!", order_id=order_id, total=round(total, 2))

if __name__ == '__main__':
    app.run(debug=True)
