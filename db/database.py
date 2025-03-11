from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base 

# Create database connection
engine = create_engine('sqlite:///db/investcycle.db')

Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)