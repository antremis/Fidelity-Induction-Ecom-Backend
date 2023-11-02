from flask import Flask, request, jsonify, 
from flask_cors import CORS
import models.CartModel as CartModel
import models.ProductTableModel as ProductTableModel
import models.ReviewModel as ReviewModel
import models.TLogModel as TLogModel
import models.TPLogsModel as TPLogsModel
import models.UserModel as UserModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

load_dotenv()
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
    
@app.route("/api/logs")
def logs():
    if request.method == "GET":
        return jsonify({"mssg":"success"})
    elif request.method == "POST":
        pid_quantity_list = [(1,10), (2,15), (3,5)]
        id = TPLogsModel.generateRandomTidAndInsert(session,pid_quantity_list)
        return jsonify({"mmsg":"success", "data": id})
    

@app.route("/api/logs/:t_id")
def transactionById(t_id):
    if request.method == "GET":
       # t_id = "6cac23b8-8d68-4815-94ab-e14a906a3ed8"
        result = TPLogsModel.getPidQuantityForTid(session,t_id)
        return jsonify({"mmsg":"success", "data": result})
    
    if request.method == "PATCH":
        return jsonify({"mmsg":"success", "data": [1, 2, 3, 4, 5]})
    
    if request.method == "DELETE":
       # t_id = "d263ae6d-d428-4bd9-82dc-7c298ef6ef6a"
        delete_tid = TPLogsModel.deleteTransaction(session,t_id)
        return jsonify({"mmsg":"success", "data": delete_tid})
if __name__ == "__main__":
    app.run()

