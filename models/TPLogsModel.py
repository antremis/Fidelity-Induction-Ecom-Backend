from sqlalchemy import create_engine, Column, String, Integer, CHAR
from server import Base, session
import uuid

class TransactionProduct(Base):  #TransactionProduct
    __tablename__ = "T_P_Logs"

    t_id = Column("t_id", String(255), nullable = False)   #t_id
    p_id = Column("p_id", Integer, nullable = False)
    quantity = Column("quantity", Integer, nullable = False)
    __mapper_args__={"primary_key": [t_id, p_id]}



#### Query to add new data into table


def insert(session, p_id, quantity):

    t_id = str(uuid.uuid4())
    new_entry = TransactionProduct(t_id = t_id, p_id = p_id, quantity = quantity)
    session.add(new_entry)
    session.commit()


# insert(1234,5)
# insert(123567,8)
# insert(5678,9)
# insert(5674,2)
# insert(6785,3)
# insert(4563,9)


#### Insert values into a single T_id


def generateRandomTidAndInsert(session, pid_quantity_list):  #generateRandomTidAndInsert
    t_id = str(uuid.uuid4())
    for p_id, quantity in pid_quantity_list:
        new_log = TransactionProduct(t_id = t_id, p_id = p_id, quantity = quantity)
        session.add(new_log)
    session.commit()
    return t_id

# id = generateRandomTidAndInsert([(1,10), (2,15), (3,5)])


#### Query to fetch P_id and Quantity when given T_id


def getPidQuantityForTid(session, t_id):
    results = session.query(TransactionProduct.p_id, TransactionProduct.quantity).filter(TransactionProduct.t_id == t_id).all()
    return results

# result = getPidQuantityForTid("6cac23b8-8d68-4815-94ab-e14a906a3ed8")
# print("hii: ",result)


##### Query to fetch Quantity when given T_id and P_id


def fetchQuantity(session, product_id_to_query, transaction_id_to_query):
    quant = session.query(TransactionProduct.quantity).filter(TransactionProduct.p_id == product_id_to_query, 
                                                              TransactionProduct.t_id == transaction_id_to_query).scalar()
    return quant
    
# product_id_to_query = 1234
# transaction_id_to_query = "d263ae6d-d428-4bd9-82dc-7c298ef6ef6a"
# result = fetchQuantity(product_id_to_query, transaction_id_to_query)
# if result is not None:
#     print(f"Quantity for Product ID '{product_id_to_query}' in Transaction ID '{transaction_id_to_query}': {result}")
# else:
#     print("Product ID and Transaction ID not found.")


# #### Define function to delete T_id


def deleteTransaction(session, transaction_id_to_delete):
    session.query(TransactionProduct).filter_by(t_id=transaction_id_to_delete).delete()
    session.commit()

# #### Call function with T_id to be deleted 
# transaction_id_to_delete = "d263ae6d-d428-4bd9-82dc-7c298ef6ef6a"
# deleteTransaction(transaction_id_to_delete)
# print(f"Transaction ID {transaction_id_to_delete} has been deleted.")

# #### To Verify if T_id has been deleted or not
# deleted_transaction = session.query(TransactionProduct).filter_by(t_id=transaction_id_to_delete).first()
# if not deleted_transaction:
#     print(f"Transaction ID {transaction_id_to_delete} not found.")

if __name__ == "__main__":

    insert(session,1234,5)
    insert(session,123567,8)
    insert(session,5678,9)
    insert(session,5674,2)
    insert(session,6785,3)
    insert(session,4563,9)

    id = generateRandomTidAndInsert(session,[(1,10), (2,15), (3,5)])

    result = getPidQuantityForTid(session,"6cac23b8-8d68-4815-94ab-e14a906a3ed8")
    print("hii: ",result)

    product_id_to_query = 1234
    transaction_id_to_query = "d263ae6d-d428-4bd9-82dc-7c298ef6ef6a"
    result = fetchQuantity(session,product_id_to_query, transaction_id_to_query)
    if result is not None:
        print(f"Quantity for Product ID '{product_id_to_query}' in Transaction ID '{transaction_id_to_query}': {result}")
    else:
        print("Product ID and Transaction ID not found.")

    #### Call function with T_id to be deleted 
    transaction_id_to_delete = "d263ae6d-d428-4bd9-82dc-7c298ef6ef6a"
    deleteTransaction(session,transaction_id_to_delete)
    print(f"Transaction ID {transaction_id_to_delete} has been deleted.")

    #### To Verify if T_id has been deleted or not
    deleted_transaction = session.query(TransactionProduct).filter_by(t_id=transaction_id_to_delete).first()
    if not deleted_transaction:
        print(f"Transaction ID {transaction_id_to_delete} not found.")