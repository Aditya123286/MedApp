# find_credentials.py
import re

print("🔍 Checking app.py for credentials...")

try:
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    print("✅ Successfully read app.py\n")
except Exception as e:
    print(f"❌ Error reading app.py: {e}")
    exit(1)

# Look for SQLALCHEMY_DATABASE_URI
print("=" * 60)
print("🔍 SEARCHING FOR DATABASE CREDENTIALS")
print("=" * 60)

# Pattern 1: Full URI
pattern1 = r'SQLALCHEMY_DATABASE_URI\s*=\s*[\'"]([^\'"]+)[\'"]'
matches1 = re.findall(pattern1, content)

if matches1:
    print(f"\n✅ FOUND DATABASE URI:")
    print(f"   {matches1[0]}")
    
    uri = matches1[0]
    
    # Parse Oracle connection string
    if 'oracle' in uri.lower():
        print("\n🔓 PARSING ORACLE CONNECTION:")
        
        # Extract components
        # Format: oracle+oracledb://user:password@host:port/?service_name=xxx
        user_match = re.search(r'oracle\+oracledb://([^:]+):([^@]+)@([^:]+):(\d+)/\?', uri)
        if user_match:
            user = user_match.group(1)
            password = user_match.group(2)
            host = user_match.group(3)
            port = user_match.group(4)
            
            # Extract service_name
            service_match = re.search(r'service_name=([^&\'"]+)', uri)
            service_name = service_match.group(1) if service_match else 'XE'
            
            print(f"\n   📋 CONNECTION DETAILS:")
            print(f"   {'='*40}")
            print(f"   User:     {user}")
            print(f"   Password: {password}")
            print(f"   Host:     {host}")
            print(f"   Port:     {port}")
            print(f"   Service:  {service_name}")
            print(f"   {'='*40}")
            
            print(f"\n   💡 USE THESE CREDENTIALS:")
            print(f"   python create_triggers.py")
else:
    print("❌ Database URI not found in app.py")
    print("\nSearching for any database-related config...")
    
    # Try to find any database config
    db_patterns = [
        r"database.*?=.*?'([^']+)'",
        r"URI.*?=.*?'([^']+)'",
        r"oracle.*?=.*?'([^']+)'",
    ]
    
    for pattern in db_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            print(f"\n⚠️  Found potential config: {matches[0]}")