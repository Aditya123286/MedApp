# check_medicines_table.py
from app import create_app
from database import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Check if medicines table exists
        result = db.session.execute(text("SELECT table_name FROM user_tables WHERE table_name = 'MEDICINES'"))
        if result.fetchone():
            print("✅ Medicines table exists")
            
            # Try to query
            from models.medicine import Medicine
            count = Medicine.query.count()
            print(f"✅ Total medicines: {count}")
        else:
            print("❌ Medicines table does not exist!")
            
            # Create tables
            db.create_all()
            print("✅ Tables created")
            
    except Exception as e:
        print(f"❌ Database error: {e}")