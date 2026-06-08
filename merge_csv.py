import pandas as pd
import os

print("Merging deliveries and feedback CSV files...\n")

# Read the CSV files from Db-Browser folder
deliveries_path = r'Db-Browser\deliveries.csv'
feedback_path = r'Db-Browser\feedback.csv'

print(f"📦 Reading: {deliveries_path}")
df_deliveries = pd.read_csv(deliveries_path)
print(f"   ✅ Loaded: {len(df_deliveries):,} delivery records")
print(f"   Columns: {list(df_deliveries.columns)[:5]}... ({len(df_deliveries.columns)} total)")

print(f"\n⭐ Reading: {feedback_path}")
df_feedback = pd.read_csv(feedback_path, encoding='latin-1')
print(f"   ✅ Loaded: {len(df_feedback):,} feedback records")
print(f"   Columns: {list(df_feedback.columns)}")

# Merge on delivery_id
print(f"\n🔗 Merging on delivery_id...")
df_merged = pd.merge(df_deliveries, df_feedback, on='delivery_id', how='left')

print(f"\n✅ MERGE COMPLETE")
print(f"   Total rows in merged file: {len(df_merged):,}")
print(f"   Total columns: {len(df_merged.columns)}")
print(f"   Deliveries with feedback: {df_merged['rating'].notna().sum():,}")
print(f"   Deliveries without feedback: {df_merged['rating'].isna().sum():,}")

# Display column names
print(f"\n📋 Merged columns ({len(df_merged.columns)} total):")
for i, col in enumerate(df_merged.columns, 1):
    print(f"   {i:2}. {col}")

# Save merged file
output_path = 'data_exports/deliveries_feedback_merged.csv'
os.makedirs('data_exports', exist_ok=True)
df_merged.to_csv(output_path, index=False)
print(f"\n✅ Saved to: {output_path}")
print(f"   File size: {os.path.getsize(output_path) / 1024 / 1024:.2f} MB")

# Show sample of merged data
print(f"\n📊 Sample of merged data (first 5 rows):")
print("="*100)
print(df_merged.head().to_string())

print("\n" + "="*100)
print("✅ Merge complete! Full dataset saved to: data_exports/deliveries_feedback_merged.csv")
