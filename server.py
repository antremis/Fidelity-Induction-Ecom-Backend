from flask import Flask, request, jsonify
from flask_cors import CORS
import models.AuthModel as AuthModel
import models.CartModel as CartModel
import models.ProductTableModel as ProductTableModel
import models.ReviewModel as ReviewModel
import models.TLogModel as TLogModel
import models.TPLogsModel as TPLogsModel
import models.UserModel as UserModel
from config import Base, engine, session
from decorators import loginRequired

app = Flask(__name__)
CORS(app)

@app.route("/api/auth", methods=["GET", "PUT", "POST"])
@loginRequired
def auth():
    if request.method == "GET":
        # print(request.uid)
        users = AuthModel.getUsers(session)
        return jsonify({"mssg": "success", "data":users})
    if request.method == "PUT":
        data = request.get_json(force=True)
        username = data.get("username")
        password = data.get("password")
        uid = AuthModel.createUser(session, username, password)
        return jsonify({"mssg": "success", "data":uid})
    elif request.method == "POST":
        body = request.get_json(force=True)
        username=body.get("username")
        password=body.get("password")
        uid = AuthModel.checkUser(session, username, password)
        return jsonify({"mssg":"success", "data": AuthModel.createJWT(uid)})

@app.route("/api/auth/<id>", methods=["DELETE"])
def get(id):
    if request.method == "DELETE":
        result = AuthModel.deleteUser(session, id)
        return jsonify({"mssg":"success"})

@app.route("/api/product", methods=["GET", "POST"])
def product():
    if request.method == "GET":
        # Get all rows from products table using sqlalchemy functions
        id="1"
        all_products = ProductTableModel.displayAllProducts(session, id)
        products_list = []
        for product in all_products:
            products_list.append({
                "p_id": product.p_id,
                "name": product.name,
                "cost": product.cost,
                "tag": product.tag,
                "img": product.img,
                "des": product.des,
                "s_id": product.s_id
            })
        return jsonify({"products": products_list})
    elif request.method == "POST":
        # Get create/insert row using sqlalchemy functions
        data = request.get_json()    #parse this JSON data and convert it into a Python dictionary
        p_id = data.get('p_id')
        name = data.get('name')
        cost = data.get('cost')
        tag = data.get('tag')
        img = data.get('img')
        des = data.get('des')
        s_id = data.get('s_id')
        new_id = ProductTableModel.addProduct(session, p_id, name, cost, tag, img, des, s_id)
        return jsonify({"message": "Product added successfully", "p_id": new_id})
    
@app.route("/api/products/:id",methods=["GET","PATCH","DELETE"])
def productById():
    if request.method == "GET":
        # Get 1 row from products table where products.id = id using sqlalchemy functions
        return jsonify({"mssg": "success"})
    elif request.method == "PATCH":
        # Update 1 row in products table where products.id = id using sqlalchemy functions
        return jsonify({"mssg":"success", "data": [1, 2, 3, 4, 5]})
    elif request.method == "DELETE":
        # Delete 1 row from products table where products.id = id using sqlalchemy functions
        return jsonify({"mssg": "success"})

    
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug = True)