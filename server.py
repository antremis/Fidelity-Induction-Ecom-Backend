from flask import Flask, request, jsonify
from flask_cors import CORS
import models.CartModel as CartModel
import models.ProductTableModel as ProductTableModel
import models.ReviewModel as ReviewModel
import models.TLogModel as TLogModel
import models.TPLogsModel as TPLogsModel
import models.UserModel as UserModel
from config import Base, engine, session

app = Flask(__name__)
CORS(app)

@app.route("/api/test")
def test():
    # Template function
    if request.method == "GET":
        TPLogsModel.insert(session, 1, 2)
        return jsonify({"mssg": "success"})
    elif request.method == "POST":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})

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
        new_id = addProduct(session, p_id, name, cost, tag, img, des, s_id)
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

    
@app.route("/api/logs")
def logs():
    if request.method == "GET":
        return jsonify({"mssg":"success"})
    elif request.method == "POST":
        pid_quantity_list = [(1,10), (2,15), (3,5)]
        id = TPLogsModel.generateRandomTidAndInsert(session,pid_quantity_list)
        return jsonify({"mmsg":"success", "data": id})
    

@app.route("/api/logs/<t_id>")
def transactionById(t_id):
    if request.method == "GET":
       # t_id = "6cac23b8-8d68-4815-94ab-e14a906a3ed8"
        result = TPLogsModel.getPidQuantityForTid(session,t_id)
        print(result)
        return jsonify({"mmsg":"success", "data": result.list()})
    
    if request.method == "PATCH":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})
    
    if request.method == "DELETE":
       # t_id = "d263ae6d-d428-4bd9-82dc-7c298ef6ef6a"
        delete_tid = TPLogsModel.deleteTransaction(session,t_id)
        return jsonify({"mmsg":"success", "data": delete_tid})
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug = True)
