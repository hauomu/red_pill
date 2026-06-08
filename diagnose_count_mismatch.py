"""
Diagnose the source of monthly feedback count mismatch
"""
import sqlite3
import pandas as pd

print("\n" + "=" * 100)
print("DIAGNOSIS: Monthly Feedback Count Mismatch")
print("=" * 100)

conn = sqlite3.connect('delivery.db')
cursor = conn.cursor()

# Get all feedback with their branch info
query1 = """
SELECT 
    COUNT(*) as total,
    COUNT(CASE WHEN d.delivery_id IS NOT NULL THEN 1 END) as with_delivery,
    COUNT(CASE WHEN d.delivery_id IS NULL THEN 1 END) as without_delivery
FROM feedback f
LEFT JOIN deliveries d ON f.delivery_id = d.delivery_id
"""

result = pd.read_sql(query1, conn)
print(f"\n1. Feedback join status:")
print(result.to_string(index=False))

# Check for null branch values
query2 = """
SELECT 
    strftime('%Y-%m', f.feedback_datetime) as month,
    COUNT(CASE WHEN d.branch IS NULL THEN 1 END) as null_branch,
    COUNT(CASE WHEN d.branch IS NOT NULL THEN 1 END) as non_null_branch,
    COUNT(*) as total
FROM feedback f
LEFT JOIN deliveries d ON f.delivery_id = d.delivery_id
GROUP BY month
ORDER BY month
"""

null_branches = pd.read_sql(query2, conn)
print(f"\n2. Feedback with null branch values by month:")
print(null_branches.to_string(index=False))

# Check what the files are actually counting
query3 = """
SELECT 
    strftime('%Y-%m', f.feedback_datetime) as month,
    CASE 
        WHEN UPPER(TRIM(d.branch)) IN ('CENTRAL', 'CNETRAL') THEN 'CENTRAL'
        WHEN UPPER(TRIM(d.branch)) IN ('EAST') THEN 'EAST'
        WHEN UPPER(TRIM(d.branch)) IN ('NORTH', 'NOTH') THEN 'NORTH'
        WHEN UPPER(TRIM(d.branch)) IN ('WEST', 'WEST ') THEN 'WEST'
        ELSE 'OTHER'
    END as depot_group,
    COUNT(*) as count
FROM feedback f
JOIN deliveries d ON f.delivery_id = d.delivery_id
GROUP BY month, depot_group
ORDER BY month, depot_group
"""

grouped = pd.read_sql(query3, conn)
print(f"\n3. Feedback by month and depot classification:")
print(grouped.to_string(index=False))

# Get the 'OTHER' category (unrecognized depots)
query4 = """
SELECT 
    strftime('%Y-%m', f.feedback_datetime) as month,
    DISTINCT d.branch as branch_name,
    COUNT(*) as count
FROM feedback f
JOIN deliveries d ON f.delivery_id = d.delivery_id
WHERE NOT UPPER(TRIM(d.branch)) IN ('CENTRAL', 'CNETRAL', 'EAST', 'NORTH', 'NOTH', 'WEST', 'WEST ')
GROUP BY month, d.branch
ORDER BY month, d.branch
"""

try:
    other_depots = pd.read_sql(query4, conn)
    print(f"\n4. Feedback with unrecognized depot names:")
    print(other_depots.to_string(index=False))
except Exception as e:
    print(f"   Error: {e}")
    # Try without DISTINCT
    query4_alt = """
    SELECT 
        strftime('%Y-%m', f.feedback_datetime) as month,
        d.branch as branch_name,
        COUNT(*) as count
    FROM feedback f
    JOIN deliveries d ON f.delivery_id = d.delivery_id
    WHERE NOT UPPER(TRIM(d.branch)) IN ('CENTRAL', 'CNETRAL', 'EAST', 'NORTH', 'NOTH', 'WEST', 'WEST ')
    GROUP BY month, d.branch
    ORDER BY month, d.branch
    """
    other_depots = pd.read_sql(query4_alt, conn)
    print(f"\n4. Feedback with unrecognized depot names:")
    print(other_depots.to_string(index=False))

# Compare file vs database totals by month with depot classification
print(f"\n" + "=" * 100)
print("COMPARISON: Total feedback by month")
print("=" * 100)

file_monthly = pd.read_excel('data_exports/Monthly_Feedback_Summary_Detailed.xlsx', sheet_name='Monthly Feedback Summary')

# Get DB total for only recognized depots
query5 = """
SELECT 
    strftime('%Y-%m', f.feedback_datetime) as month,
    COUNT(*) as db_count
FROM feedback f
JOIN deliveries d ON f.delivery_id = d.delivery_id
WHERE UPPER(TRIM(d.branch)) IN ('CENTRAL', 'CNETRAL', 'EAST', 'NORTH', 'NOTH', 'WEST', 'WEST ')
GROUP BY month
ORDER BY month
"""

db_recognized = pd.read_sql(query5, conn)

print(f"\n{'Month':<12} {'File':<12} {'DB-Recognized':<15} {'Difference':<15}")
print("-" * 54)

for idx, row in db_recognized.iterrows():
    month = row['month']
    db_count = row['db_count']
    
    file_data = file_monthly[file_monthly['Month'] == month]
    if len(file_data) > 0:
        file_count = file_data['Total Feedback'].values[0]
        diff = file_count - db_count
        print(f"{month:<12} {file_count:<12} {db_count:<15} {diff:+<15}")

conn.close()

print(f"\n" + "=" * 100)
print("HYPOTHESIS:")
print("=" * 100)
print("""
The files appear to be counting a different set of feedback records than the database.
This could be due to:
1. Different join logic (LEFT JOIN vs INNER JOIN)
2. Different filtering conditions (date range, rating presence, etc.)
3. Different branch mapping logic

All monthly counts in the file are LOWER than the database counts, which suggests:
- Files may only include feedback with non-null ratings
- Files may have a different date range
- Files may only count specific branch values

ACTION: Check the scripts that generated these files to understand the logic.
""")
