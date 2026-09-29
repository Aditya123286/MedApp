# force_users.py - FIXED VERSION
from app import create_app
from database import db
from models.user import User
from datetime import datetime

def force_create_user():
    """Create user WITH proper app context"""
    app = create_app()
    
    # ✅ IMPORTANT: App context ke ANDAR saara kaam karo
    with app.app_context():
        try:
            print("🔍 Checking for existing users...")
            
            # Check if admin exists
            admin = User.query.filter_by(email='admin@medapp.com').first()
            if admin:
                print(f"🗑️ Deleting existing admin: {admin.email}")
                db.session.delete(admin)
                db.session.commit()
                print("✅ Deleted existing admin")
            
            # Check if user exists
            user = User.query.filter_by(email='user@medapp.com').first()
            if user:
                print(f"🗑️ Deleting existing user: {user.email}")
                db.session.delete(user)
                db.session.commit()
                print("✅ Deleted existing user")
            
            # Check if super admin exists
            super_admin = User.query.filter_by(email='superadmin@medapp.com').first()
            if super_admin:
                print(f"🗑️ Deleting existing super admin: {super_admin.email}")
                db.session.delete(super_admin)
                db.session.commit()
                print("✅ Deleted existing super admin")
            
            print("\n🔄 Creating new users...")
            
            # Create admin
            new_admin = User(
                user_id=f"U{datetime.now().strftime('%y%m%d%H%M%S')}",
                name="Aditya Sharma",
                email="admin@medapp.com",
                phone="9876543210",
                role="admin",
                is_active=True
            )
            new_admin.set_password("123456")
            db.session.add(new_admin)
            print(f"   ➕ Added: {new_admin.email}")
            
            # Create regular user
            new_user = User(
                user_id=f"U{datetime.now().strftime('%y%m%d%H%M%S')}",
                name="Test User",
                email="user@medapp.com",
                phone="9876543211",
                role="user",
                is_active=True
            )
            new_user.set_password("123456")
            db.session.add(new_user)
            print(f"   ➕ Added: {new_user.email}")
            
            # Create super admin
            new_super = User(
                user_id=f"SA{datetime.now().strftime('%y%m%d%H%M%S')}",
                name="Super Admin",
                email="superadmin@medapp.com",
                phone="9999999999",
                role="super_admin",
                is_active=True
            )
            new_super.set_password("SuperAdmin@123")
            db.session.add(new_super)
            print(f"   ➕ Added: {new_super.email}")
            
            # Commit all changes
            db.session.commit()
            print("\n✅ All users created successfully!")
            
            # Verify users
            print("\n📋 Verifying users:")
            for u in User.query.all():
                print(f"   • {u.email} ({u.role})")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            db.session.rollback()

if __name__ == "__main__":
    force_create_user()