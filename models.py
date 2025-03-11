from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0.0)
    reliability_score = Column(Float, default=100.0)  # Users start with a perfect score

#relationship
    groups = relationship("GroupMember", back_populates="user")
    contributions = relationship("Contribution", back_populates="user")
    payouts = relationship("Payout", back_populates="user")

class Contribution(Base):
    __tablename__ = 'contributions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
#relationship
    user = relationship("User", back_populates="contributions")
