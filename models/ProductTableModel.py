from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from config import Base, session
import uuid

class Product(Base):
    __tablename__ = 'products'

    p_id = Column(String(50), primary_key=True, default=uuid.uuid4)
    name = Column(String(255))
    cost = Column(Float)
    tag = Column(String(255))
    img = Column(String(255))
    des = Column(Text)
    s_id = Column(String(50))

# Create the table in the database

def addProduct(session,name,cost,tag,img,des,s_id):
    new_product = Product( name=name, cost=cost, tag=tag, img=img, des=des, s_id=s_id)
    session.add(new_product)
    session.commit()
    return new_product.p_id
    # print("Product added successfully.")

def updateProductInfo(session, p_id,name=None,cost=None,tag=None,img=None,des=None,s_id=None):
    product = session.query(Product).filter(Product.p_id==p_id).first()
    if product:
        if name: product.name=name
        if cost: product.cost=cost
        if tag: product.tag=tag
        if img: product.img=img
        if des: product.des=des
        if s_id: product.s_id=s_id
        session.commit()
        #print("Product updated successfully.")
    #else:
        #print(f"Product ID {product} not found.")
    
def readProductById(session, p_id):
    read_product_var = session.query(Product).filter(Product.p_id==p_id).first()
    return read_product_var
    

    # if product:
    #     return product.p_id,
        
        # print(f"Product ID: {product.p_id}")
        # print(f"Name: {product.name}")
        # print(f"Cost: {product.cost}")
        # print(f"Tag: {product.tag}")
        # print(f"Image: {product.img}")
        # print(f"Description: {product.des}")
        # print(f"Supplier ID: {product.s_id}")
    # else:
    #     print(f"Product ID {p_id} not found.")
            

def deleteProduct(session,p_id):
    #product_id_to_delete = int(input("Enter the Product ID to delete: "))
    product = session.query(Product).filter_by(p_id=p_id).first()

    if product:
        session.delete(product)
        session.commit()
        #print(f"Product with Product ID {p_id} has been deleted.")
    # else:
    #     print(f"Product ID {p_id} not found.")

def displayAllProducts(session):
    all_products = session.query(Product).all()
    return all_products
    # for product in all_products:
    #     print(f"Product ID: {product.p_id}")
    #     print(f"Name: {product.name}")
    #     print(f"Cost: {product.cost}")
    #     print(f"Tag: {product.tag}")
    #     print(f"Image: {product.img}")
    #     print(f"Description: {product.des}")
    #     print(f"Supplier ID: {product.s_id}")
        
# def display_products_by_seller_and_tags(session, s_id, tags):
#     filtered_products = session.query(Product).filter(Product.s_id == s_id, Product.tag.in_(tags)).all()

#     for product in filtered_products:
#         print(f"Product ID: {product.p_id}")
#         print(f"Name: {product.name}")
#         print(f"Cost: {product.cost}")
#         print(f"Tag: {product.tag}")
#         print(f"Image: {product.img}")
#         print(f"Description: {product.des}")
#         print(f"Supplier ID: {product.s_id}")

def displayProductsBySeller(session, s_id):
    filtered_products = session.query(Product).filter(Product.s_id == s_id).all()
    return filtered_products

    # for product in filtered_products:
    #     print(f"Product ID: {product.p_id}")
    #     print(f"Name: {product.name}")
    #     print(f"Cost: {product.cost}")
    #     print(f"Tag: {product.tag}")
    #     print(f"Image: {product.img}")
    #     print(f"Description: {product.des}")
    #     print(f"Supplier ID: {product.s_id}")
        

def displayProductsByTags(session, tag):
    filtered_products = session.query(Product).filter(Product.tag==tag).all()
    return filtered_products

if __name__=="__main__":
    pass
    # for product in filtered_products:
    #     print(f"Product ID: {product.p_id}")
    #     print(f"Name: {product.name}")
    #     print(f"Cost: {product.cost}")
    #     print(f"Tag: {product.tag}")
    #     print(f"Image: {product.img}")
    #     print(f"Description: {product.des}")
    #     print(f"Supplier ID: {product.s_id}")
        




# while True:
#     print("1. Add Product")
#     print("2. Read ")
#     print("3. Update Product")
#     print("4. Delete Product")
#     print("5. Display All Products")
#     print("6. Products by Seller")
#     print("7. Products by Tags")

#     print("8. Exit")

#     choice = input("Enter your choice (1/2/3/4/5/6/7/8): ")

#     if choice == "1":
#         addProduct(session=session,p_id=4,name='Asus Zenbook',cost=65000,tag='Electronics',img="zenbook.jpg",des="elct",s_id=1250)
#     elif choice == "2":
#         readProductById(session=session,p_id=3)
#     elif choice == "3":
#         updateProductInfo(session=session,p_id=3)
#     elif choice == "4":
#         deleteProduct(p_id=2)
#     elif choice == "5":
#         displayAllProducts(session=session)
#     elif choice == "6":
#         displayProductsBySeller(session=session,s_id=1250)
#     elif choice == "7":
#         displayProductsByTags(session=session,tag=['Electronics'])
#     elif choice == "8":
#         break
#     else:
#         print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7 or 8.")



# Close the session
#session.close()
