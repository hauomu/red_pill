import sqlite3

print("=== FIXING BRANCH DATA IN DATABASE ===\n")

conn = sqlite3.connect('delivery.db')
c = conn.cursor()

# Mapping to standardize branches
fixes = {
    'Central': 'CENTRAL',
    'Cnetral': 'CENTRAL',
    'EAST': 'EAST',
    'East': 'EAST',
    'North': 'NORTH',
    'Noth': 'NORTH',
    'West': 'WEST',
    'west': 'WEST'
}

print("Before fixes:")
c.execute('SELECT branch, COUNT(*) FROM deliveries GROUP BY branch ORDER BY branch')
for row in c.fetchall():
    print(f"  {row[0]:10s}: {row[1]:,} rows")

# Fix each variant
for old_name, new_name in fixes.items():
    c.execute('UPDATE deliveries SET branch = ? WHERE branch = ?', (new_name, old_name))
    count = c.rowcount
    if count > 0:
        print(f"\n✓ Fixed: {old_name:10s} → {new_name:10s} ({count:,} rows)")

conn.commit()

print("\n\nAfter fixes:")
c.execute('SELECT branch, COUNT(*) FROM deliveries GROUP BY branch ORDER BY branch')
for row in c.fetchall():
    print(f"  {row[0]:10s}: {row[1]:,} rows")

conn.close()
print("\n✅ Database fixed!")
