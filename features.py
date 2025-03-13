import datetime
from sqlalchemy.orm import sessionmaker
from database import engine
from models import User, GroupMember, Contribution, Payout

Session = sessionmaker(bind=engine)
session = Session()

        # check for missed contributions and defaulters
def check_and_remove_defaulters(group_id):
    members = session.query(GroupMember).filter_by(group_id=group_id, is_active=True).all()  

    for member in members:
        user = session.query(User).filter_by(id=member.user_id).first()  