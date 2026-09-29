# create_users_simple.py
import os
import sqlite3

# Direct database connection
db_path = r"C:\medapp\medapp1\food\instance\medapp.db"

# Ensure directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Delete old database if exists
if os.path.exists(db_path):
    os.remove(db_path)
    print("✅ Old database deleted")

# Create new database and tables
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(200),
    role VARCHAR(20) DEFAULT 'user',
    is_active BOOLEAN DEFAULT 1,
    last_login DATETIME,
    created_at DATETIME,
    updated_at DATETIME
)
''')

from werkzeug.security import generate_password_hash
from datetime import datetime

# Insert users
users = [
    ('SA001', 'Aditya Prasad', 'superadmin@medapp.com', 'superadmin', 'Medapp@2026SuperAdmin'),
    ('U001', 'Vishal Kumar', 'admin@medapp.com', 'admin', 'Medapp@2026Admin'),
    ('U002', 'Test User', 'user@medapp.com', 'user', 'Medapp@2026User')
]

now = datetime.now().isoformat()

for uid, name, email, role, password in users:
    password_hash = generate_password_hash(password)
    cursor.execute('''
        INSERT INTO users (user_id, name, email, role, password_hash, is_active, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 1, ?, ?)
    ''', (uid, name, email, role, password_hash, now, now))

conn.commit()
conn.close()

print("✅ Database created successfully!")
print("📁 Location:", db_path)
print("\n🔑 Login Credentials:")
print("   Super Admin: superadmin@medapp.com / Medapp@2026SuperAdmin")
print("   Admin: admin@medapp.com / Medapp@2026Admin")
print("   User: user@medapp.com / Medapp@2026User")