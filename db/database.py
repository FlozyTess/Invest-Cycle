from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base 

# Create database connection
engine = create_engine('sqlite:///db/investcycle.db')