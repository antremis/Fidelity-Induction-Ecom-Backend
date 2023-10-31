from flask import Flask, request, jsonify, 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/test")
def test():
    # Template function
    if request.method == "GET":
        return jsonify({"mssg": "success"})
    elif request.method == "POST":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})
    
if __name__ == "__main__":
    app.run()