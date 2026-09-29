# check_my_order.py
from app import create_app
from models.order import Order, OrderItem

def check_recent_order():
    app = create_app()
    
    with app.app_context():
        # Get the most recent order
        order = Order.query.order_by(Order.created_at.desc()).first()
        
        if order:
            print("\n" + "="*50)
            print("📦 MOST RECENT ORDER FOUND!")
            print("="*50)
            print(f"Order ID: {order.id}")
            print(f"Order Number: {order.order_number}")
            print(f"Customer: {order.customer_name}")
            print(f"Amount: ₹{order.total_amount}")
            print(f"Status: {order.status}")
            print(f"Created: {order.created_at}")
            
            # Check items
            items = OrderItem.query.filter_by(order_id=order.id).all()
            if items:
                print(f"\n📋 Items ({len(items)}):")
                for item in items:
                    print(f"   • {item.medicine_name} x{item.quantity} = ₹{item.total}")
            else:
                print("\n❌ No items found for this order!")
        else:
            print("❌ No orders found in database!")

if __name__ == "__main__":
    check_recent_order()