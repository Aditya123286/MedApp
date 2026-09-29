# check_user.py
import sys
sys.path.insert(0, r'C:\medapp\medapp1\food')

from app import app
from database import db
from models.user import User

def check_user():
    with app.app_context():
        user = User.query.filter_by(email='user@medapp.com').first()
        if user:
            print(f"Email: {user.email}")
            print(f"ID: {user.id}")
            print(f"Role ID: {user.role_id}")
            print(f"Role Name: {user.role.name if user.role else 'None'}")
            print(f"Password hash: {user.password[:20]}...")
        else:
            print("User not found!")

if __name__ == '__main__':
    check_user()