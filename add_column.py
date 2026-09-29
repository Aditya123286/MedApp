# check_order_columns.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    result = db.session.execute(db.text("""
        SELECT column_name FROM user_tab_columns 
        WHERE table_name = 'ORDERS'
    """))
    
    print("Order table columns:")
    for row in result:
        print(f"  {row[0]}")