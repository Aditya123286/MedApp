# setup_db.py
import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

# Database path
db_path = r"C:\medapp\medapp1\food\instance\medapp.db"

# Ensure directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Delete old database if exists
if os.path.exists(db_path):
    os.remove(db_path)
    print("✅ Old database deleted")

# Create fresh database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("✅ New database created")

# Create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(200) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT 1,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ Users table created")

# Create orders table (if needed)
cursor.execute('''
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id VARCHAR(50),
    customer_name VARCHAR(100) NOT NULL,
    customer_email VARCHAR(100),
    customer_phone VARCHAR(20),
    delivery_address TEXT,
    total_amount FLOAT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    payment_method VARCHAR(50),
    notes TEXT,
    delivered_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
''')
print("✅ Orders table created")

# Current timestamp
now = datetime.now().isoformat()

# Insert users
users = [
    {
        'user_id': 'SA001',
        'name': 'Aditya Prasad',
        'email': 'superadmin@medapp.com',
        'password': 'Medapp@2026SuperAdmin',
        'role': 'superadmin'
    },
    {
        'user_id': 'U001',
        'name': 'Vishal Kumar',
        'email': 'admin@medapp.com',
        'password': 'Medapp@2026Admin',
        'role': 'admin'
    },
    {
        'user_id': 'U002',
        'name': 'Test User',
        'email': 'user@medapp.com',
        'password': 'Medapp@2026User',
        'role': 'user'
    }
]

for user in users:
    password_hash = generate_password_hash(user['password'])
    cursor.execute('''
        INSERT INTO users (user_id, name, email, password_hash, role, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 1, ?, ?)
    ''', (user['user_id'], user['name'], user['email'], password_hash, user['role'], now, now))
    print(f"   ✅ {user['email']} ({user['role']})")

# Insert sample order
cursor.execute('''
    INSERT INTO orders (order_number, user_id, customer_name, customer_email, customer_phone, 
                       delivery_address, total_amount, status, payment_status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'ORD-20260301-001', 'U002', 'Test User', 'user@medapp.com', '9876543210',
    'Test Address, Mumbai', 500.00, 'pending', 'pending', now, now
))
print("✅ Sample order created")

# Commit and close
conn.commit()
print("\n📊 Verifying database...")

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"   - {table[0]}")

# Check users
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]
print(f"\n👥 Users in database: {user_count}")

cursor.execute("SELECT id, user_id, name, email, role FROM users")
for row in cursor.fetchall():
    print(f"   - {row[3]} ({row[4]})")

conn.close()

print("\n" + "="*50)
print("✅ DATABASE SETUP COMPLETE!")
print("="*50)
print("\n🔑 Login Credentials:")
print("   Super Admin: superadmin@medapp.com / Medapp@2026SuperAdmin")
print("   Admin: admin@medapp.com / Medapp@2026Admin")
print("   User: user@medapp.com / Medapp@2026User")
print("\n📁 Database location:", db_path)
