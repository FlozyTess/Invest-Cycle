import bcrypt
import getpass
from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User, Group, GroupMember, Contribution, Payout
from features import add_contribution, assign_payout

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
        print("Email already in use. Please log in.")
        return
    password = getpass.getpass("Enter your password: ")  # Hides input
    hashed_pw = hash_password(password)

    new_user = User(name=name, email=email, balance=0.0, reliability_score=100.0, password=hashed_pw.decode('utf-8'))
    session.add(new_user)
    session.commit()
    print("Account created successfully")

def login():
    email = input("Enter your email: ")
    user = session.query(User).filter_by(email=email).first()

    if not user:
        print("No,account found.")
        return None
    
    password = getpass.getpass("Enter password: ")
    
    if verify_password(user.password.encode('utf-8'), password):
        print(f"Welcome back, {user.name}!")
        return user
    else:
        print("Incorrect password")
        return None

def view_profile(user):     # views profile for user
    print("\n=== Your Profile ===")
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"Balance: Ksh {user.balance:.2f}")
    print(f"Reliability Score: {user.reliability_score}")
    print("====================")

def create_group(user): # creates a group
    group_name = input("Enter the group name: ")
    contribution_amount = float(input("Enter contribution amount: ")) 
    existing_group = session.query(Group).filter_by(name=group_name).first()
    # checks group existance
    if existing_group:
        print("Group already exists.")
        return

    group = Group(name=group_name, contribution_amount=contribution_amount)
    session.add(group)
    session.commit() 

    session.add(GroupMember(user_id=user.id, group_id=group.id, is_active=True))
    session.commit()
    print(f"Group '{group_name}' created successfully!") 

def join_group(user): 
    group_name = input("Enter the group name to join: ")
    group = session.query(Group).filter_by(name=group_name).first()
    
    if not group:
        print("Group not found.")
        return
    session.add(GroupMember(user_id=user.id, group_id=group.id, is_active=True))
    session.commit()
    print(f"You joined '{group.name}' successfully!")     

# User dashboard after login
def user_dashboard(user):
    while True:
        print("\nUser Menu")
        print("1. View Profile")
        print("2. Create Group")
        print("3. Join Group")
        print("4. Log Out")

        choice = input("Choose an option: ")

        if choice == "1":
            view_profile(user)
        elif choice == "2":
            create_group(user)
        elif choice == "3":
            join_group(user)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

# Main CLI menu
def main():
    while True:
        print("\nMain Menu")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            signup()
        elif choice == "2":
            user = login()
            if user:
                user_dashboard(user)  # Redirects logged-in user to dashboard
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

# Ensure the script runs properly
if __name__ == "__main__":
    main()

