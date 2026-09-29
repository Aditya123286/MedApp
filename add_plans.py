# create_customer_users.py
from app import create_app
from models.user import User
from database import db

app = create_app()

with app.app_context():
    print("="*60)
    print("🔧 CREATING MISSING CUSTOMER USERS")
    print("="*60)
    
    try:
        # Customer 1 Users
        customer1_users = [
            {
                'email': 'admin@customer1.com',
                'password': 'Admin@123',
                'name': 'Admin Customer 1',
                'role': 'admin',
                'tenant_id': 2
            },
            {
                'email': 'user@customer1.com',
                'password': 'User@123',
                'name': 'User Customer 1',
                'role': 'user',
                'tenant_id': 2
            }
        ]
        
        # Customer 2 Users
        customer2_users = [
            {
                'email': 'admin@customer2.com',
                'password': 'Admin@123',
                'name': 'Admin Customer 2',
                'role': 'admin',
                'tenant_id': 3
            },
            {
                'email': 'user@customer2.com',
                'password': 'User@123',
                'name': 'User Customer 2',
                'role': 'user',
                'tenant_id': 3
            }
        ]
        
        all_users = customer1_users + customer2_users
        
        for user_data in all_users:
            existing = User.query.filter_by(email=user_data['email']).first()
            
            if existing:
                print(f"⚠️ User {user_data['email']} already exists")
                continue
            
            user = User(
                user_id=f"U{User.query.count() + 1:03d}",
                name=user_data['name'],
                email=user_data['email'],
                role=user_data['role'],
                is_active=True,
                tenant_id=user_data['tenant_id']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            db.session.commit()
            
            print(f"✅ Created user: {user_data['email']} (Tenant ID: {user_data['tenant_id']})")
        
        # Verify
        print("\n" + "="*60)
        print("📊 VERIFICATION")
        print("="*60)
        
        users = User.query.all()
        print(f"\n👥 Total Users: {len(users)}")
        for user in users:
            tenant = user.tenant
            tenant_name = tenant.name if tenant else "Default"
            print(f"   • {user.email} ({user.role}) - Tenant: {tenant_name}")
        
        print("\n" + "="*60)
        print("✅ Users Created Successfully!")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()