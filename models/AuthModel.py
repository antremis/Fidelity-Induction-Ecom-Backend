from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime,func,UniqueConstraint
# from config import Base, session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import bcrypt

Base = declarative_base()
class Auth(Base):
    __tablename__ = 'Auth'  # Table name

    u_id = Column(String(255), primary_key=True, default=uuid.uuid4)  
    username = Column(String(50), unique=True)
    password = Column(String(255))\

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

if __name__ == "__main__":
    engine = create_engine('mysql+pymysql://akash:manarises@localhost/fidelity')
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(bind=engine)
    deleteUser(session, "612a280b-5bbd-48ee-9d18-d3ec6031fb70", "1234")