# add_subscription.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    print("🔄 Adding subscription tables...")
    
    try:
        # Create subscription_plans table
        db.session.execute(db.text("""
            CREATE TABLE subscription_plans (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                name VARCHAR2(100) NOT NULL,
                plan_type VARCHAR2(20) NOT NULL,
                description CLOB,
                price NUMBER NOT NULL,
                duration_days NUMBER DEFAULT 30,
                discount_percentage NUMBER DEFAULT 0,
                free_delivery NUMBER(1) DEFAULT 0,
                express_delivery NUMBER(1) DEFAULT 0,
                priority_support NUMBER(1) DEFAULT 0,
                free_prescriptions NUMBER(1) DEFAULT 0,
                max_free_orders NUMBER DEFAULT 0,
                is_active NUMBER(1) DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        print("✅ subscription_plans table created")
    except Exception as e:
        print(f"⚠️  subscription_plans: {str(e)[:50]}")
    
    try:
        # Create user_subscriptions table
        db.session.execute(db.text("""
            CREATE TABLE user_subscriptions (
                id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                user_id NUMBER NOT NULL,
                plan_id NUMBER NOT NULL,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP NOT NULL,
                status VARCHAR2(20) DEFAULT 'active',
                auto_renew NUMBER(1) DEFAULT 0,
                payment_method VARCHAR2(50),
                transaction_id VARCHAR2(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        print("✅ user_subscriptions table created")
    except Exception as e:
        print(f"⚠️  user_subscriptions: {str(e)[:50]}")
    
    # Insert plans
    plans = [
        ('Free', 'free', 'Basic access for all users', 0, 30, 0, 0, 0, 0, 0, 0),
        ('Bronze', 'bronze', 'Perfect for occasional buyers', 99, 30, 5, 0, 0, 0, 0, 1),
        ('Silver', 'silver', 'Great for regular medicine needs', 199, 30, 10, 1, 0, 0, 0, 2),
        ('Gold', 'gold', 'Best value for families', 399, 30, 15, 1, 1, 1, 1, 5),
        ('Platinum', 'platinum', 'Premium healthcare experience', 799, 30, 25, 1, 1, 1, 1, 999),
    ]
    
    try:
        for p in plans:
            db.session.execute(db.text("""
                INSERT INTO subscription_plans (name, plan_type, description, price, duration_days, 
                discount_percentage, free_delivery, express_delivery, priority_support, 
                free_prescriptions, max_free_orders)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)
            """), p)
        db.session.commit()
        print("✅ Plans added!")
    except Exception as e:
        print(f"⚠️  Insert plans: {str(e)[:50]}")
        db.session.rollback()
    
    # Show plans
    try:
        result = db.session.execute(db.text("SELECT name, price FROM subscription_plans ORDER BY price"))
        print("\n📋 Available Plans:")
        for row in result:
            print(f"   {row[0]} - ₹{row[1]}/month")
    except:
        pass
    
    print("\n✅ DONE!")