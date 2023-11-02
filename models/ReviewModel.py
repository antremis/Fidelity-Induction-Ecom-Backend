# Import necessary SQLAlchemy components
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime,func,UniqueConstraint
from server import Base, session
import datetime
import uuid
# Define the database connection URL for MySQL
# Replace 'username', 'password', 'host', 'port', and 'database_name' with your actual MySQL credentials


# Create an SQLAlchemy engine to connect to the MySQL database

# Create a base class for declarative class definitions

# Define the Product table class that maps to the 'product' table
class ReviewClass(Base):
    __tablename__ = 'review_table'  # Table name

    r_id = Column(String(255), primary_key=True, default=str(uuid.uuid4()))  
    p_id = Column(Integer)  # Product ID
    review = Column(Text)  # Review text
    u_id = Column(String(50))  # User name (up to 50 characters)
    date = Column(DateTime, default=datetime.datetime.now())  # Review date with a default value
    rating=Column(Integer) #rating 
    

    
#CRUD OPERATION


def createNewReview(session,p_id,review,u_id,rating):
    new_review=ReviewClass(p_id=p_id,review=review,u_id=u_id,rating=rating)
    session.add(new_review)
    session.commit()

def readReviewPID(session,p_id):
    review1=session.query(ReviewClass).filter(ReviewClass.p_id==p_id).all()
    return review1

def readReviewUid(session,u_id):
    review1=session.query(ReviewClass).filter(ReviewClass.u_id==u_id).all()
    return review1

def avgRatingPid(session,p_id):
    pid_rating=session.query(func.avg(ReviewClass.rating)).filter(ReviewClass.p_id==p_id).scalar()
    if pid_rating is not None:
        return round(pid_rating,2)
    else:
        return None 


    

def updateReview(session,r_id,review=None,rating=None):
    new_review=session.query(ReviewClass).filter(ReviewClass.r_id==r_id).first()
    # select * from review where review.r_id = r_id
    # ^ - cursor
    # new_review ^
    # new_review.first()

    # True, False, Truthy, Falsy
    # 0 -> False, all else is True
    # None -> False
    # False -> False
    # Object -> True

    if new_review:
        if review:
            new_review.review=review
        if rating:
            new_review.rating=rating
        
        new_review.date=datetime.datetime.utcnow()
        session.commit()

def deleteReview(session,r_id):
    delete_review=session.query(ReviewClass).filter(ReviewClass.r_id==r_id).first()
    if delete_review:
        session.delete(delete_review)
        session.commit()


if __name__=="__main__":
    
    pass

