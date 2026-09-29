# drop_sequences.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    print("🔄 Dropping sequences...")
    
    sequences = ['seq_users', 'seq_medicines', 'seq_suppliers', 'seq_orders', 'seq_order_items']
    
    for seq in sequences:
        try:
            db.session.execute(db.text(f"DROP SEQUENCE {seq}"))
            print(f"✅ Dropped sequence: {seq}")
        except Exception as e:
            print(f"⚠️  Could not drop {seq}: {e}")
    
    db.session.commit()
    print("\n✅ Sequences dropped!")