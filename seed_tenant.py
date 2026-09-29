# seed_tenant_fixed.py
from app import create_app
from models.tenant import Tenant, TenantConfig
from models.user import User
from database import db

app = create_app()

with app.app_context():
    print("="*60)
    print("🔧 CREATING TENANTS AND USERS")
    print("="*60)
    
    try:
        # First, check existing tenants
        existing_tenants = Tenant.query.all()
        print(f"\n📋 Existing tenants: {len(existing_tenants)}")
        
        existing_ids = [t.id for t in existing_tenants]
        if existing_ids:
            print(f"   Existing IDs: {existing_ids}")
        
        # Get next available ID
        def get_next_id():
            if not existing_ids:
                return 1
            return max(existing_ids) + 1
        
        # Create default tenant if not exists
        default_tenant = Tenant.query.filter_by(subdomain='default').first()
        if not default_tenant:
            default_id = get_next_id()
            print(f"\n➕ Creating default tenant with ID: {default_id}")
            
            default_tenant = Tenant(
                id=default_id,
                name="Default Tenant",
                subdomain="default",
                custom_domain=None,
                is_active=True
            )
            db.session.add(default_tenant)
            db.session.commit()
            print(f"✅ Created default tenant (ID: {default_id})")
            existing_ids.append(default_id)
        else:
            print(f"\n✅ Default tenant already exists (ID: {default_tenant.id})")
        
        # Customer tenants data
        customers = [
            {
                'name': 'Customer 1',
                'subdomain': 'customer1',
                'domain': 'customer1.com',
                'theme': '#2e5bff',
                'company': 'Customer 1 Pharmacy',
                'email': 'support@customer1.com'
            },
            {
                'name': 'Customer 2',
                'subdomain': 'customer2',
                'domain': 'customer2.com',
                'theme': '#10b981',
                'company': 'Customer 2 Medical',
                'email': 'support@customer2.com'
            },
        ]
        
        # Create customer tenants
        for cust in customers:
            existing = Tenant.query.filter_by(subdomain=cust['subdomain']).first()
            if existing:
                print(f"\n✅ Tenant {cust['name']} already exists (ID: {existing.id})")
                continue
            
            next_id = get_next_id()
            print(f"\n➕ Creating {cust['name']} with ID: {next_id}")
            
            tenant = Tenant(
                id=next_id,
                name=cust['name'],
                subdomain=cust['subdomain'],
                custom_domain=cust['domain'],
                is_active=True
            )
            db.session.add(tenant)
            db.session.commit()
            
            # Create tenant config
            config = TenantConfig(
                id=next_id,
                tenant_id=tenant.id,
                logo_url=None,
                theme_color=cust['theme'],
                company_name=cust['company'],
                support_email=cust['email']
            )
            db.session.add(config)
            db.session.commit()
            
            print(f"✅ Created {cust['name']} (ID: {next_id})")
            existing_ids.append(next_id)
            
            # Create users for this tenant
            users = [
                {
                    'email': f"admin@{cust['subdomain']}.com",
                    'password': 'Admin@123',
                    'name': f"Admin {cust['name']}",
                    'role': 'admin'
                },
                {
                    'email': f"user@{cust['subdomain']}.com",
                    'password': 'User@123',
                    'name': f"User {cust['name']}",
                    'role': 'user'
                }
            ]
            
            for user_data in users:
                existing_user = User.query.filter_by(email=user_data['email']).first()
                if existing_user:
                    print(f"   ⚠️ User {user_data['email']} already exists")
                    continue
                
                user = User(
                    user_id=f"U{User.query.count() + 1:03d}",
                    name=user_data['name'],
                    email=user_data['email'],
                    role=user_data['role'],
                    is_active=True,
                    tenant_id=tenant.id
                )
                user.set_password(user_data['password'])
                db.session.add(user)
                db.session.commit()
                print(f"   ✅ Created user: {user_data['email']}")
        
        # Summary
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        
        tenants = Tenant.query.all()
        users = User.query.all()
        print(f"\n🏢 Tenants: {len(tenants)}")
        for t in tenants:
            print(f"   • {t.name} (ID: {t.id}) - {t.subdomain}")
        
        print(f"\n👥 Users: {len(users)}")
        for u in users:
            tenant = u.tenant
            print(f"   • {u.email} ({u.role}) - Tenant: {tenant.name if tenant else 'Default'}")
        
        print("\n🔑 LOGIN CREDENTIALS:")
        for u in users:
            password = 'Admin@123' if u.role == 'admin' else 'User@123'
            tenant_name = u.tenant.name if u.tenant else 'Default'
            print(f"   {u.email} / {password} ({tenant_name})")
        
    except Exception as e:
        db.session.rollback()
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()