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
            # check if email exists 
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        Print("Email already in use. Please log in.")
        return
    password = getpass.getpass("Enter your password: ")  # Hides input
    hashed_pw = hash_password(password)

    new_user = User(name=name, email=email, balance=0.0, reliability_score=100.0, password=hashed_pw)
    session.add(new_user)
    session.commit()
    print("Account created successfully")

def login():
    email = input("Enter your email: ")
    user = session.query(User).filter_by(email=email).first()

    if not user:
        print("No,account found.")
        return
    
    password = getpass.getpass("Enter password: ")
    
    if verify_password(user.password, password):
        print(f"Welcome back, {user.name}!")
    else:
        print("Incorrect password")
        
        #cli menu
def main():
    while True:
        print("\n=== Invest Cycle CLI ===")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            signup()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Great...")
            break
        else:
            print("Invalid choice! Please select again.")

    if __name__ == "__main__":
        main()

