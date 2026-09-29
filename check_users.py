# check_and_fix_roles.py
from app import app
from models.user import User
from models.role import Role
from database import db

with app.app_context():
    print("=" * 60)
    print("CHECKING DATABASE ROLES")
    print("=" * 60)
    
    # Get all roles
    roles = Role.query.all()
    print("\nAvailable Roles:")
    for role in roles:
        print(f"   ID: {role.id}, Name: {role.name}")
    
    print("\n" + "=" * 60)
    print("CURRENT USER ROLES IN DATABASE:")
    print("=" * 60)
    
    users_to_fix = []
    
    for user in User.query.all():
        role_name = user.role.name if user.role else 'No Role'
        print(f"   {user.email} -> {role_name} (role_id: {user.role_id})")
        
        # Check if role is correct
        if user.email == 'superadmin@medapp.com' and role_name != 'super_admin':
            users_to_fix.append((user, 'super_admin', 'superadmin@medapp.com'))
        elif user.email == 'admin@medapp.com' and role_name != 'admin':
            users_to_fix.append((user, 'admin', 'admin@medapp.com'))
        elif user.email == 'user@medapp.com' and role_name != 'user':
            users_to_fix.append((user, 'user', 'user@medapp.com'))
    
    # Fix incorrect roles
    if users_to_fix:
        print("\n" + "=" * 60)
        print("FIXING INCORRECT ROLES:")
        print("=" * 60)
        
        for user, correct_role, email in users_to_fix:
            role_obj = Role.query.filter_by(name=correct_role).first()
            if role_obj:
                user.role_id = role_obj.id
                print(f"   ✅ Fixed {email} -> {correct_role}")
            else:
                print(f"   ❌ Role '{correct_role}' not found!")
        
        db.session.commit()
        print("\n✅ Database roles fixed!")
    else:
        print("\n✅ All roles are correct in database!")
    
    # Show final roles
    print("\n" + "=" * 60)
    print("FINAL DATABASE ROLES:")
    print("=" * 60)
    for user in User.query.all():
        role_name = user.role.name if user.role else 'No Role'
        icon = "👑" if role_name == 'super_admin' else ("⚙️" if role_name == 'admin' else "👤")
        print(f"   {icon} {user.email} -> {role_name}")