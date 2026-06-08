import pandas as pd
import numpy as np
from datetime import datetime

print("=" * 120)
print("EDA VALIDATION AUDIT - AIAP24 Assessment")
print("=" * 120)

# ============================================================================
# TASK 1: LOAD SOURCE DATA
# ============================================================================
print("\n📂 LOADING SOURCE DATA (Ground Truth)")
print("-" * 120)

deliveries_src = pd.read_csv('Db-Browser/deliveries.csv', encoding='latin-1')
feedback_src = pd.read_csv('Db-Browser/feedback.csv', encoding='latin-1')

print(f"✅ Deliveries source: {len(deliveries_src):,} rows × {len(deliveries_src.columns)} columns")
print(f"✅ Feedback source: {len(feedback_src):,} rows × {len(feedback_src.columns)} columns")

# ============================================================================
# TASK 2: VALIDATE ROW COUNTS
# ============================================================================
print("\n" + "=" * 120)
print("1. ROW COUNT VALIDATION")
print("=" * 120)

print(f"\nSource Data:")
print(f"  Deliveries: {len(deliveries_src):,} rows")
print(f"  Feedback:   {len(feedback_src):,} rows")

# Load exported files for comparison
merged_csv = pd.read_csv('data_exports/deliveries_feedback_merged.csv', encoding='latin-1')
monthly_enhanced = pd.read_excel('data_exports/Monthly_Feedback_Enhanced.xlsx', sheet_name='Depot Monthly Breakdown')
monthly_summary = pd.read_excel('data_exports/Monthly_Feedback_Summary_Detailed.xlsx', sheet_name='Monthly Feedback Summary')

print(f"\nExported Files:")
print(f"  Merged CSV:           {len(merged_csv):,} rows (should be ~{len(deliveries_src):,})")
print(f"  Monthly Enhanced:     {len(monthly_enhanced):,} rows")
print(f"  Monthly Summary:      {len(monthly_summary):,} rows")

# Check merge quality
match_merged = "✅ MATCH" if len(merged_csv) == len(deliveries_src) else "⚠️ MISMATCH"
print(f"\n{match_merged} - Merged CSV preserves all delivery records")

# ============================================================================
# TASK 3: MISSING VALUES ANALYSIS
# ============================================================================
print("\n" + "=" * 120)
print("2. MISSING VALUES VALIDATION")
print("=" * 120)

print("\nDeliveries Missing Values:")
del_missing = deliveries_src.isnull().sum()
for col in del_missing[del_missing > 0].index:
    pct = (del_missing[col] / len(deliveries_src) * 100)
    print(f"  {col:35s}: {del_missing[col]:>8,} ({pct:>5.1f}%)")

if del_missing.sum() == 0:
    print("  No missing values")

print("\nFeedback Missing Values:")
fb_missing = feedback_src.isnull().sum()
for col in fb_missing[fb_missing > 0].index:
    pct = (fb_missing[col] / len(feedback_src) * 100)
    print(f"  {col:35s}: {fb_missing[col]:>8,} ({pct:>5.1f}%)")

if fb_missing.sum() == 0:
    print("  No missing values")

# ============================================================================
# TASK 4: DUPLICATE RECORDS
# ============================================================================
print("\n" + "=" * 120)
print("3. DUPLICATE RECORDS VALIDATION")
print("=" * 120)

del_dupes = deliveries_src.duplicated().sum()
fb_dupes = feedback_src.duplicated().sum()

print(f"\nDeliveries Duplicates:  {del_dupes} records")
print(f"Feedback Duplicates:    {fb_dupes} records")

# Check primary keys
del_id_dupes = deliveries_src['delivery_id'].duplicated().sum()
fb_id_dupes = feedback_src['feedback_id'].duplicated().sum()

print(f"\nPrimary Key Duplicates:")
print(f"  delivery_id:  {del_id_dupes} duplicates" + ("" if del_id_dupes == 0 else " ⚠️"))
print(f"  feedback_id:  {fb_id_dupes} duplicates" + ("" if fb_id_dupes == 0 else " ⚠️"))

# ============================================================================
# TASK 5: UNIQUE VALUE COUNTS
# ============================================================================
print("\n" + "=" * 120)
print("4. UNIQUE VALUES & CATEGORY DISTRIBUTIONS")
print("=" * 120)

print("\nDeliveries - Key Dimensions:")
print(f"  Unique delivery_id:        {deliveries_src['delivery_id'].nunique():>8,}")
print(f"  Unique branch:             {deliveries_src['branch'].nunique():>8,}")
print(f"  Unique client_id:          {deliveries_src['client_id'].nunique():>8,}")
print(f"  Unique driver_id:          {deliveries_src['driver_id'].nunique():>8,}")
print(f"  Unique vehicle_type:       {deliveries_src['vehicle_type'].nunique():>8,}")
print(f"  Unique parcel_category:    {deliveries_src['parcel_category'].nunique():>8,}")
print(f"  Unique delivery_priority:  {deliveries_src['delivery_priority'].nunique():>8,}")

print("\nDeliveries - Branch Distribution:")
branch_dist = deliveries_src['branch'].value_counts()
for branch, count in branch_dist.items():
    pct = (count / len(deliveries_src) * 100)
    print(f"  {str(branch):15s}: {count:>8,} ({pct:>5.1f}%)")

print("\nFeedback - Key Dimensions:")
print(f"  Unique feedback_id:        {feedback_src['feedback_id'].nunique():>8,}")
print(f"  Unique delivery_id:        {feedback_src['delivery_id'].nunique():>8,}")
print(f"  Unique rating:             {feedback_src['rating'].nunique():>8,}")

print("\nFeedback - Rating Distribution:")
rating_dist = feedback_src['rating'].value_counts().sort_index(ascending=False)
for rating, count in rating_dist.items():
    pct = (count / len(feedback_src) * 100)
    stars = "★" * int(rating)
    print(f"  {int(rating)} stars {stars:5s}: {count:>8,} ({pct:>5.1f}%)")

# ============================================================================
# TASK 6: DATE RANGES
# ============================================================================
print("\n" + "=" * 120)
print("5. DATE RANGES VALIDATION")
print("=" * 120)

# Parse dates
deliveries_src['booking_datetime_parsed'] = pd.to_datetime(deliveries_src['booking_datetime'], format='%d/%m/%Y %H:%M', errors='coerce')
deliveries_src['delivery_datetime_parsed'] = pd.to_datetime(deliveries_src['delivery_datetime'], format='%d/%m/%Y %H:%M', errors='coerce')
deliveries_src['promised_datetime_parsed'] = pd.to_datetime(deliveries_src['promised_delivery_datetime'], format='%d/%m/%Y %H:%M', errors='coerce')
feedback_src['feedback_datetime_parsed'] = pd.to_datetime(feedback_src['feedback_datetime'], format='%d/%m/%Y %H:%M', errors='coerce')

print("\nDeliveries Date Range:")
print(f"  Booking:       {deliveries_src['booking_datetime_parsed'].min()} to {deliveries_src['booking_datetime_parsed'].max()}")
print(f"  Delivery:      {deliveries_src['delivery_datetime_parsed'].min()} to {deliveries_src['delivery_datetime_parsed'].max()}")
print(f"  Parse errors:  {deliveries_src['booking_datetime_parsed'].isnull().sum()} rows")

print("\nFeedback Date Range:")
print(f"  Feedback:      {feedback_src['feedback_datetime_parsed'].min()} to {feedback_src['feedback_datetime_parsed'].max()}")
print(f"  Parse errors:  {feedback_src['feedback_datetime_parsed'].isnull().sum()} rows")

# ============================================================================
# TASK 7: NUMERICAL SUMMARY STATISTICS
# ============================================================================
print("\n" + "=" * 120)
print("6. NUMERICAL STATISTICS VALIDATION")
print("=" * 120)

print("\nDeliveries Numeric Columns:")
numeric_cols = ['distance_km', 'parcel_weight_kg', 'parcel_value_sgd', 'num_stops_on_route', 'driver_experience_months']
for col in numeric_cols:
    if col in deliveries_src.columns:
        print(f"\n  {col}:")
        print(f"    Count:     {deliveries_src[col].notna().sum():>10,}")
        print(f"    Min:       {deliveries_src[col].min():>10.2f}")
        print(f"    Mean:      {deliveries_src[col].mean():>10.2f}")
        print(f"    Median:    {deliveries_src[col].median():>10.2f}")
        print(f"    Max:       {deliveries_src[col].max():>10.2f}")
        print(f"    Std Dev:   {deliveries_src[col].std():>10.2f}")

print("\nFeedback Numeric Columns:")
print(f"\n  rating:")
print(f"    Count:     {feedback_src['rating'].notna().sum():>10,}")
print(f"    Min:       {feedback_src['rating'].min():>10.2f}")
print(f"    Mean:      {feedback_src['rating'].mean():>10.2f}")
print(f"    Median:    {feedback_src['rating'].median():>10.2f}")
print(f"    Max:       {feedback_src['rating'].max():>10.2f}")

# ============================================================================
# TASK 8: ON-TIME DELIVERY METRIC
# ============================================================================
print("\n" + "=" * 120)
print("7. ON-TIME DELIVERY VALIDATION")
print("=" * 120)

deliveries_src['on_time'] = deliveries_src['delivery_datetime_parsed'] <= deliveries_src['promised_datetime_parsed']
on_time_count = deliveries_src['on_time'].sum()
on_time_pct = (on_time_count / len(deliveries_src) * 100)
late_count = (~deliveries_src['on_time']).sum()
late_pct = (late_count / len(deliveries_src) * 100)

print(f"\nOn-Time Deliveries:")
print(f"  On-time: {on_time_count:>10,} ({on_time_pct:>5.1f}%)")
print(f"  Late:    {late_count:>10,} ({late_pct:>5.1f}%)")

# ============================================================================
# TASK 9: FEEDBACK COVERAGE
# ============================================================================
print("\n" + "=" * 120)
print("8. FEEDBACK COVERAGE VALIDATION")
print("=" * 120)

feedback_coverage = feedback_src['delivery_id'].nunique()
total_deliveries = deliveries_src['delivery_id'].nunique()
coverage_pct = (feedback_coverage / total_deliveries * 100)

print(f"\nFeedback Coverage:")
print(f"  Total deliveries:      {total_deliveries:>10,}")
print(f"  Deliveries with feedback: {feedback_coverage:>10,}")
print(f"  Coverage:              {coverage_pct:>10.1f}%")

print("\n" + "=" * 120)
print("✅ SOURCE DATA ANALYSIS COMPLETE")
print("=" * 120)
