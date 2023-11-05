from functools import wraps
from flask import request, jsonify, g
import jwt
from models.AuthModel import createJWT, isAdmin
import os

def loginRequired(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authorisation')
        if not token: return jsonify({"mssg": "Unauthorised"}), 403
        try:
            token = token.split(" ")[-1]
            info = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=['HS256'])
            g.uid = info["uid"]
        except Exception as e:
            print(e)
            return jsonify({"mssg": "Invalid or Expired Token!"}), 403
        return f(*args, **kwargs)

    return decorator

def adminOnly(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        print(g.uid)
        if not isAdmin(g.uid): return jsonify({"mssg": "This site is only visible to admins"})
        return f(*args, **kwargs)

    return decorator