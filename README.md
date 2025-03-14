# InvestCycle
### Invest Cycle is a command-line application that facilitates group-based savings and investment cycles. Users can create and join groups, make contributions, and assign payouts in a secure and structured way.

#  Features
### User Authentication
   1. Sign Up – Users can register an account. 
   2. Log In – Users can securely log in with password hashing.

### User Profile
   1. View Profile – Users can see their details, balance, and reliability score.

### Group Management
   1. Create a Group – Users can create investment groups.
   2. Join a Group – Users can join an existing group.

### Contributions & Payouts
   1. Add Contribution – Users can contribute money to their group.
   2. Assign Payouts – The system assigns payouts to members based on a structured cycle.

#  Installation & Setup
##  Prerequisites
###   Ensure you have Python 3.8+ installed and the following dependencies:
    `pip install bcrypt sqlalchemy`

## Cloning the Repository
    
    `git clone https://github.com/your-repo/invest-cycle.git`
    `cd invest-cycle`

## Database Setup
### Make sure the database is configured correctly:
  1. Navigate to db/database.py and ensure the correct database engine is set.
  2. Run migrations if necessary.

## How to Run
### To start the CLI application, run:
        `python cli.py`
### You’ll be presented with a menu to sign up, log in, and interact with the system.

# Usage Guide
1. Sign Up – Create an account by providing a name, email, and password.
2. Log In – Enter your credentials to access your profile.
3. View Profile – Check your balance and reliability score.
4. Create a Group – Start a new investment group.
5. Join a Group – Join an existing group to contribute.
6. Make Contributions – Add money to your group.
7. Receive Payouts – Check assigned payouts.

# Technologies Used
1. Python 3 – Core programming language
2. SQLAlchemy – ORM for database handling
3. bcrypt – Secure password hashing

# Contributing
1. Fork the repository.
2. Create a new branch (feature-branch).
3. Commit your changes.
4. Push to GitHub and create a pull request.

# License
  ### MIT License.


