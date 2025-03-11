from sqlalchemy import Column, Integer, String, Float,Boolean, ForeignKey, DateTime
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

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    contribution_amount = Column(Float, nullable=False)  # Fixed amount per round
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    #relationship
    members = relationship("GroupMember", back_populates="group")


class GroupMember(Base):
    __tablename__ = 'group_members'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    is_active = Column(Boolean, default=True)  # False if user defaults on payments
    
    #relationship
    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="members")


class Contribution(Base):
    __tablename__ = 'contributions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    #relationship
    user = relationship("User", back_populates="contributions")

class Payout(Base):
    __tablename__ = 'payouts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    #relationship
    user = relationship("User", back_populates="payouts")