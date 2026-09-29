# add_image_url_column.py
from app import create_app
from database import db
from models.medicine import Medicine

app = create_app('development')

with app.app_context():
    try:
        # Add image_url column if it doesn't exist
        db.session.execute(db.text("""
            ALTER TABLE medicines ADD (
                image_url VARCHAR2(500)
            )
        """))
        db.session.commit()
        print("✅ image_url column added successfully!")
    except Exception as e:
        # If column already exists, ignore error
        if "ORA-01430" in str(e):
            print("ℹ️  image_url column already exists")
        else:
            print(f"Error: {e}")
        db.session.rollback()