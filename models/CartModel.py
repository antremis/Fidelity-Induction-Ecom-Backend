from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os

load_dotenv()
#DB_URL = 'mysql+pymysql://root:root@localhost/fidelity'
DB_ENGINE = create_engine(os.getenv("DB_URL"))
Base = declarative_base()

class CartItem(Base):
    __tablename__ = 'Cart'
    u_id = Column(Integer, nullable=False)
    p_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False, default=1)
    __mapper_args__={"primary_key": [u_id, p_id]}
    # CUSTOMER = relationship('Customer')
    # PRODUCT = relationship('Product')

Base.metadata.create_all(DB_ENGINE)
# Session = sessionmaker(bind=create_engine(DB_ENGINE))
# session = Session()

def addToCart(session):
    u_id = int(input("Enter u_id: "))
    p_id = int(input("Enter p_id: "))

    # Check if the CUSTOMER and PRODUCT exist
    # CUSTOMER = session.query(Customer).filter_by(id=customer_id).first()
    # PRODUCT = session.query(Product).filter_by(id=product_id).first()

    # if CUSTOMER and PRODUCT:
    quantity = int(input("Enter the quantity: "))
    if quantity > 0:
        cart_item = CartItem(u_id=u_id, p_id=p_id, qty=quantity)
        session.add(cart_item)
        session.commit()
        return cart_item
    #     print("Product added to the cart successfully.")
    # else:
    #     print("Quantity must be greater than 0.")
    # else:
    #     print("CUSTOMER or PRODUCT not found.")

def getCart(session, u_id):
    cart = session.query(CartItem).filter_by(u_id=u_id).all()
    return cart

def removeFromCart(session):
    customer_id = int(input("Enter CUSTOMER_ID: "))
    product_id = int(input("Enter PRODUCT_ID: "))

    # Check if the CUSTOMER and PRODUCT exist
    # CUSTOMER = session.query(Customer).filter_by(id=customer_id).first()
    # PRODUCT = session.query(Product).filter_by(id=product_id).first()

    # if CUSTOMER and PRODUCT:
    cart_item = session.query(CartItem).filter_by(u_id=customer_id, p_id=product_id).first()
    # if cart_item:
    session.delete(cart_item)
    session.commit()
    return (cart_item)
        # print("Product removed from the cart successfully.")
    # else:
    #     print("Product not found in the CUSTOMER's cart.")
    # else:
    #     print("CUSTOMER or PRODUCT not found.")

# while True:
#     print("1. Add Product to Cart")
#     print("2. Remove Product from Cart")
#     print("3. Get Cart Using U_ID")
#     print("4. Exit")

#     choice = input("Enter your choice (1/2/3/4): ")

#     if choice == "1":
#         addToCart()
#     elif choice == "2":
#         removeFromCart()
#     elif choice == "3":
#         getCart(int(input()))
#     elif choice == "4":
#         break
#     else:
#         print("Invalid choice. Please enter 1, 2, or 3.")

# session.close()