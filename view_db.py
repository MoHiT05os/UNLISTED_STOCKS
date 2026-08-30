import sqlite3
import os

db_path = os.path.join('backend', 'stocks.db')

if not os.path.exists(db_path):
    print(f"Error: Database file not found at {db_path}")
    exit()

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query all tables first to show the user
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("=== DATABASE TABLES ===")
    for table in tables:
        print(f"- {table[0]}")
    print("\n" + "="*50 + "\n")
    
    # Query users
    cursor.execute("SELECT id, full_name, phone, pan_number, is_verified, created_at FROM users;")
    users = cursor.fetchall()
    
    print(f"=== REGISTERED USERS ({len(users)} entries) ===")
    print(f"{'ID':<4} | {'Full Name':<20} | {'Phone':<12} | {'PAN Number':<12} | {'Verified':<8} | {'Created At'}")
    print("-" * 80)
    for u in users:
        verified_str = "Yes" if u[4] else "No"
        print(f"{u[0]:<4} | {u[1]:<20} | {u[2]:<12} | {u[3]:<12} | {verified_str:<8} | {u[5]}")
        
except sqlite3.OperationalError as e:
    print(f"Operational Error: {e}. Has the table been created yet?")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
