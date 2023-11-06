from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime,func,UniqueConstraint, Boolean
from config import Base, session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import bcrypt
import jwt
import datetime
import os

class Auth(Base):
    __tablename__ = 'Auth'  # Table name

    u_id = Column(String(255), primary_key=True, default=uuid.uuid4)  
    username = Column(String(50), unique=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)

def getUsers(session):
    users = session.query(Auth.u_id).all()
    return [list(user) for user in users]
    
def createUser(session, username, password):
    user = Auth(username=username, password=bcrypt.hashpw(password.encode('utf-8') , bcrypt.gensalt()))
    session.add(user)
    session.commit()
    return user.u_id

def checkUser(session, username, password):
    user = session.query(Auth.password, Auth.u_id).filter(Auth.username==username).first()
    if not user:
        raise Exception('User not found')
    if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return user.u_id
    else: raise Exception('Incorrect Password')

def deleteUser(session, uid):
    user = session.query(Auth).filter(Auth.u_id==uid).first()
    if not user:
        raise Exception('User not found')
    # if NotAuthenticated
    session.query(Auth).filter(Auth.u_id==uid).delete()
    session.commit()

def createJWT(uid):
    return jwt.encode({'uid': uid, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, os.getenv("SECRET_KEY"))

def isAdmin(uid):
    return session.query(Auth.is_admin).filter(Auth.u_id==uid).first().is_admin

def makeAdmin(uid):
    user = session.query(Auth).filter(Auth.u_id==uid).first()
    user.is_admin = 1
    session.commit()

if __name__ == "__main__":
    # engine = create_engine('mysql+pymysql://root:avi%401201@localhost/fidelity')
    # Session = sessionmaker(bind=engine)
    # session = Session()
    # Base.metadata.create_all(bind=engine)
    # createUser(session, "Akaash", "12434")

    def loginRequired(f):
        def decorator(*args, **kwargs):
            # Get JWT
            print(args, kwargs)
            f()
        return decorator

    @app.route()
    def protected():
        print("Here")

    print(createJWT())
