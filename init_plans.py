# init_plans.py
from app import create_app
from database import db
from models.subscription import SubscriptionPlan
import json

def init_plans():
    app = create_app()
    with app.app_context():
        # Clear existing plans
        SubscriptionPlan.query.delete()
        
        # Create sample plans
        plans = [
            {
                'name': '7 Day Access',
                'description': 'Perfect for trying out our services',
                'price': 99.0,
                'duration_days': 7,
                'features': json.dumps([
                    'Up to 50 medicines',
                    'Up to 25 orders',
                    'Basic support',
                    'Email notifications'
                ]),
                'max_orders': 25,
                'max_medicines': 50,
                'discount_percent': 0,
                'is_active': True
            },
            {
                'name': 'Monthly Premium',
                'description': 'Most popular choice',
                'price': 499.0,
                'duration_days': 30,
                'features': json.dumps([
                    'Unlimited medicines',
                    'Unlimited orders',
                    'Priority support',
                    'Advanced analytics',
                    'Inventory alerts',
                    'Export reports'
                ]),
                'max_orders': None,
                'max_medicines': None,
                'discount_percent': 0,
                'is_active': True
            },
            {
                'name': 'Quarterly Business',
                'description': 'Best value for businesses',
                'price': 1299.0,
                'duration_days': 90,
                'features': json.dumps([
                    'Everything in Monthly',
                    '2 months FREE',
                    'Multi-branch support',
                    'API access',
                    'Dedicated account manager',
                    '24/7 phone support'
                ]),
                'max_orders': None,
                'max_medicines': None,
                'discount_percent': 15,
                'is_active': True
            },
            {
                'name': 'Yearly Enterprise',
                'description': 'Complete solution',
                'price': 4499.0,
                'duration_days': 365,
                'features': json.dumps([
                    'Everything in Quarterly',
                    '4 months FREE',
                    'Custom integrations',
                    'Training sessions',
                    'SLA guarantee',
                    'White-label option'
                ]),
                'max_orders': None,
                'max_medicines': None,
                'discount_percent': 25,
                'is_active': True
            }
        ]
        
        for plan_data in plans:
            plan = SubscriptionPlan(**plan_data)
            db.session.add(plan)
        
        db.session.commit()
        print("✅ Subscription plans created successfully!")
        print("\n📋 Available Plans:")
        for plan in SubscriptionPlan.query.all():
            print(f"   - {plan.name}: ₹{plan.price}/{plan.duration_days} days")

if __name__ == "__main__":
    init_plans()