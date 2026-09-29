# recreate_suppliers.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    print("🔄 Recreating suppliers table...")
    
    try:
        # Drop existing table
        db.session.execute(db.text("DROP TABLE suppliers CASCADE CONSTRAINTS"))
        print("✅ Table dropped!")
    except Exception as e:
        print(f"⚠️  Drop: {e}")
    
    try:
        # Create new table with identity column
        db.session.execute(db.text("""
            CREATE TABLE suppliers (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name VARCHAR2(200) NOT NULL,
                contact_person VARCHAR2(100),
                email VARCHAR2(120),
                phone VARCHAR2(20),
                address CLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        print("✅ Table created with auto-increment!")
    except Exception as e:
        print(f"⚠️  Create: {e}")
    
    db.session.commit()
    print("\n✅ DONE!")