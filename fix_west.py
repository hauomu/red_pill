import sqlite3

conn = sqlite3.connect('delivery.db')
c = conn.cursor()

c.execute('UPDATE deliveries SET branch = ? WHERE branch = ?', ('WEST', 'west'))
conn.commit()
print(f"✓ Fixed: west → WEST ({c.rowcount} rows)")

c.execute('SELECT branch, COUNT(*) FROM deliveries GROUP BY branch ORDER BY branch')
print("\nBranches after fix:")
for row in c.fetchall():
    print(f"  {row[0]:10s}: {row[1]:,} rows")

conn.close()
