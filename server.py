from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv


load_dotenv()


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
def review():
    if request.method == "GET":
        return jsonify({"mssg": "success"})
    elif request.method == "POST":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})

@app.route("/api/review/:id",methods=["GET","PATCH","DELETE"])
def reviewById():
    if request.method == "GET":
        return jsonify({"mssg": "success"})
    elif request.method == "DELETE":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})
    elif request.method == "PATCH":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})
    


    
if __name__ == "__main__":
    app.run()