from flask import Flask, request, jsonify
from flask_cors import CORS
import models.CartModel as CartModel
import models.ProductTableModel as ProductTableModel
import models.ReviewModel as ReviewModel
import models.TLogModel as TLogModel
import models.TPLogsModel as TPLogsModel
import models.UserModel as UserModel
from config import Base,session,engine

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
        all_products = ReviewModel.displayAllProducts(session)
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
        new_id = ReviewModel.addProduct(session, p_id, name, cost, tag, img, des, s_id)
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
        r_id=data.get("r_id")
        p_id=data.get("p_id")
        review=data.get("review")
        u_id=data.get("u_id")
        date=data.get("date")
        rating=data.get("rating")
        new_id = ReviewModel.createNewReview(session, r_id, p_id, review, u_id, date, rating)

        return jsonify({"message": "Product added successfully", "new review": new_id})

@app.route("/api/review/<r_id>",methods=["GET","PATCH","DELETE"])
def reviewById():
    if request.method == "GET":
        return jsonify({"mssg": "success"})
    elif request.method == "DELETE":
        data=request.get_json(force=True)
        r_id=data.get("r_id")

        ReviewModel.deleteReview(session,r_id)

        return jsonify({"mmsg":"success"})
    elif request.method == "PATCH":
        data=request.get_json(force=True)
        r_id=data.get("r_id")
        review=data.get("review")
        rating=data.get("rating")

        new_review=ReviewModel.updateReview(session,r_id,review,rating)


        return jsonify({"mmsg":"success", "updated review": new_review})
    


    
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run()
