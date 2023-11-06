from sqlalchemy import create_engine, Column, Integer, String
from config import Base, session
import uuid

class User(Base):
    __tablename__='Users'
    u_id=Column(String(100), primary_key=True, unique=True)
    email=Column(String(50), unique=True, nullable=False)
    phone=Column(String(10))
    address=Column(String(100))

def getUser(session, u_id):
    return session.query(User).filter_by(u_id=u_id).first()

def getAllUsers(session):
    return session.query(User).all()

def addUser(session, uid, email, phone, address):
    new_user = User(u_id=uid, email=email, phone=phone, address=address)
    session.add(new_user)
    session.commit()
    return new_user

def updateUserInfo(session, u_id, data):
    user = session.query(User).filter(User.u_id==u_id).first()

    if data.get("email"): user.email=data.get("email")
    if data.get("phone"): user.phone=data.get("phone")
    if data.get("address"): user.address=data.get("address")
    session.commit()
    return user

def deleteUser(session, u_id):
    user = session.query(User).filter(User.u_id==u_id).first()
    session.delete(user)
    session.commit()
        

if __name__ == "__main__":
    pass


# while True:
#     print("1. Add User")
#     print("2. Update User")
#     print("3. Delete User")
#     print("4. Get all Users")
#     print("5. Get user by ID")
#     print("6. Exit")

#     choice = input("Enter your choice (1/2/3/4): ")

#     if choice == "1":
#         email = input("Enter email: ")
#         phone = input("Enter phone: ")
#         address = input("Enter address: ")
#         add_user(email, phone, address)
#         break
#     elif choice == "2":
#         u_id = input("Enter the User ID to update: ")
#         email = input("Enter new email: ")
#         phone = input("Enter new phone: ")
#         address = input("Enter new address: ")
#         updated_user = update_user_info(u_id, email, phone, address)
#         if updated_user:
#             print(f"User with User ID {u_id} updated successfully.")
#         else:
#             print(f"User ID {u_id} not found.")
#         break
#     elif choice == "3":
#         u_id = input("Enter the User ID to delete: ")
#         if delete_user(u_id):
#             print(f"User with User ID {u_id} has been deleted.")
#         else:
#             print(f"User ID {u_id} not found.")
#         break

#     elif choice == "4":
#         users = getAllUsers()
#         if users:
#             for user in users:
#                 print(f"User ID: {user.u_id}")
#                 print(f"Email: {user.email}")
#                 print(f"Phone: {user.phone}")
#                 print(f"Address: {user.address}")
#                 print("----------------------------")
#         else:
#             print("No users found.")
        
#         break
    
#     elif choice == "5":
#         u_id = input("Enter the User ID to retrieve: ")
#         user = getUser(u_id)
#         if user:
#             print(f"User ID: {user.u_id}")
#             print(f"Email: {user.email}")
#             print(f"Phone: {user.phone}")
#             print(f"Address: {user.address}")
#         else:
#             print(f"User ID {u_id} not found.")
#         break
#     elif choice == "6":
#         break
#     else:
#         print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")

# session.close()