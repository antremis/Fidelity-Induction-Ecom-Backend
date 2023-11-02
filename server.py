from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

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
    
@app.route("/api/logs", methods = ['GET','POST'])
def logs():
    if request.method == "GET":
        return jsonify({"mssg": "success"})
    elif request.method == "POST":
        
        return jsonify({"mmsg": "success", "data" : [1, 2, 3, 4]}) 

@app.route("/api/logs/:id", methods = ['GET', 'PATCH', 'DELETE'])
def logsById(): 
    if request.method == "GET":
        t_id = "6cac23b8-8d68-4815-94ab-e14a906a3ed8"
        result = getPidQuantityForTid(session,t_id)
        if result:
            return jsonify({"mmsg":"success", "data": result})
        return jsonify({"mssg": "success"})
    elif request.method == "PATCH":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})
    elif request.method == "DELETE":
        transaction_id_to_delete = "d263ae6d-d428-4bd9-82dc-7c298ef6ef6a"
        deleteTransaction(session,transaction_id_to_delete)
        return jsonify({"msg":"Transaction id successfully deleted"})
    


    

if __name__ == "__main__":
    app.run()

