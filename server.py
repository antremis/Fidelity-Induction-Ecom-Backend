from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from config import session
import models.CartModel as CartModel
import models.ProductTableModel as ProductTableModel
import models.ReviewModel as ReviewModel
import models.TLogModel as TLogModel
import models.TPLogsModel as TPLogsModel
import models.UserModel as UserModel
from sqlalchemy.orm import sessionmaker
# from CartModel import addToCart, getCart, removeFromCart


load_dotenv()

app = Flask(__name__)
CORS(app)
carts = []

# Define a route to add a product to the cart
@app.route("/api/cart", methods=["POST"])

def addToCart():
    data = request.json
    u_id = data.get("u_id")
    p_id = data.get("p_id")
    qty = data.get("qty")

    if u_id is None or p_id is None or qty is None or qty < 1:
        return jsonify({"message": "Invalid request. Please provide u_id, p_id, and a quantity greater than 0."}), 400

    # Check if the same item is already in the cart
    for cart_item in carts:
        if cart_item["u_id"] == u_id and cart_item["p_id"] == p_id:
            cart_item["qty"] += qty
            return jsonify({"message": "Quantity updated in the cart successfully."})

    # If not found, create a new cart item and add it to the carts list
    cart_item = {"u_id": u_id, "p_id": p_id, "qty": qty}
    carts.append(cart_item)

    return jsonify({"message": "Product added to the cart successfully."})

# Define a route to get the cart for a user
@app.route("/api/cart/<int:u_id>", methods=["GET"])
def getCart(u_id):
    user_cart = [cart_item for cart_item in carts if cart_item["u_id"] == u_id]

    if user_cart:
        return jsonify({"cart": user_cart})

    return jsonify({"message": "Cart is empty."}), 404

# Define a route to remove a cart item
@app.route("/api/cart/<int:u_id>/<int:p_id>", methods=["DELETE"])
def removeFromCart(u_id, p_id):
    for cart_item in carts:
        if cart_item["u_id"] == u_id and cart_item["p_id"] == p_id:
            carts.remove(cart_item)
            return jsonify({"message": "Cart item removed from the cart successfully."})

    return jsonify({"message": "Cart item not found in the cart."}), 404

if __name__ == "__main__":
    app.run()

