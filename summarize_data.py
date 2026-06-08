import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('delivery.db')

print("="*80)
print("DELIVERY DATABASE SUMMARY")
print("="*80)

# DELIVERY RECORDS SUMMARY
print("\n[1] DELIVERY RECORDS")
print("-"*80)

# Basic stats
query = "SELECT COUNT(*) as total_records FROM deliveries"
df = pd.read_sql_query(query, conn)
print(f"Total deliveries: {df['total_records'][0]:,}")

# Date range
query = "SELECT MIN(booking_datetime) as earliest, MAX(booking_datetime) as latest FROM deliveries"
df = pd.read_sql_query(query, conn)
print(f"Date range: {df['earliest'][0]} to {df['latest'][0]}")

# Branches
query = "SELECT branch, COUNT(*) as count FROM deliveries GROUP BY branch ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
print(f"\nDeliveries by branch:")
for idx, row in df.iterrows():
    pct = (row['count'] / df['count'].sum()) * 100
    print(f"  {row['branch']:12} {row['count']:>8,} ({pct:5.1f}%)")

# Vehicle types
query = "SELECT vehicle_type, COUNT(*) as count FROM deliveries GROUP BY vehicle_type ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
print(f"\nDeliveries by vehicle type:")
for idx, row in df.iterrows():
    pct = (row['count'] / df['count'].sum()) * 100
    print(f"  {row['vehicle_type']:12} {row['count']:>8,} ({pct:5.1f}%)")

# Priority
query = "SELECT delivery_priority, COUNT(*) as count FROM deliveries GROUP BY delivery_priority ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
print(f"\nDeliveries by priority:")
for idx, row in df.iterrows():
    pct = (row['count'] / df['count'].sum()) * 100
    print(f"  {row['delivery_priority']:12} {row['count']:>8,} ({pct:5.1f}%)")

# Parcel category
query = "SELECT parcel_category, COUNT(*) as count FROM deliveries GROUP BY parcel_category ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
print(f"\nDeliveries by parcel category:")
for idx, row in df.iterrows():
    pct = (row['count'] / df['count'].sum()) * 100
    print(f"  {row['parcel_category']:12} {row['count']:>8,} ({pct:5.1f}%)")

# Payment method
query = "SELECT payment_method, COUNT(*) as count FROM deliveries GROUP BY payment_method"
df = pd.read_sql_query(query, conn)
print(f"\nPayment method:")
for idx, row in df.iterrows():
    pct = (row['count'] / df['count'].sum()) * 100
    print(f"  {row['payment_method']:12} {row['count']:>8,} ({pct:5.1f}%)")

# Numeric column statistics
print(f"\nNumeric columns statistics:")
numeric_cols = ['distance_km', 'parcel_weight_kg', 'parcel_value_sgd', 'num_stops_on_route', 'driver_experience_months']
for col in numeric_cols:
    query = f"SELECT COUNT(*) as count, MIN(CAST({col} as REAL)) as min_val, MAX(CAST({col} as REAL)) as max_val, AVG(CAST({col} as REAL)) as avg_val FROM deliveries WHERE {col} IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    min_v = float(df['min_val'][0]) if df['min_val'][0] is not None else 0
    max_v = float(df['max_val'][0]) if df['max_val'][0] is not None else 0
    avg_v = float(df['avg_val'][0]) if df['avg_val'][0] is not None else 0
    print(f"  {col:30} min={min_v:>8.1f}  max={max_v:>8.1f}  avg={avg_v:>8.2f}")

# On-time delivery rate
print(f"\nOn-time delivery analysis:")
query = """
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN delivery_datetime <= promised_delivery_datetime THEN 1 ELSE 0 END) as on_time,
    SUM(CASE WHEN delivery_datetime > promised_delivery_datetime THEN 1 ELSE 0 END) as late,
    AVG(CAST((julianday(delivery_datetime) - julianday(promised_delivery_datetime)) * 24 AS FLOAT)) as avg_hours_delay
FROM deliveries
"""
df = pd.read_sql_query(query, conn)
on_time_pct = (df['on_time'][0] / df['total'][0]) * 100
late_pct = (df['late'][0] / df['total'][0]) * 100
print(f"  On-time deliveries: {df['on_time'][0]:>8,} ({on_time_pct:5.1f}%)")
print(f"  Late deliveries:    {df['late'][0]:>8,} ({late_pct:5.1f}%)")
print(f"  Avg delay:          {df['avg_hours_delay'][0]:>8.2f} hours")

# CUSTOMER FEEDBACK SUMMARY
print("\n" + "="*80)
print("[2] CUSTOMER FEEDBACK")
print("-"*80)

# Basic stats
query = "SELECT COUNT(*) as total_records FROM feedback"
df = pd.read_sql_query(query, conn)
total_feedback = df['total_records'][0]
print(f"Total feedback records: {total_feedback:,}")

# Feedback rate
query = "SELECT COUNT(DISTINCT delivery_id) as total_deliveries FROM deliveries"
df = pd.read_sql_query(query, conn)
total_deliveries = df['total_deliveries'][0]
feedback_rate = (total_feedback / total_deliveries) * 100
print(f"Deliveries with feedback: {feedback_rate:.1f}%")

# Date range
query = "SELECT MIN(feedback_datetime) as earliest, MAX(feedback_datetime) as latest FROM feedback"
df = pd.read_sql_query(query, conn)
print(f"Feedback date range: {df['earliest'][0]} to {df['latest'][0]}")

# Rating distribution
print(f"\nRating distribution:")
query = "SELECT rating, COUNT(*) as count FROM feedback WHERE rating IS NOT NULL GROUP BY rating ORDER BY rating"
df = pd.read_sql_query(query, conn)
for idx, row in df.iterrows():
    rating = int(row['rating'])
    pct = (row['count'] / total_feedback) * 100
    stars = "★" * rating + "☆" * (5 - rating)
    print(f"  {rating} stars {stars} {row['count']:>8,} ({pct:5.1f}%)")

# Average rating
query = "SELECT AVG(rating) as avg_rating FROM feedback"
df = pd.read_sql_query(query, conn)
avg_rating = df['avg_rating'][0]
print(f"\nAverage rating: {avg_rating:.2f}/5.0")

# Comments analysis
print(f"\nComment statistics:")
query = "SELECT COUNT(*) as total, SUM(CASE WHEN comment IS NOT NULL AND comment != '' THEN 1 ELSE 0 END) as with_comment FROM feedback"
df = pd.read_sql_query(query, conn)
comment_pct = (df['with_comment'][0] / df['total'][0]) * 100 if df['total'][0] > 0 else 0
print(f"  Feedback with comments: {df['with_comment'][0]:>8,} ({comment_pct:5.1f}%)")
print(f"  Feedback without comments: {df['total'][0] - df['with_comment'][0]:>8,}")

# Low ratings (1-2 stars)
print(f"\nLow satisfaction (1-2 stars):")
query = "SELECT COUNT(*) as low_ratings FROM feedback WHERE rating <= 2"
df = pd.read_sql_query(query, conn)
low_pct = (df['low_ratings'][0] / total_feedback) * 100
print(f"  Count: {df['low_ratings'][0]:>8,} ({low_pct:5.1f}%)")

# CORRELATION ANALYSIS
print("\n" + "="*80)
print("[3] DELIVERY-FEEDBACK RELATIONSHIP")
print("-"*80)

query = """
SELECT 
    d.delivery_id,
    f.rating,
    CAST((julianday(d.delivery_datetime) - julianday(d.promised_delivery_datetime)) * 24 AS FLOAT) as hours_delay
FROM deliveries d
LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
WHERE f.rating IS NOT NULL
LIMIT 5
"""
df = pd.read_sql_query(query, conn)
print(f"Sample of delivery-feedback linkage (first 5):")
print(df.head().to_string(index=False))

# Late deliveries vs ratings
query = """
SELECT 
    CASE WHEN delivery_datetime > promised_delivery_datetime THEN 'Late' ELSE 'On-time' END as delivery_status,
    COUNT(f.feedback_id) as feedback_count,
    AVG(f.rating) as avg_rating
FROM deliveries d
LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
WHERE f.rating IS NOT NULL
GROUP BY CASE WHEN delivery_datetime > promised_delivery_datetime THEN 'Late' ELSE 'On-time' END
"""
df = pd.read_sql_query(query, conn)
print(f"\nRating by delivery status:")
for idx, row in df.iterrows():
    print(f"  {row['delivery_status']:10} {row['feedback_count']:>8,} feedbacks  avg_rating={row['avg_rating']:.2f}")

conn.close()
print("\n" + "="*80)
