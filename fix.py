# create_supplier_fixed.py
from app import create_app
from models.user import User
from database import db
import random

app = create_app('development')

with app.app_context():
    print("="*60)
    print("🔧 CREATING SUPPLIER ACCOUNT")
    print("="*60)
    
    # Check if supplier exists
    supplier = User.query.filter_by(email='supplier@medapp.com').first()
    
    if not supplier:
        print("\n➕ Creating supplier account...")
        
        supplier = User(
            user_id=f"SUP{random.randint(100, 999)}",
            name="MedApp Supplier",
            email="supplier@medapp.com",
            role="supplier",  # string, not enum
            is_active=True
        )
        supplier.set_password("Supplier@123")
        
        db.session.add(supplier)
        db.session.commit()
        
        print("✅ Supplier created successfully!")
        print("\n🔑 SUPPLIER LOGIN CREDENTIALS:")
        print("   Email: supplier@medapp.com")
        print("   Password: Supplier@123")
        print("   Role: supplier")
    else:
        print(f"\n✅ Supplier already exists!")
        print(f"   Email: {supplier.email}")
        print(f"   Name: {supplier.name}")
        print(f"   Role: {supplier.role}")
        print(f"   User ID: {supplier.user_id}")
        print("\n🔑 Login with:")
        print("   Email: supplier@medapp.com")
        print("   Password: Supplier@123")