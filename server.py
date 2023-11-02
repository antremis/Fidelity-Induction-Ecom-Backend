from flask import Flask, request, jsonify
from flask_cors import CORS
import models.CartModel as CartModel
import models.ProductTableModel as ProductTableModel
import models.ReviewModel as ReviewModel
import models.TLogModel as TLogModel
import models.TPLogsModel as TPLogsModel
import models.UserModel as UserModel
from sqlalchemy.orm import sessionmaker
from config import Base, engine,session

app = Flask(__name__)
CORS(app)

@app.route("/api/test")
def test():
    # Template function
    if request.method == "GET":
        return jsonify({"mssg": "success"})
    elif request.method == "POST":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})

@app.route("/api/product", methods=["GET", "POST"])
def product():
    if request.method == "GET":
        # Get all rows from products table using sqlalchemy functions
        id="1"
        all_products = ProductTableModel.displayAllProducts(session)
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
        #body=request.get_json(force=True)
        
        data = request.get_json(force=True)    #parse this JSON data and convert it into a Python dictionary
        p_id = data.get('p_id')
        name = data.get('name')
        cost = data.get('cost')
        tag = data.get('tag')
        img = data.get('img')
        des = data.get('des')
        s_id = data.get('s_id')
        new_id = ProductTableModel.addProduct(session, p_id, name, cost, tag, img, des, s_id)
        return jsonify({"message": "Product added successfully", "p_id": new_id})
    
@app.route("/api/products/<p_id>",methods=["GET","PATCH","DELETE"])
def productById(p_id):
    if request.method == "GET":
        # Get 1 row from products table where products.id = id using sqlalchemy functions
        data = request.get_json(force=True)
        p_id = data.get('p_id')
        product = ProductTableModel.readProductById(session, p_id)
        if product:
            return jsonify({
                "p_id": product.p_id,
                "name": product.name,
                "cost": product.cost,
                "tag": product.tag,
                "img": product.img,
                "des": product.des,
                "s_id": product.s_id
            })
        else:
            return jsonify({"message": "Product not found"})
        
    elif request.method == "PATCH":
        # Update 1 row in products table where products.id = id using sqlalchemy functions
        data = request.get_json(force=True)
        p_id = data.get('p_id')
        ProductTableModel.updateProductInfo(session, **data)
        return jsonify({"message": "Product updated successfully"})
    
    elif request.method == "DELETE":
        # Delete 1 row from products table where products.id = id using sqlalchemy functions
        data = request.get_json(force=True)
        p_id = data.get('p_id')
        ProductTableModel.deleteProduct(session, p_id)
        return jsonify({"message": "Product deleted successfully"})

    
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run()