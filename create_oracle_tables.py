# recreate_tables.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    print("🔄 Creating sequences...")
    
    # Create sequences
    sequences = [
        'CREATE SEQUENCE seq_users START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE seq_medicines START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE seq_suppliers START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE seq_orders START WITH 1 INCREMENT BY 1',
        'CREATE SEQUENCE seq_order_items START WITH 1 INCREMENT BY 1'
    ]
    
    for seq_sql in sequences:
        try:
            db.session.execute(db.text(seq_sql))
            print("✅ Created sequence")
        except Exception as e:
            print(f"⚠️  Sequence: {e}")
    
    db.session.commit()
    print("\n✅ Sequences created!")
    
    print("\n🔄 Creating triggers...")
    
    # Create triggers using text() without parameters
    triggers_sql = """
    CREATE OR REPLACE TRIGGER trg_users_id
    BEFORE INSERT ON users
    FOR EACH ROW
    BEGIN
        IF :NEW.id IS NULL THEN
            :NEW.id := seq_users.NEXTVAL;
        END IF;
    END;
    /
    """
    
    try:
        db.session.execute(db.text(triggers_sql))
        print("✅ Created trigger: trg_users_id")
    except Exception as e:
        print(f"⚠️  Trigger error: {e}")
    
    triggers_sql2 = """
    CREATE OR REPLACE TRIGGER trg_medicines_id
    BEFORE INSERT ON medicines
    FOR EACH ROW
    BEGIN
        IF :NEW.id IS NULL THEN
            :NEW.id := seq_medicines.NEXTVAL;
        END IF;
    END;
    /
    """
    
    try:
        db.session.execute(db.text(triggers_sql2))
        print("✅ Created trigger: trg_medicines_id")
    except Exception as e:
        print(f"⚠️  Trigger error: {e}")
    
    triggers_sql3 = """
    CREATE OR REPLACE TRIGGER trg_suppliers_id
    BEFORE INSERT ON suppliers
    FOR EACH ROW
    BEGIN
        IF :NEW.id IS NULL THEN
            :NEW.id := seq_suppliers.NEXTVAL;
        END IF;
    END;
    /
    """
    
    try:
        db.session.execute(db.text(triggers_sql3))
        print("✅ Created trigger: trg_suppliers_id")
    except Exception as e:
        print(f"⚠️  Trigger error: {e}")
    
    triggers_sql4 = """
    CREATE OR REPLACE TRIGGER trg_orders_id
    BEFORE INSERT ON orders
    FOR EACH ROW
    BEGIN
        IF :NEW.id IS NULL THEN
            :NEW.id := seq_orders.NEXTVAL;
        END IF;
    END;
    /
    """
    
    try:
        db.session.execute(db.text(triggers_sql4))
        print("✅ Created trigger: trg_orders_id")
    except Exception as e:
        print(f"⚠️  Trigger error: {e}")
    
    triggers_sql5 = """
    CREATE OR REPLACE TRIGGER trg_order_items_id
    BEFORE INSERT ON order_items
    FOR EACH ROW
    BEGIN
        IF :NEW.id IS NULL THEN
            :NEW.id := seq_order_items.NEXTVAL;
        END IF;
    END;
    /
    """
    
    try:
        db.session.execute(db.text(triggers_sql5))
        print("✅ Created trigger: trg_order_items_id")
    except Exception as e:
        print(f"⚠️  Trigger error: {e}")
    
    db.session.commit()
    print("\n✅ All triggers created!")