# check_medicines.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    print("🔄 Checking medicines...")
    
    # Check table structure
    try:
        result = db.session.execute(db.text("""
            SELECT column_name, data_type 
            FROM user_tab_columns 
            WHERE table_name = 'MEDICINES'
            ORDER BY column_id
        """))
        
        print("\n📋 Medicines table structure:")
        for row in result:
            print(f"  {row[0]}: {row[1]}")
    except Exception as e:
        print(f"⚠️  Table check: {e}")
    
    # Check if medicines exist
    try:
        result = db.session.execute(db.text("SELECT COUNT(*) FROM medicines"))
        count = result.scalar()
        print(f"\n📦 Total medicines in DB: {count}")
        
        if count > 0:
            result = db.session.execute(db.text("SELECT id, name, price, quantity FROM medicines"))
            print("\n📋 Existing medicines:")
            for row in result:
                print(f"  - {row[0]}: {row[1]} (₹{row[2]}, Qty: {row[3]})")
        else:
            print("\n❌ No medicines found!")
            
    except Exception as e:
        print(f"⚠️  Query: {e}")