# test_models.py
import sys
sys.path.insert(0, '.')

print("🔄 Testing all models...")

try:
    from models.user import User
    print("✅ User imported")
except Exception as e:
    print(f"❌ User: {e}")

try:
    from models.order import Order, OrderItem
    print("✅ Order and OrderItem imported")
except Exception as e:
    print(f"❌ Order/OrderItem: {e}")

try:
    from models.medicine import Medicine
    print("✅ Medicine imported")
except Exception as e:
    print(f"❌ Medicine: {e}")

try:
    from models.subscription import SubscriptionPlan, UserSubscription
    print("✅ Subscription models imported")
except Exception as e:
    print(f"❌ Subscription: {e}")

print("\n🎉 All tests complete!")