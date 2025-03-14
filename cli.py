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

def contribute(user):
    """Allows a user to contribute to a group."""
    group_name = input("Enter the group name: ")
    group = session.query(Group).filter_by(name=group_name).first()

    if not group:
        print("Group not found.")
        return

    amount = float(input(f"Enter the amount to contribute (Minimum Ksh {group.contribution_amount}): "))

    if amount < group.contribution_amount:
        print(f"Minimum contribution is Ksh {group.contribution_amount}. Please enter a valid amount.")
        return

    existing_contribution = session.query(Contribution).filter_by(user_id=user.id, group_id=group.id).first()
    if existing_contribution:
        print("You have already contributed to this group.")
        return

    add_contribution(user.id, group.id, amount)
    print(f"Successfully contributed Ksh {amount} to '{group.name}'.")

def payout(user):
    """Assigns a payout to the next eligible user in a group."""
    group_name = input("Enter the group name for payout: ")
    group = session.query(Group).filter_by(name=group_name).first()

    if not group:
        print("Group not found.")
        return

    amount = float(input("Enter the payout amount: "))

    # Fetch active group members
    group_members = session.query(GroupMember).filter_by(group_id=group.id, is_active=True).all()

    if not group_members:
        print("No active members in this group.")
        return

    # Find the last payout recipient
    last_payout = session.query(Payout).filter_by(group_id=group.id).order_by(Payout.timestamp.desc()).first()

    if last_payout:
        # Find the next user in rotation
        last_user_index = next((index for index, member in enumerate(group_members) if member.user_id == last_payout.user_id), -1)
        next_user_index = (last_user_index + 1) % len(group_members)
    else:
        # If no previous payouts, start from the first user
        next_user_index = 0

    next_user = session.query(User).filter_by(id=group_members[next_user_index].user_id).first()

    # Assign the payout
    assign_payout(next_user.id, group.id, amount)
    print(f"Payout of Ksh {amount} assigned successfully to {next_user.name} (ID: {next_user.id}) in group '{group.name}'.")

def user_dashboard(user):
    """Displays the user dashboard menu."""
    while True:
        print("\nUser Menu")
        print("1. View Profile")
        print("2. Create Group")
        print("3. Join Group")
        print("4. Contribute")
        print("5. Assign Payout")
        print("6. Log Out")

        choice = input("Choose an option: ")

        if choice == "1":
            view_profile(user)
        elif choice == "2":
            create_group(user)
        elif choice == "3":
            join_group(user)
        elif choice == "4":
            contribute(user)
        elif choice == "5":
            payout(user)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")
def main():
    """Main menu of the application."""
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
                user_dashboard(user)
        elif choice == "3":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()