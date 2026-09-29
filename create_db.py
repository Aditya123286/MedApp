# create_db.py
import os
from app import create_app
from database import db

# App create karein
app = create_app('development')

# Database context mein tables create karein
with app.app_context():
    # PEHLE PURANI TABLES DROP KAREIN
    print("🔄 Dropping old tables...")
    db.drop_all()
    print("✅ Old tables dropped")
    
    # NAYI TABLES CREATE KAREIN
    print("🔄 Creating new tables...")
    db.create_all()
    print("✅ Database 'medapp.db' created successfully!")
    print("✅ All tables created!")
    
    # Tables verify
    print("\n📋 Tables created:")
    print("  - user")
    print("  - medicines")
    print("  - suppliers")
    print("  - order")