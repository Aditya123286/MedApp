# fix_subscription.py
from app import create_app
from database import db

app = create_app('development')

with app.app_context():
    print("🔄 Checking/Adding subscription tables...")
    
    # Import models to register them
    from models.subscription import SubscriptionPlan, UserSubscription
    
    # Create tables
    try:
        db.create_all()
        print("✅ Tables created/verified!")
    except Exception as e:
        print(f"⚠️  Table creation: {e}")
    
    # Check if plans exist
    print("\n🔄 Checking subscription plans...")
    
    plans = SubscriptionPlan.query.all()
    
    if len(plans) == 0:
        print("❌ No plans found. Adding default plans...")
        
        plans_data = [
            {
                'name': 'Free',
                'plan_type': 'free',
                'description': 'Basic access for all users',
                'price': 0,
                'duration_days': 30,
                'discount_percentage': 0,
                'free_delivery': False,
                'express_delivery': False,
                'priority_support': False,
                'free_prescriptions': False,
                'max_free_orders': 0
            },
            {
                'name': 'Bronze',
                'plan_type': 'bronze',
                'description': 'Perfect for occasional buyers',
                'price': 99,
                'duration_days': 30,
                'discount_percentage': 5,
                'free_delivery': False,
                'express_delivery': False,
                'priority_support': False,
                'free_prescriptions': False,
                'max_free_orders': 1
            },
            {
                'name': 'Silver',
                'plan_type': 'silver',
                'description': 'Great for regular medicine needs',
                'price': 199,
                'duration_days': 30,
                'discount_percentage': 10,
                'free_delivery': True,
                'express_delivery': False,
                'priority_support': False,
                'free_prescriptions': False,
                'max_free_orders': 2
            },
            {
                'name': 'Gold',
                'plan_type': 'gold',
                'description': 'Best value for families',
                'price': 399,
                'duration_days': 30,
                'discount_percentage': 15,
                'free_delivery': True,
                'express_delivery': True,
                'priority_support': True,
                'free_prescriptions': True,
                'max_free_orders': 5
            },
            {
                'name': 'Platinum',
                'plan_type': 'platinum',
                'description': 'Premium healthcare experience',
                'price': 799,
                'duration_days': 30,
                'discount_percentage': 25,
                'free_delivery': True,
                'express_delivery': True,
                'priority_support': True,
                'free_prescriptions': True,
                'max_free_orders': 999
            },
        ]
        
        for p in plans_data:
            plan = SubscriptionPlan(**p)
            db.session.add(plan)
        
        db.session.commit()
        print("✅ Plans added successfully!")
    
    # Show all plans
    print("\n" + "="*50)
    print("📋 AVAILABLE SUBSCRIPTION PLANS")
    print("="*50)
    
    all_plans = SubscriptionPlan.query.order_by(SubscriptionPlan.price.asc()).all()
    for i, p in enumerate(all_plans, 1):
        print(f"\n{i}. {p.name} Plan")
        print(f"   💰 Price: ₹{p.price}/month")
        print(f"   📝 {p.description}")
        features = []
        if p.discount_percentage > 0:
            features.append(f"{p.discount_percentage}% discount")
        if p.free_delivery:
            features.append("Free Delivery")
        if p.express_delivery:
            features.append("Express Delivery")
        if p.priority_support:
            features.append("Priority Support")
        if p.free_prescriptions:
            features.append("Free Prescriptions")
        if p.max_free_orders > 0:
            features.append(f"{p.max_free_orders} free orders/month")
        
        if features:
            print(f"   ✨ Features: {', '.join(features)}")
    
    print("\n" + "="*50)