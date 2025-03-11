from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User, Investment

Session = sessionmaker(bind=engine)
session = Session()

#insert sample users
user1 = User(name="Joy",email="joy@outlook.com")
user2 = User(name="Gabby",email="gabby@outlook.com")

session.add_all([user1, user2])
session.commit()
