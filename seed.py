from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User, Investment

Session = sessionmaker(bind=engine)
session = Session()

#Add users
user1 = User(name="Joy",email="joy@outlook.com")
user2 = User(name="Gabby",email="gabby@outlook.com")

session.add_all([user1, user2])
session.commit()

#Add Investments
investment1 = Investment(user_id=1, amount=2000.80, investment_type="Stock")
investment2 = Investment(user_id=2, amount=1000.50, investment_type="Crypto")

session.add_all([investment1, investment2])
session.commit()