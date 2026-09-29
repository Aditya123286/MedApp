# database.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os

db = SQLAlchemy()


def _ensure_orders_schema_compatibility(use_oracle):
    """Ensure legacy tables have columns required by current models."""
    try:
        if use_oracle:
            table_exists = db.session.execute(
                text("SELECT COUNT(*) FROM user_tables WHERE table_name = 'ORDERS'")
            ).scalar()
            if not table_exists:
                return

            def oracle_column_exists(table_name, column_name):
                return db.session.execute(
                    text(
                        "SELECT COUNT(*) FROM user_tab_columns "
                        "WHERE table_name = :table_name AND column_name = :column_name"
                    ),
                    {'table_name': table_name, 'column_name': column_name}
                ).scalar()

            order_columns = [
                ('DELIVERED_AT', "ALTER TABLE ORDERS ADD (DELIVERED_AT TIMESTAMP NULL)"),
                ('ASSIGNED_SUPPLIER_ID', "ALTER TABLE ORDERS ADD (ASSIGNED_SUPPLIER_ID NUMBER NULL)"),
                ('ASSIGNED_SUPPLIER_NAME', "ALTER TABLE ORDERS ADD (ASSIGNED_SUPPLIER_NAME VARCHAR2(200) NULL)"),
                ('HUB_STATUS', "ALTER TABLE ORDERS ADD (HUB_STATUS VARCHAR2(30) DEFAULT 'unassigned')"),
                ('HUB_NOTES', "ALTER TABLE ORDERS ADD (HUB_NOTES CLOB NULL)")
            ]
            for column_name, ddl in order_columns:
                if not oracle_column_exists('ORDERS', column_name):
                    db.session.execute(text(ddl))
                    db.session.commit()
                    print(f"[MIGRATION] Added ORDERS.{column_name}")

            supplier_exists = db.session.execute(
                text("SELECT COUNT(*) FROM user_tables WHERE table_name = 'SUPPLIERS'")
            ).scalar()
            if supplier_exists:
                supplier_columns = [
                    ('CITY', "ALTER TABLE SUPPLIERS ADD (CITY VARCHAR2(100) NULL)"),
                    ('STATE', "ALTER TABLE SUPPLIERS ADD (STATE VARCHAR2(100) NULL)"),
                    ('PINCODE', "ALTER TABLE SUPPLIERS ADD (PINCODE VARCHAR2(10) NULL)"),
                    ('IS_PHARMACY_PARTNER', "ALTER TABLE SUPPLIERS ADD (IS_PHARMACY_PARTNER NUMBER(1) DEFAULT 1)"),
                    ('IS_ACTIVE', "ALTER TABLE SUPPLIERS ADD (IS_ACTIVE NUMBER(1) DEFAULT 1)"),
                    ('PRIORITY_RANK', "ALTER TABLE SUPPLIERS ADD (PRIORITY_RANK NUMBER DEFAULT 100)")
                ]
                for column_name, ddl in supplier_columns:
                    if not oracle_column_exists('SUPPLIERS', column_name):
                        db.session.execute(text(ddl))
                        db.session.commit()
                        print(f"[MIGRATION] Added SUPPLIERS.{column_name}")
        else:
            table_exists = db.session.execute(
                text("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='orders'")
            ).scalar()
            if not table_exists:
                return

            columns = db.session.execute(text("PRAGMA table_info(orders)")).fetchall()
            column_names = {str(row[1]).lower() for row in columns}

            order_columns = [
                ('delivered_at', "ALTER TABLE orders ADD COLUMN delivered_at DATETIME"),
                ('assigned_supplier_id', "ALTER TABLE orders ADD COLUMN assigned_supplier_id INTEGER"),
                ('assigned_supplier_name', "ALTER TABLE orders ADD COLUMN assigned_supplier_name TEXT"),
                ('hub_status', "ALTER TABLE orders ADD COLUMN hub_status TEXT DEFAULT 'unassigned'"),
                ('hub_notes', "ALTER TABLE orders ADD COLUMN hub_notes TEXT")
            ]
            for col_name, ddl in order_columns:
                if col_name not in column_names:
                    db.session.execute(text(ddl))
                    db.session.commit()
                    print(f"[MIGRATION] Added orders.{col_name}")

            supplier_exists = db.session.execute(
                text("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='suppliers'")
            ).scalar()
            if supplier_exists:
                supplier_columns = db.session.execute(text("PRAGMA table_info(suppliers)")).fetchall()
                supplier_column_names = {str(row[1]).lower() for row in supplier_columns}
                supplier_additions = [
                    ('city', "ALTER TABLE suppliers ADD COLUMN city TEXT"),
                    ('state', "ALTER TABLE suppliers ADD COLUMN state TEXT"),
                    ('pincode', "ALTER TABLE suppliers ADD COLUMN pincode TEXT"),
                    ('is_pharmacy_partner', "ALTER TABLE suppliers ADD COLUMN is_pharmacy_partner INTEGER DEFAULT 1"),
                    ('is_active', "ALTER TABLE suppliers ADD COLUMN is_active INTEGER DEFAULT 1"),
                    ('priority_rank', "ALTER TABLE suppliers ADD COLUMN priority_rank INTEGER DEFAULT 100")
                ]
                for col_name, ddl in supplier_additions:
                    if col_name not in supplier_column_names:
                        db.session.execute(text(ddl))
                        db.session.commit()
                        print(f"[MIGRATION] Added suppliers.{col_name}")
    except Exception as e:
        db.session.rollback()
        print(f"[WARN] Schema compatibility check failed: {e}")


def init_oracle_connection(app):
    """Initialize Oracle database connection."""

    # Check if already initialized
    if app.extensions.get('sqlalchemy'):
        print("[WARN] SQLAlchemy already initialized")
        return

    # Get Oracle config
    username = os.getenv('ORACLE_USER', 'system')
    password = os.getenv('ORACLE_PASSWORD', '1234')
    host = os.getenv('ORACLE_HOST', 'localhost')
    port = os.getenv('ORACLE_PORT', '1521')
    service_name = os.getenv('ORACLE_SERVICE', 'XE')
    oracle_dsn = os.getenv('ORACLE_DSN', f'{host}:{port}/{service_name}')

    connection_string = None
    use_oracle = False

    try:
        # Try Oracle connection
        connection_string = f"oracle+oracledb://{username}:{password}@{oracle_dsn}"
        print(f"[INFO] Trying Oracle: {oracle_dsn}")

        # Test connection
        from sqlalchemy import create_engine
        test_engine = create_engine(connection_string)
        with test_engine.connect() as conn:
            conn.execute(text("SELECT 1 FROM DUAL"))

        print("[OK] Oracle connected successfully!")
        use_oracle = True

    except Exception as e:
        print(f"[ERROR] Oracle failed: {str(e)[:80]}")
        connection_string = "sqlite:///medapp.db"
        print("[WARN] Using SQLite fallback")

    # Set config
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Test query and run lightweight compatibility migration
    with app.app_context():
        if use_oracle:
            db.session.execute(text("SELECT 1 FROM DUAL"))
        else:
            db.session.execute(text("SELECT 1"))

        _ensure_orders_schema_compatibility(use_oracle)
        print("[OK] Database ready!")


def get_engine():
    from flask import current_app
    return db.get_engine(current_app)


def get_session():
    return db.session


def create_tables():
    from flask import current_app
    with current_app.app_context():
        db.create_all()
