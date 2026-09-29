# test_oracledb.py
import oracledb

print("="*60)
print("🔍 ORACLEDB CONNECTION TEST")
print("="*60)

# ==================== METHOD 1: DIRECT IP (BEST) ====================
print("\n📌 METHOD 1: Using IP address directly")
print("-" * 40)

try:
    connection = oracledb.connect(
        user='system',
        password='oracle',
        host='127.0.0.1',  # Direct IP, not hostname
        port=1521,
        service_name='XEPDB1'
    )
    print("✅ SUCCESS with 127.0.0.1!")
    connection.close()
except Exception as e:
    print(f"❌ Failed: {e}")

