# drop_all_tables.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    print("🔄 Dropping all tables with CASCADE CONSTRAINTS...")
    
    # List of all tables in order (child tables first)
    tables = [
        'order_items',
        'orders', 
        'prescriptions',
        'chat_conversations',
        'medicines',
        'suppliers',
        'users'
    ]
    
    for table in tables:
        try:
            # Drop table with CASCADE CONSTRAINTS
            db.session.execute(db.text(f"DROP TABLE {table} CASCADE CONSTRAINTS"))
            print(f"✅ Dropped: {table}")
        except Exception as e:
            # Table might not exist
            print(f"⚠️  {table}: {str(e)[:50]}")
    
    # Also drop sequences
    sequences = [
        'seq_users',
        'seq_medicines',
        'seq_suppliers',
        'seq_orders',
        'seq_order_items',
        'seq_prescriptions'
    ]
    
    print("\n🔄 Dropping sequences...")
    for seq in sequences:
        try:
            db.session.execute(db.text(f"DROP SEQUENCE {seq}"))
            print(f"✅ Dropped sequence: {seq}")
        except Exception as e:
            print(f"⚠️  Sequence {seq}: {str(e)[:50]}")
    
    db.session.commit()
    print("\n✅ All tables and sequences dropped!")