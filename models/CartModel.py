from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from config import Base, session

class CartItem(Base):
    __tablename__ = 'Cart'
    u_id = Column(Integer, nullable=False)
    p_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False, default=1)
    __mapper_args__={"primary_key": [u_id, p_id]}

def addToCart(session, u_id, p_id, qty):
    try: CartItem(u_id=u_id, p_id=p_id, qty=qty)
    except: pass

def getCart(session, u_id):
    try: return session.query(CartItem).filter_by(CartItem.u_id==u_id).all()
    except: pass

def removeFromCart(session, uid, pid):
    try: 
        session.query(CartItem).filter(CartItem.u_id==uid, CartItem.p_id==pid).first().delete()
        session.commit()
    except: pass

if __name__ == "__main__":
    load_dotenv()
    DB_ENGINE = create_engine(os.getenv("DB_URL"))
    Session = sessionmaker(bind=DB_ENGINE)
    session = Session()
    Base.metadata.create_all(DB_ENGINE)

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