from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User, Investment

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

# Fetch users from DB to ensure correct user IDs
user1 = session.query(User).filter_by(email="joy@outlook.com").first()
user2 = session.query(User).filter_by(email="gabby@gmail.com").first()    

#Add Investments
investment1 = Investment(user_id=1, amount=2000.80, name="Stock")
investment2 = Investment(user_id=2, amount=1000.50, name="Crypto")

session.add_all([investment1, investment2])
session.commit()

print("data inserted successfully!")

session.close()