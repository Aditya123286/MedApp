from app import create_app
from models.user import User
from database import db

app = create_app()  
with app.app_context():

    existing_admin = User.find_by_email("admin@gmail.com")

    if not existing_admin:
        admin = User.create({
            "full_name": "Admin",
            "email": "admin@gmail.com",
            "pharmacy_name": "Admin Panel",
            "phone_number": "9999999999",
            "license_number": "ADMIN001",
            "password": "admin123",
            "role": "admin"
        })

        print("✅ Admin Created Successfully")
    else:
        print("⚠ Admin already exists")
