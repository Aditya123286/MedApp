from app import create_app
from database import db
from sqlalchemy import text


app = create_app('development')


def is_oracle():
    engine_name = db.engine.url.get_backend_name()
    return engine_name.startswith('oracle')


with app.app_context():
    try:
        if is_oracle():
            table_exists = db.session.execute(
                text("SELECT COUNT(*) FROM user_tables WHERE table_name = 'ORDERS'")
            ).scalar()
            if not table_exists:
                print("ORDERS table not found")
            else:
                col_exists = db.session.execute(
                    text(
                        "SELECT COUNT(*) FROM user_tab_columns "
                        "WHERE table_name = 'ORDERS' AND column_name = 'DELIVERED_AT'"
                    )
                ).scalar()
                if col_exists:
                    print("DELIVERED_AT column already exists")
                else:
                    db.session.execute(text("ALTER TABLE ORDERS ADD (DELIVERED_AT TIMESTAMP NULL)"))
                    db.session.commit()
                    print("Added DELIVERED_AT column to ORDERS")
        else:
            table_exists = db.session.execute(
                text("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='orders'")
            ).scalar()
            if not table_exists:
                print("orders table not found")
            else:
                columns = db.session.execute(text("PRAGMA table_info(orders)")).fetchall()
                names = {str(row[1]).lower() for row in columns}
                if 'delivered_at' in names:
                    print("delivered_at column already exists")
                else:
                    db.session.execute(text("ALTER TABLE orders ADD COLUMN delivered_at DATETIME"))
                    db.session.commit()
                    print("Added delivered_at column to orders")
    except Exception as e:
        db.session.rollback()
        print(f"Migration failed: {e}")
