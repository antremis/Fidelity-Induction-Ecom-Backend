from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv("DB_URL"))
Session = sessionmaker(bind=engine)
session = Session()
