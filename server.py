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
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})



    
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

@app.route('/api/review/product/<pid>',methods=["GET"])
def getReviewByPid(pid):
    if request.method == "GET":
        all_review=ReviewModel.readReviewPid(session,pid)
        review_list=[]
        for reviews in all_review:
            review_list.append({
                "r_id":reviews.r_id,
                "p_id":reviews.p_id,
                "review":reviews.review,
                "u_id":reviews.u_id,
                "date":reviews.date,
                "rating":reviews.rating
            })
        return jsonify({"reviews":review_list})


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
    app.run()
