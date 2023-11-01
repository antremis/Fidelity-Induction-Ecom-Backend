# Import necessary SQLAlchemy components
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime,func,UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime,uuid

# Define the database connection URL for MySQL
# Replace 'username', 'password', 'host', 'port', and 'database_name' with your actual MySQL credentials
db_url = 'mysql+pymysql://root:avi%401201@localhost/product_database'

# Create an SQLAlchemy engine to connect to the MySQL database
engine = create_engine(db_url, echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()

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



# Create the 'product' table in the MySQL database
Base.metadata.create_all(engine)

# Establish a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Example: Create a new product review entry
# createNewReview(session, p_id=1, review="This product is bad!", u_id=1, rating=2)

# Example: Create new product reviews
# createNewReview(session, p_id=1, review="This product is great!", u_id="User1", rating=5)
# createNewReview(session, p_id=1, review="Not bad, but could be better.", u_id="User2", rating=3)
# createNewReview(session, p_id=2, review="Terrible product!", u_id="User1", rating=1)

# Example: Read reviews by Product ID
product_reviews = readReviewPID(session, p_id=1)
print("Reviews for Product ID 1:")
for review in product_reviews:
    print(f"Review ID: {review.r_id}, User: {review.u_id}, Rating: {review.rating}, Review: {review.review}")

# Example: Read reviews by User ID
user_reviews = readReviewUid(session, u_id="User1")
print("\nReviews by User 'User1':")
for review in user_reviews:
    print(f"Review ID: {review.r_id}, Product ID: {review.p_id}, Rating: {review.rating}, Review: {review.review}")

# Example: Calculate average rating for a Product
product_avg_rating = avgRatingPid(session, p_id=1)
print(f"\nAverage Rating for Product ID 1: {product_avg_rating}")

updateReview(session, r_id="be0dd22e-b5bf-4746-bcbf-5b33dee27c52", review="Updated review text", rating=4)







