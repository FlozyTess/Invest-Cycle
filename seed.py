import bcrypt
from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User, Group, GroupMember, Contribution, Payout
from features import add_contribution, assign_payout

Session = sessionmaker(bind=engine)
session = Session()

# Function to get or create a user
def get_or_create_user(name, email, password, balance, reliability_score):
    user = session.query(User).filter_by(email=email).first()
    if not user:
        # Hash the password before storing
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        user = User(
            name=name,
            email=email,
            password=hashed_password.decode('utf-8'),
            balance=balance, 
            reliability_score=reliability_score
        )
        session.add(user)
        session.commit()
        print(f"Created new user: {name}")
    else:
        print(f"User {name} already exists.")
    return user  # Always returns a valid user object

# Ensure users exist
user1 = get_or_create_user("Joy", "joy@outlook.com", "securepassword256", 3000.00, 100.0)
user2 = get_or_create_user("Gabby", "gabby@gmail.com", "strongpassword123", 5000.00, 100.0)

# Get or create the group
group1 = session.query(Group).filter_by(name="Alpha Investors").first()
if not group1:
    group1 = Group(name="Alpha Investors", contribution_amount=1000.00)
    session.add(group1)
    session.commit()
    print(f"Created new group: {group1.name}")
else:
    print(f"Group '{group1.name}' already exists.")

# Add users to the group if not already members
existing_members = session.query(GroupMember).filter_by(group_id=group1.id).all()
existing_user_ids = {member.user_id for member in existing_members}

if user1.id not in existing_user_ids:
    session.add(GroupMember(user_id=user1.id, group_id=group1.id, is_active=True))
    print(f"{user1.name} added to group '{group1.name}'.")

if user2.id not in existing_user_ids:
    session.add(GroupMember(user_id=user2.id, group_id=group1.id, is_active=True))
    print(f"{user2.name} added to group '{group1.name}'.")

session.commit()

# Add contributions using the function (prevents duplicates)
add_contribution(user1.id, group1.id, 1000.00)
add_contribution(user2.id, group1.id, 1000.00)

# Assign payout using the function (prevents duplicates)
assign_payout(user1.id, group1.id, 2000.00)  # Joy gets first payout

print("Data inserted successfully!")
session.close()
