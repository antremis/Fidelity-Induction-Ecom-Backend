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
        return jsonify({"mssg": "success"})
    elif request.method == "POST":
        return jsonify({"mssg":"success", "data": [1, 2, 3, 4, 5]})

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
    
@app.route("/api/products/<id>",methods=["GET","PATCH","DELETE"])
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


@app.route("/api/transaction", methods=["GET", "POST"])
def transaction():
    if request.method == "GET":
        all_t_logs = TLogModel.getAllTlogs(session)
        transaction_logs_list = []
        for t_logs in all_t_logs:
            transaction_logs_list.append({
                "p_id": t_logs.t_id,
                "u_id": t_logs.u_id,
                "s_id": t_logs.s_id,
                "t_cost":  t_logs.t_cost,
                "time": t_logs.time
            })
        return jsonify({"t_logs": transaction_logs_list})

    elif request.method == "POST":
        data = request.get_json(force=True)
        product_list = data.get('p_id')
        u_id = data.get('u_id')
        s_id = data.get('s_id')
        t_cost = data.get('t_cost')
        utr_number = data.get("utr_number")

        tid = TLogModel.addTransactionLog(session, u_id, s_id, t_cost, utr_number)
        TPLogsModel.generateRandomTidAndInsert(session, product_list)
        return jsonify({"mssg":"Transaction Log added", "tid": tid})

@app.route("/api/transaction/<t_id>", methods=["GET", "DELETE", "PATCH"])
def transactionById(t_id):
    if request.method == "GET":
        data = request.get_json(force=True)
        t_id = data.get("t_id")
        transaction_log_byID = TLogModel.getTlog(session, t_id)
        if transaction_log_byID:
            return jsonify({
                "t_id": transaction_log_byID.t_id,
                "u_id": transaction_log_byID.u_id,
                "s_id": transaction_log_byID.s_id,
                "t_cost": transaction_log_byID.t_cost,
                "utr_number": transaction_log_byID.utr_number,
            })
        return jsonify({"Transaction Log By id": transaction_log_byID})

    elif request.method == "DELETE":
        data = request.get_json(force=True)
        t_id = data.get('t_id')
        TLogModel.deleteTransactionLog(session, t_id)
        return jsonify({"mssg": "Transaction Log Deleted"})

    elif request.method == "PATCH":
        data = request.get_json(force=True)
        t_id = data.get('t_id')
        u_id = data.get('u_id')
        s_id = data.get('s_id')
        t_cost = data.get('t_cost')
        TLogModel.updateTransactionLog(session, t_id, u_id, s_id, t_cost, utr_number)
        TLogModel.updateTransactionLog(session, **data)
        return jsonify({"msg":"Information Updated"}) 

@app.route("/api/user", methods=["GET", "POST"])
def user():
    # Template function
    if request.method == "GET":
        all_users = UserModel.getAllUsers(session)
        users_list = []
        for users in all_users:
            users_list.append({
                "u_id": users.u_id,
                "email": users.email,
                "phone":  users.phone,
                "address": users.address,
            })
        return jsonify({"msg": "success", "data": [list(result) for result in users_list]})

    elif request.method == "POST":
        data = request.get_json(force=True)

        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
       
        new_user = UserModel.addUser(session, email, phone, address)
        return jsonify({"mssg":"User added", "User": new_user})


@app.route("/api/user/<u_id>", methods=["GET", "DELETE", "PATCH"])
def userById(u_id):
    if request.method == "GET":
        data = request.get_json(force=True)
        user_by_id = UserModel.getUser(session, u_id)
        if user_by_id:
            return jsonify({
                "u_id": user_by_id.u_id,
                "email": user_by_id.email,
                "phone": user_by_id.phone,
                "address": user_by_id.address
            })
        return jsonify({"User By id": user_by_id})

    elif request.method == "DELETE":
        data = request.get_json(force=True)
        u_id = data.get('u_id')
        UserModel.deleteUser(session, u_id)
        return jsonify({"mssg": "User Log Deleted"})

    elif request.method == "PATCH":
        data = request.get_json()
        u_id = data.get('u_id')
        # email = data.get('email')
        # phone = data.get('phone')
        # address = data.get("address")
        UserModel.updateUserInfo(session, **data)
        return jsonify({"msg":"Information Updated"}) 


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run()