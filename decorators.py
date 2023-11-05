from functools import wraps
from flask import request, jsonify
import jwt
from models.AuthModel import createJWT, checkAdmin
import os

def loginRequired(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorisation')
        if not token: return jsonify({"mssg": "Unauthorised"}), 403
        try:
            token = token.split(" ")[-1]
            info = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
            # request.uid = info["uid"]
        except Exception as e:
            print(e)
            return jsonify({"mssg": "Invalid or Expired Token!"}), 403
        return f(*args, **kwargs)

    return decorator

def adminOnly(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorisation')
        if not token: return jsonify({"mssg": "Unauthorised"})
        try:
            token = token.split(" ")[-1]
            info = jwt.decode(token, "ASDASDMOASDMUHASIDGABSUYDFANUSDGAUSD", algorithms=['HS256'])
            # if not checkAdmin(info):
            #     pass
        except Exception as e:
            print(e)
            return jsonify({"mssg": "Invalid or Expired Token!"})
        return f(*args, **kwargs)

    return decorator