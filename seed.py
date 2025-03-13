import bcrypt
from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User, Group, GroupMember, Contribution, Payout

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

# Add users to the group if they are not already members
existing_members = session.query(GroupMember).filter(GroupMember.group_id == group1.id).all()
existing_user_ids = {member.user_id for member in existing_members}

memberships_to_add = []
if user1.id not in existing_user_ids:
    memberships_to_add.append(GroupMember(user_id=user1.id, group_id=group1.id, is_active=True))
if user2.id not in existing_user_ids:
    memberships_to_add.append(GroupMember(user_id=user2.id, group_id=group1.id, is_active=True))

if memberships_to_add:
    session.add_all(memberships_to_add)
    session.commit()

# Add contributions if they don't exist
existing_contributions = session.query(Contribution).filter(Contribution.group_id == group1.id).all()
existing_contribution_pairs = {(c.user_id, c.group_id) for c in existing_contributions}

contributions_to_add = []
if (user1.id, group1.id) not in existing_contribution_pairs:
    contributions_to_add.append(Contribution(user_id=user1.id, group_id=group1.id, amount=1000.00))
if (user2.id, group1.id) not in existing_contribution_pairs:
    contributions_to_add.append(Contribution(user_id=user2.id, group_id=group1.id, amount=1000.00))

if contributions_to_add:
    session.add_all(contributions_to_add)
    session.commit()

# Assign a payout (assuming a rotating order)
existing_payout = session.query(Payout).filter_by(user_id=user1.id, group_id=group1.id).first()
if not existing_payout:
    payout1 = Payout(user_id=user1.id, group_id=group1.id, amount=2000.00)  # Joy gets first payout
    session.add(payout1)
    session.commit()

print("Data inserted successfully!")
session.close()
