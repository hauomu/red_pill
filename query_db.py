import sqlite3

conn = sqlite3.connect('delivery.db')
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in delivery.db:")
for table in tables:
    print(f"  - {table[0]}")
    
# Get schema and data for each table
for table in tables:
    print(f"\n{'='*60}")
    print(f"Table: {table[0]}")
    print(f"{'='*60}")
    
    cursor.execute(f"PRAGMA table_info({table[0]})")
    columns = cursor.fetchall()
    print("Columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    cursor.execute(f"SELECT * FROM {table[0]};")
    rows = cursor.fetchall()
    print(f"\nData ({len(rows)} rows):")
    if rows:
        for row in rows:
            print(f"  {row}")
    else:
        print("  (empty)")

conn.close()
