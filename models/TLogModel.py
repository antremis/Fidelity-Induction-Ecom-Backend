from sqlalchemy import create_engine, Column, Integer, Float, String, Datetime
from config import Base, session
import uuid
from datetime.datetime import now

class TransactionLog(Base):
    __tablename__ = 'T_log'

    t_id = Column(String(100), primary_key=True, default=uuid.uuid4, unique=True)
    u_id = Column(String(100), unique=True)
    s_id = Column(String(100), unique=True)
    t_cost = Column(Float(50))
    date = Column(Datetime, default=now)

def addTransactionLog(session, u_id, s_id, t_cost):
    try:
        new_transaction_log = TransactionLog(u_id=u_id, s_id=s_id, t_cost=t_cost)
        session.add(new_transaction_log)
        session.commit()
        return new_transaction_log.t_id
    except: raise Exception("Could not add Transaction")

def updateTransactionLog(session, t_id, u_id, s_id, t_cost, utr_number):
    try:
        transaction_log = session.query(TransactionLog).filter(TransactionLog.t_id==t_id).first()
        if u_id: transaction_log.u_id = u_id
        if s_id: transaction_log.s_id = s_id
        if t_cost: transaction_log.t_cost = t_cost
        session.commit()
    except: raise Exception("Could not update transaction")

def deleteTransactionLog(session, t_id):
    try:
        session.query(TransactionLog).filter_by(t_id=t_id).first().delete()
        session.commit()
    except: raise Exception("Could not delete transaction")
        
def getAllTlogs(session):
    return session.query(TransactionLog).all()

def getTlog(session, t_id):
    return session.query(TransactionLog).filter(TransactionLog.t_id==t_id).first()

def getTlogUser(session, u_id):
    return session.query(TransactionLog).filter(TransactionLog.u_id==u_id).all()

def getTlogSeller(session, s_id):
    return session.query(TransactionLog).filter(TransactionLog.s_id==s_id).all()

if __name__ == "__main__":
    pass
    # while True:
    #     print("1. Add Transaction Log")
    #     print("2. Update Transaction Log")
    #     print("3. Delete Transaction Log")
    #     print("4. Read Transaction Logs")
    #     print("5. Read Transaction Log by Transaction ID")
    #     print("6. Get Transaction Logs for User ID")
    #     print("7. Get Transaction Logs for Seller ID")
    #     print("8. Exit")

    #     choice = input("Enter your choice (1/2/3/4): ")

    #     if choice == "1":
    #         u_id = input("Enter User ID: ")
    #         s_id = input("Enter Seller ID: ")
    #         t_cost = float(input("Enter Transaction Cost: "))
    #         utr_number = input("Enter UTR Number: ")
    #         added_log = add_transaction_log(u_id, s_id, t_cost, utr_number)
    #         if added_log:
    #             print(f"Transaction log added successfully. ID: {added_log.t_id}")
    #         else:
    #             print("Failed to add transaction log.")
    #         break

    #     elif choice == "2":
    #         tid_to_update = input("Enter the Transaction ID to update: ")
    #         u_id = input(f"Enter new User ID for Transaction ID {tid_to_update}: ")
    #         s_id = input(f"Enter new Seller ID for Transaction ID {tid_to_update}: ")
    #         t_cost = float(input(f"Enter new Transaction Cost for Transaction ID {tid_to_update}: "))
    #         utr_number = input(f"Enter new UTR Number for Transaction ID {tid_to_update}: ")
    #         updated_log = update_transaction_log(tid_to_update, u_id, s_id, t_cost, utr_number)
    #         if updated_log:
    #             print(f"Transaction log with Transaction ID {tid_to_update} updated successfully.")
    #         else:
    #             print(f"Transaction ID {tid_to_update} not found.")
    #         break
        
    #     elif choice == "3":
    #         tid_to_delete = input("Enter the Transaction ID to delete: ")
    #         if delete_transaction_log(tid_to_delete):
    #             print(f"Transaction log with Transaction ID {tid_to_delete} has been deleted.")
    #         else:
    #             print(f"Transaction ID {tid_to_delete} not found.")
    #         break

    #     elif choice == "4":
    #         transaction_logs = getAllTlogs()
    #         if transaction_logs:
    #             for transaction_log in transaction_logs:
    #                 print(f"Transaction ID: {transaction_log.t_id}")
    #                 print(f"User ID: {transaction_log.u_id}")
    #                 print(f"Seller ID: {transaction_log.s_id}")
    #                 print(f"Transaction Cost: {transaction_log.t_cost}")
    #                 print(f"UTR Number: {transaction_log.utr_number}")
    #                 print("----------------------------")
    #         else:
    #             print("No transaction logs found.")
    #         break
        
    #     elif choice == "5":
    #         tid_to_read = input("Enter the Transaction ID to retrieve: ")
    #         transaction_log = getTlog(tid_to_read)
    #         if transaction_log:
    #             print(f"Transaction ID: {transaction_log.t_id}")
    #             print(f"User ID: {transaction_log.u_id}")
    #             print(f"Seller ID: {transaction_log.s_id}")
    #             print(f"Transaction Cost: {transaction_log.t_cost}")
    #             print(f"UTR Number: {transaction_log.utr_number}")
    #         else:
    #             print(f"Transaction ID {tid_to_read} not found.")
    #         break

    #     elif choice == "6":
    #         u_id = input("Enter User ID to retrieve transaction logs for: ")
    #         user_logs = getTlogUser(u_id)
    #         if user_logs:
    #             print("Transaction logs for User ID", u_id)
    #             for transaction_log in user_logs:
    #                 print(f"Transaction ID: {transaction_log.t_id}")
    #                 print(f"User ID: {transaction_log.u_id}")
    #                 print(f"Seller ID: {transaction_log.s_id}")
    #                 print(f"Transaction Cost: {transaction_log.t_cost}")
    #                 print(f"UTR Number: {transaction_log.utr_number}")
    #                 print("----------------------------")
    #         else:
    #             print("No transaction logs found for User ID", u_id)
    #         break
        
    #     elif choice == "7":
    #         s_id = input("Enter Seller ID to retrieve transaction logs for: ")
    #         seller_logs = getTlogSeller(s_id)
    #         if seller_logs:
    #             print("Transaction logs for Seller ID", s_id)
    #             for transaction_log in seller_logs:
    #                 print(f"Transaction ID: {transaction_log.t_id}")
    #                 print(f"User ID: {transaction_log.u_id}")
    #                 print(f"Seller ID: {transaction_log.s_id}")
    #                 print(f"Transaction Cost: {transaction_log.t_cost}")
    #                 print(f"UTR Number: {transaction_log.utr_number}")
    #                 print("----------------------------")
    #         else:
    #             print("No transaction logs found for Seller ID", s_id)
    #         break
        
    #     elif choice == "8":
    #         break

    #     else:
    #         print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7 or 8.")

    # session.close()