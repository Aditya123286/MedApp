# add_tenant_column_fixed.py
from app import create_app
from database import db
from sqlalchemy import text

app = create_app('development')

with app.app_context():
    try:
        print("="*60)
        print("🔧 ADDING TENANT_ID COLUMN TO USERS TABLE")
        print("="*60)
        
        # First, check if table exists using correct Oracle view
        print("\n📋 Checking if USERS table exists...")
        result = db.session.execute(text("""
            SELECT COUNT(*) FROM user_tables WHERE table_name = 'USERS'
        """))
        table_exists = result.scalar()
        
        if not table_exists:
            print("❌ USERS table does not exist!")
            print("   Available tables:")
            tables = db.session.execute(text("SELECT table_name FROM user_tables"))
            for table in tables:
                print(f"   - {table[0]}")
            exit()
        
        print("✅ USERS table exists")
        
        # Check if TENANT_ID column already exists
        print("\n🔍 Checking if TENANT_ID column exists...")
        try:
            # Method 1: Check using all_tab_columns (safer)
            result = db.session.execute(text("""
                SELECT COUNT(*) FROM all_tab_columns 
                WHERE table_name = 'USERS' AND column_name = 'TENANT_ID'
            """))
            col_exists = result.scalar()
        except:
            # Method 2: Try to query the column
            try:
                db.session.execute(text("SELECT TENANT_ID FROM USERS WHERE ROWNUM = 1"))
                col_exists = True
            except:
                col_exists = False
        
        if col_exists:
            print("✅ TENANT_ID column already exists")
        else:
            print("➕ Adding TENANT_ID column...")
            
            # Add the column
            db.session.execute(text("""
                ALTER TABLE USERS ADD TENANT_ID VARCHAR2(50)
            """))
            db.session.commit()
            print("✅ TENANT_ID column added successfully")
        
        # Show table structure
        print("\n📋 Current USERS table structure:")
        columns = db.session.execute(text("""
            SELECT column_name, data_type, nullable 
            FROM user_tab_columns 
            WHERE table_name = 'USERS'
            ORDER BY column_id
        """))
        
        for col in columns:
            nullable = "NULL" if col[2] == "Y" else "NOT NULL"
            print(f"   - {col[0]:20} {col[1]:15} {nullable}")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if you have permission to alter tables")
        print("   2. Verify you're using the correct schema")
        print("   3. Try running as a user with DBA privileges")
    
    print("\n" + "="*60)