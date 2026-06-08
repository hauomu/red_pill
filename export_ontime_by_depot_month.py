import pandas as pd
import sqlite3

print("📊 Creating On-Time % by Month & Depot (CSV)...")

# Load from database
conn = sqlite3.connect('delivery.db')

# Query: On-time delivery by month and depot
query = """
SELECT 
    strftime('%Y-%m', d.booking_datetime) as Month,
    CASE 
        WHEN UPPER(TRIM(d.branch)) IN ('CENTRAL', 'CNETRAL') THEN 'Central'
        WHEN UPPER(TRIM(d.branch)) = 'EAST' THEN 'East'
        WHEN UPPER(TRIM(d.branch)) IN ('NORTH', 'NOTH') THEN 'North'
        WHEN UPPER(TRIM(d.branch)) = 'WEST' THEN 'West'
        ELSE d.branch
    END as Depot,
    COUNT(d.delivery_id) as Total_Deliveries,
    SUM(CASE WHEN d.delivery_datetime <= d.promised_delivery_datetime THEN 1 ELSE 0 END) as OnTime_Count,
    ROUND(AVG(CASE WHEN d.delivery_datetime <= d.promised_delivery_datetime THEN 1 ELSE 0 END) * 100, 2) as OnTime_Percentage
FROM deliveries d
GROUP BY Month, Depot
ORDER BY Month, Depot
"""

result_df = pd.read_sql_query(query, conn)
conn.close()

print("\n" + "="*120)
print("📊 ON-TIME DELIVERY % BY MONTH & DEPOT")
print("="*120 + "\n")
print(result_df.to_string(index=False))

# Save as CSV
csv_path = 'data_exports/Monthly_OnTime_Percentage_By_Depot.csv'
result_df.to_csv(csv_path, index=False)
print(f"\n✅ Saved CSV: {csv_path}")

# Create pivot view (Months as rows, Depots as columns)
pivot_df = result_df.pivot_table(
    index='Month',
    columns='Depot',
    values='OnTime_Percentage',
    aggfunc='first'
).reset_index()

print("\n" + "="*100)
print("📊 PIVOT VIEW: ON-TIME % BY MONTH (Rows) & DEPOT (Columns)")
print("="*100 + "\n")
print(pivot_df.to_string(index=False))

# Save pivot as CSV
pivot_csv_path = 'data_exports/Monthly_OnTime_Percentage_Pivot.csv'
pivot_df.to_csv(pivot_csv_path, index=False)
print(f"\n✅ Saved Pivot CSV: {pivot_csv_path}")

# Summary stats
print("\n" + "="*100)
print("🎯 SUMMARY STATISTICS")
print("="*100)

print("\nDepot Overall On-Time %:")
depot_avg = result_df.groupby('Depot')['OnTime_Percentage'].agg(['mean', 'min', 'max']).round(2)
for depot in ['Central', 'North', 'West', 'East']:
    if depot in depot_avg.index:
        row = depot_avg.loc[depot]
        print(f"  {depot:8s}: Avg {row['mean']:.2f}% | Min {row['min']:.2f}% | Max {row['max']:.2f}%")

print("\nMonthly Overall On-Time %:")
monthly_avg = result_df.groupby('Month')['OnTime_Percentage'].mean().round(2)
for month, pct in monthly_avg.items():
    print(f"  {month}: {pct:.2f}%")

print("\nBest Month-Depot Combination:")
best_idx = result_df['OnTime_Percentage'].idxmax()
best_row = result_df.iloc[best_idx]
print(f"  {best_row['Depot']} in {best_row['Month']}: {best_row['OnTime_Percentage']:.2f}% ({int(best_row['OnTime_Count'])}/{int(best_row['Total_Deliveries'])})")

print("\nWorst Month-Depot Combination:")
worst_idx = result_df['OnTime_Percentage'].idxmin()
worst_row = result_df.iloc[worst_idx]
print(f"  {worst_row['Depot']} in {worst_row['Month']}: {worst_row['OnTime_Percentage']:.2f}% ({int(worst_row['OnTime_Count'])}/{int(worst_row['Total_Deliveries'])})")

print("\n" + "="*100)
