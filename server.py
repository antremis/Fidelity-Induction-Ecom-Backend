from flask import Flask, request, jsonify, g
from flask_cors import CORS
import models.AuthModel as AuthModel
import models.CartModel as CartModel
import models.ProductTableModel as ProductTableModel
import models.ReviewModel as ReviewModel
import models.TLogModel as TLogModel
import models.TPLogsModel as TPLogsModel
import models.UserModel as UserModel
from config import Base, engine, session
from decorators import loginRequired, adminOnly

app = Flask(__name__)
CORS(app)
carts = []

# Define a route to add a product to the cart
@app.route("/api/cart", methods=["POST"])
@loginRequired
def addToCart():
    if request.method == "GET":
        user_cart = CartModel.getCart(session, g.uid)
        if user_cart:
            return jsonify({"mssg": "success", "data": user_cart})
            
    if request.method == "POST":
        data = request.get_json(force=True)
        p_id = data.get("p_id")
        qty = data.get("qty")
        CartModel.addToCart(session, g.uid, p_id, qty)
        return jsonify({"message": "Product added to the cart successfully."})

    if request.method == "DELETE":
        CartModel.removeFromCart(session)
        return jsonify({"message": "Product removed from the cart successfully."})

# Define a route to get the cart for a user
@app.route("/api/cart/<int:u_id>", methods=["GET"])
def getCart(u_id):
    pass

# Define a route to remove a cart item
@app.route("/api/cart/<int:u_id>/<int:p_id>", methods=["DELETE"])
@loginRequired
def removeFromCart(u_id, p_id):
    for cart_item in carts:
        if cart_item["u_id"] == u_id and cart_item["p_id"] == p_id:
            carts.remove(cart_item)
            return jsonify({"message": "Cart item removed from the cart successfully."})

    return jsonify({"message": "Cart item not found in the cart."}), 404

@app.route("/api/test", methods=["GET"])
def test():
    return jsonify({"mssg": "success"})

@app.route("/api/auth", methods=["GET", "PATCH"])
@loginRequired
@adminOnly
def adminAuth():
    if request.method == "GET":
        users = AuthModel.getUsers(session)
        return jsonify({"mssg": "success", "data":users})
    elif request.method == "PATCH":
        uid = request.get_json(force=True).get("uid")
        AuthModel.makeAdmin(uid)
        return jsonify({"mssg": f"success! user {uid} was made an admin"})

@app.route("/api/auth", methods=["PUT", "POST"])
def auth():
    if request.method == "PUT":
        data = request.get_json(force=True)
        username = data.get("username")
        password = data.get("password")
        uid = AuthModel.createUser(session, username, password)
        return jsonify({"mssg": "success", "data": AuthModel.createJWT(uid)})
    elif request.method == "POST":
        body = request.get_json(force=True)
        username=body.get("username")
        password=body.get("password")
        uid = AuthModel.checkUser(session, username, password)
        return jsonify({"mssg":"success", "data": AuthModel.createJWT(uid)})

@app.route("/api/auth/<id>", methods=["DELETE"])
@loginRequired
def get(id):
    if request.method == "DELETE":
        if id != g.uid: return jsonify({"mssg": "You are Unauthorised to complete this action!"})
        AuthModel.deleteUser(session, id)
        return jsonify({"mssg":"success"})

@app.route("/api/product", methods=["GET", "POST"])
@loginRequired
def product():
    if request.method == "GET":
        # Get all rows from products table using sqlalchemy functions
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
        data = request.get_json(force=True)
        name = data.get('name')
        cost = data.get('cost')
        tag = data.get('tag')
        img = data.get('img')
        des = data.get('des')
        s_id = g.uid
        new_id = ProductTableModel.addProduct(session, name, cost, tag, img, des, s_id)
        return jsonify({"message": "Product added successfully", "p_id": new_id})
        
@app.route("/api/products/categories", methods=["GET"])
def getProductsByCategory():
    category = request.args.get("category")
    result = ProductTableModel.displayProductsByTags(session, category)
    return jsonify({"mssg": "success", "data": [{
        "name" : product.name,
        "cost" : product.cost,
        "tag" : product.tag,
        "img" : product.img,
        "des" : product.des,
        "p_id" : product.p_id
    } for product in result]})
    
@app.route("/api/products/<p_id>",methods=["GET","PATCH","DELETE"])
def productById(p_id):
    if request.method == "GET":
        # Get 1 row from products table where products.id = id using sqlalchemy functions
        products = ProductTableModel.readProductById(session, p_id)
        if product:
            return jsonify({"mssg": "success", "data": {
                    "p_id": products.p_id,
                    "name": products.name,
                    "cost": products.cost,
                    "tag": products.tag,
                    "img": products.img,
                    "des": products.des,
                    "s_id": products.s_id
                }})
        else:
            return jsonify({"message": {
                    "p_id": "NA",
                    "name": "NA",
                    "cost": "NA",
                    "tag": "NA",
                    "img": "NA",
                    "des": "NA",
                    "s_id": "NA"
                }})
        
    elif request.method == "PATCH":
        # Update 1 row in products table where products.id = id using sqlalchemy functions
        data = request.get_json(force=True)
        data={
            p_id : data.get('p_id'),
            name : data.get('name'),
            cost : data.get('cost'),
            tag : data.get('tag'),
            img : data.get('img'),
            des : data.get('des'),
            s_id : data.get('s_id',)
        }
        ProductTableModel.updateProductInfo(session, **data)
        return jsonify({"message": "Product updated successfully"})
    
    elif request.method == "DELETE":
        # Delete 1 row from products table where products.id = id using sqlalchemy functions
        data = request.get_json(force=True)
        p_id = data.get('p_id')
        ProductTableModel.deleteProduct(session, p_id)
        return jsonify({"message": "Product deleted successfully"})

    
@app.route("/api/logs", methods = ['GET', 'POST'])
def logs():
    if request.method == "GET":
        return jsonify({"mssg":"success"})
    elif request.method == "POST":
        data = request.get_json(force = True)
        pid_quantity_list = data.get("pid_quantity_list") 
        id = TPLogsModel.generateRandomTidAndInsert(session,pid_quantity_list)
        return jsonify({"mssg":"success", "data": id})
    

@app.route("/api/logs/<t_id>", methods = ['GET', 'PATCH', 'DELETE'])
def logsById(t_id):
    if request.method == "GET":
       # t_id = "6cac23b8-8d68-4815-94ab-e14a906a3ed8"
       result = TPLogsModel.getPidQuantityForTid(session,t_id)
       return jsonify({"mssg":"success", "data": [list(res) for res in result]})
    
    if request.method == "PATCH":
        return jsonify({"mssg":"success", "data": [1, 2, 3, 4, 5]})
    
    if request.method == "DELETE":
       # t_id = "d263ae6d-d428-4bd9-82dc-7c298ef6ef6a"
        delete_tid = TPLogsModel.deleteTransaction(session,t_id)
        return jsonify({"mssg":"success", "data": delete_tid})

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

@app.route("/api/user", methods=["GET", "POST", "PATCH"])
@loginRequired
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
       
        UserModel.addUser(session, g.uid, email, phone, address)
        return jsonify({"mssg":"User added"})

    elif request.method == "PATCH":
        data = request.get_json()
        print(data)
        UserModel.updateUserInfo(session, g.uid, data)
        return jsonify({"msg":"Information Updated"}) 


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

    
    
@app.route("/api/review",methods=["GET","POST"])
def reviewPid():
    # if request.method == "GET":
    #     all_review=readReviewPid(session)
    #     review_list=[]
    #     for reviews in all_review:
    #         review_list.append({
    #             "r_id":reviews.r_id,
    #             "p_id":reviews.p_id,
    #             "review":reviews.review,
    #             "u_id":reviews.u_id,
    #             "date":reviews.date,
    #             "rating":reviews.rating
    #         })
    #     return jsonify({"reviews":review_list})
    # if request.method == "GET":
    #     all_review=readReviewUid(session)
    #     review_list=[]
    #     for reviews in all_review:
    #         review_list.append({
    #             "r_id":reviews.r_id,
    #             "p_id":reviews.p_id,
    #             "review":reviews.review,
    #             "u_id":reviews.u_id,
    #             "date":reviews.date,
    #             "rating":reviews.rating
    #         })
    #     return jsonify({"reviews":review_list})
    if request.method == "POST":

        data = request.get_json(force=True)
        
        p_id=data.get("p_id")
        review=data.get("review")
        u_id=data.get("u_id")
        rating=data.get("rating")

        new_id = ReviewModel.createNewReview(session,p_id,review,u_id,rating)

        return jsonify({"message": "Product added successfully", "new review": new_id})

@app.route("/api/review/<r_id>",methods=["GET","PATCH","DELETE"])
def reviewById(r_id):
    if request.method == "GET":
        return jsonify({"mssg": "success"})
    
    elif request.method == "DELETE":

        ReviewModel.deleteReview(session,r_id)

        return jsonify({"mmsg":"success"})
    
    elif request.method == "PATCH":
        data=request.get_json(force=True)
        review=data.get("review")
        rating=data.get("rating")

        new_review=ReviewModel.updateReview(session,r_id,review,rating)

        return jsonify({"mmsg":"success", "updated review": new_review})


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(debug=True)
