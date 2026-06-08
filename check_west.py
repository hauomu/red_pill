import sqlite3
conn = sqlite3.connect('delivery.db')
c = conn.cursor()
c.execute("SELECT DISTINCT branch FROM deliveries WHERE UPPER(branch) = 'WEST' ORDER BY branch")
print("WEST variants:")
for row in c.fetchall():
    print(f"  '{row[0]}' (len={len(row[0])})")
conn.close()
