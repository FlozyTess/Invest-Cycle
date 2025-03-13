import bcrypt
import getpass
from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User

Session = sessionmaker(bind=engine)
session = Session()

def hash_password(password):        # for hashing the password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_password, entered_password):         # to verify the password
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_password) 

def signup():           # for signing up users
    name = input("Enter your name: ")
    email = input("Enter your email: ")

