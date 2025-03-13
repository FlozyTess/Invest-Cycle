from sqlalchemy import Column, Integer, String, Float,Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base,relationship
import datetime     # for timestamps 
import bcrypt       # for authentication and password security.

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    reliability_score = Column(Float, default=100.0)  # users start with a perfect score

    def set_password(self, pasword):
        """Hashes the password and stores it."""
        salt = bcrypt.gensalt()     # creates a random salt for added security.
        self.password = bcrypt.hashpw(password.encode('utf-8'), salt)  # hashes the password and stores it.
    
    def check_password(self, password):
        """Checks if the entered password matches the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))     # function used during login to verify password
    
    #relationship
    groups = relationship("GroupMember", back_populates="user")
    contributions = relationship("Contribution", back_populates="user")
    payouts = relationship("Payout", back_populates="user")

class Group(Base):
    __tablename__ = 'groups'     # investment groups are stored.

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    contribution_amount = Column(Float, nullable=False)  # fixed amount per round
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    #relationship
    members = relationship("GroupMember", back_populates="group")


class GroupMember(Base):
    __tablename__ = 'group_members'     # tracks which users belong to which groups.

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    is_active = Column(Boolean, default=True)  # False if user defaults on payments
    missed_contributions = Column(Integer, default=0)  # Track missed payments

    #relationship
    user = relationship("User", back_populates="groups")
    group = relationship("Group", back_populates="members")


class Contribution(Base):
    __tablename__ = 'contributions'     # stores all contributions made by users.

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    #relationship
    user = relationship("User", back_populates="contributions")

class Payout(Base):            
    __tablename__ = 'payouts'    # payout records, tracking which users have received their share.

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    #relationship
    user = relationship("User", back_populates="payouts")