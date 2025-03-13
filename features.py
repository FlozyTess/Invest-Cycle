import datetime
from sqlalchemy.orm import sessionmaker
from db.database import engine
from models import User, GroupMember, Contribution, Payout

Session = sessionmaker(bind=engine)
session = Session()

        # check for missed contributions and defaulters
def check_and_remove_defaulters(group_id):
    members = session.query(GroupMember).filter_by(group_id=group_id, is_active=True).all()  

    for member in members:
        user = session.query(User).filter_by(id=member.user_id).first()  

        # Check if user contributed in the last 30 days
        last_contribution = session.query(Contribution).filter_by(user_id=user.id, group_id=group_id).order_by(Contribution.timestamp.desc()).first()

        if not last_contribution or (datetime.datetime.utcnow() - last_contribution.timestamp).days > 30:
            member.missed_contributions += 1
            user.reliability_score -= 20  # Reduce reliability score
            
            if member.missed_contributions >= 3:
                member.is_active = False
                print(f"{user.name} has been removed from the group due to missed contributions.")
        
        session.commit()

        # To edit group details
def edit_group(group_id):
    group = session.query(Group).filter_by(id=group_id).first()
    
    if not group:
        print(No group found.)
        return

    New_name = input(f"Enter new name (current: {group.name}): ")
    new_amount = input(f"Enter new contribution amount (current: {group.contribution_amount}): ")

    if new_name:
        group.name = new_name
    if new_amount:
        group.contribution_amount = float(new_amount)

    session.commit()
        print("Group updated")


        # deleting a group
def delete_group(group_id):
    group = session.query(Group).filter_by(id=group_id).first()

    if not group:
        print("group does not exist.")
        return
         



