# check_plans.py
from app import create_app
from models.subscription import SubscriptionPlan

def check_plans():
    app = create_app()
    with app.app_context():
        plans = SubscriptionPlan.query.all()
        print(f"📊 Total plans in database: {len(plans)}")
        
        if plans:
            print("\n✅ Plans found:")
            for plan in plans:
                print(f"   • ID: {plan.id}, Name: {plan.name}, Price: ₹{plan.price}, Active: {plan.is_active}")
        else:
            print("\n❌ No plans found in database!")

if __name__ == "__main__":
    check_plans()