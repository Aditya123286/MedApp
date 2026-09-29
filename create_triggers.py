# create_trigger_raw.py
import oracledb
import os

# Get connection string from environment or config
dsn = oracledb.makedsn("localhost", 1521, service_name="XE")
username = "system"
password = "1234"  # Your Oracle password

try:
    print("Connecting to Oracle...")
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    print("✅ Connected!")
    
    cursor = connection.cursor()
    
    # Drop old trigger if exists
    try:
        cursor.execute("DROP TRIGGER trg_orders_id")
        print("✅ Old trigger dropped")
    except:
        print("No old trigger")
    
    # Create trigger
    cursor.execute("""
        CREATE OR REPLACE TRIGGER trg_orders_id
        BEFORE INSERT ON orders
        FOR EACH ROW
        BEGIN
            IF :NEW.id IS NULL THEN
                SELECT seq_orders.NEXTVAL INTO :NEW.id FROM DUAL;
            END IF;
        END;
    """)
    print("✅ Trigger created!")
    
    # Also do for order_items
    try:
        cursor.execute("DROP TRIGGER trg_order_items_id")
    except:
        pass
    
    cursor.execute("""
        CREATE OR REPLACE TRIGGER trg_order_items_id
        BEFORE INSERT ON order_items
        FOR EACH ROW
        BEGIN
            IF :NEW.id IS NULL THEN
                SELECT seq_order_items.NEXTVAL INTO :NEW.id FROM DUAL;
            END IF;
        END;
    """)
    print("✅ Order items trigger created!")
    
    connection.commit()
    cursor.close()
    connection.close()
    
    print("\n🎉 All done!")
    
except Exception as e:
    print(f"Error: {e}")