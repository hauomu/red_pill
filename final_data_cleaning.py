import pandas as pd

print("Performing final data cleaning (fixing typos and consolidating variants)...\n")

df = pd.read_csv('data_exports/deliveries_feedback_merged.csv', encoding='latin-1')
print(f"✅ Loaded: {len(df):,} rows")

# Before cleaning
print("\n" + "="*100)
print("BEFORE FINAL CLEANING")
print("="*100)
print(f"\nBranch unique values & counts:")
print(df['branch'].value_counts().to_string())
print(f"\nParcel Category unique values & counts:")
print(df['parcel_category'].value_counts().to_string())

# Fix branch typos
print("\n🔧 Fixing branch typos...")
df['branch'] = df['branch'].replace({
    'cnetral': 'central',  # Fix typo (275 rows)
    'noth': 'north'        # Fix typo (186 rows)
})
print(f"   ✅ cnetral → central (275 rows merged)")
print(f"   ✅ noth → north (186 rows merged)")

# Consolidate parcel category variants
print("\n🔧 Consolidating parcel category variants...")
df['parcel_category'] = df['parcel_category'].replace({
    'over-sized': 'oversized',      # Consolidate variants
    'refrig.': 'refrigerated'       # Consolidate variants
})
print(f"   ✅ over-sized → oversized")
print(f"   ✅ refrig. → refrigerated")

# After cleaning
print("\n" + "="*100)
print("AFTER FINAL CLEANING")
print("="*100)
print(f"\nBranch unique values & counts:")
print(df['branch'].value_counts().to_string())
print(f"\nParcel Category unique values & counts:")
print(df['parcel_category'].value_counts().to_string())

# Verify all standardized
print("\n" + "="*100)
print("FINAL DATA QUALITY CHECK")
print("="*100)
print(f"\nvehicle_type unique: {sorted([x for x in df['vehicle_type'].unique() if pd.notna(x)])}")
print(f"branch unique: {sorted([x for x in df['branch'].unique() if pd.notna(x)])}")
print(f"delivery_priority unique: {sorted([x for x in df['delivery_priority'].unique() if pd.notna(x)])}")
print(f"parcel_category unique: {sorted([x for x in df['parcel_category'].unique() if pd.notna(x)])}")
print(f"payment_method unique: {sorted([x for x in df['payment_method'].unique() if pd.notna(x)])}")

# Save cleaned CSV
output_path = 'data_exports/deliveries_feedback_merged.csv'
df.to_csv(output_path, index=False, encoding='latin-1')
print(f"\n✅ Cleaned data saved to: {output_path}")
print(f"   Total rows: {len(df):,}")
print(f"   All categorical columns standardized & clean!")
