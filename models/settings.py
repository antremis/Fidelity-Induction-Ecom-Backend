import os
from os.path import join, dirname
from dotenv import load_dotenv

#dotenv_path = join(dirname(__file__), '.env')
load_dotenv()

# SECRET_KEY = os.environ.get("SECRET_KEY")
DATABASE_PASSWORD = os.environ.get("avi%401201")