from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User, Group, GroupMember, Contribution, Payout

Session = sessionmaker(bind=engine)
session = Session()

#checks if user exists
def user_exists(email):
    return session.query(User).filter_by(email=email).first() is not None

#Add users if they dont exist
if not user_exists(email="joy@outlook.com"):
    user1 = User(name="Joy",email="joy@outlook.com",balance=3000.00)
    session.add(user1)

if not user_exists(email="gabby@gmail.com"):
    user2 = User(name="Gabby",email="gabby@gmail.com",balance=5000.00)
    session.add(user2)

    session.commit()

# Fetch users after committing
user1 = session.query(User).filter_by(email="joy@outlook.com").first()
user2 = session.query(User).filter_by(email="gabby@gmail.com").first()    

#Add Investment group
group1 = Group(name="Alpha Investors", contribution_amount=1000.00)
session.add(group1)
session.commit()

# Fetch group
group1 = session.query(Group).filter_by(name="Alpha Investors").first()

# Add users to the group
membership1 = GroupMember(user_id=user1.id, group_id=group1.id, is_active=True)
membership2 = GroupMember(user_id=user2.id, group_id=group1.id, is_active=True)

session.add_all([membership1, membership2])
session.commit()

# Add contributions
contribution1 = Contribution(user_id=user1.id, group_id=group1.id, amount=1000.00)
contribution2 = Contribution(user_id=user2.id, group_id=group1.id, amount=1000.00)

session.add_all([contribution1, contribution2])
session.commit()

# Assign a payout (assuming a rotating order)
payout1 = Payout(user_id=user1.id, group_id=group1.id, amount=2000.00)  # Joy gets first payout
session.add(payout1)
session.commit()

print("data inserted successfully!")

session.close()