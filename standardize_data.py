import pandas as pd

print("Standardizing data quality issues...\n")

df = pd.read_csv('data_exports/deliveries_feedback_merged.csv', encoding='latin-1')
print(f"✅ Loaded: {len(df):,} rows")

# Before standardization
print("\n" + "="*100)
print("BEFORE STANDARDIZATION")
print("="*100)
print(f"\nvehicle_type unique values: {sorted([x for x in df['vehicle_type'].unique() if pd.notna(x)])}")
print(f"branch unique values: {sorted([x for x in df['branch'].unique() if pd.notna(x)])}")
print(f"delivery_priority unique values: {sorted([x for x in df['delivery_priority'].unique() if pd.notna(x)])}")
print(f"parcel_category unique values: {sorted([x for x in df['parcel_category'].unique() if pd.notna(x)])}")
print(f"payment_method unique values: {sorted([x for x in df['payment_method'].unique() if pd.notna(x)])}")

# Standardize to lowercase
print("\n🔧 Applying standardization...")

df['vehicle_type'] = df['vehicle_type'].str.lower().str.strip()
df['branch'] = df['branch'].str.lower().str.strip()
df['delivery_priority'] = df['delivery_priority'].str.lower().str.strip()
df['parcel_category'] = df['parcel_category'].str.lower().str.strip()
df['payment_method'] = df['payment_method'].str.lower().str.strip()

# After standardization
print("\n" + "="*100)
print("AFTER STANDARDIZATION")
print("="*100)
print(f"\nvehicle_type unique values: {sorted([x for x in df['vehicle_type'].unique() if pd.notna(x)])}")
print(f"branch unique values: {sorted([x for x in df['branch'].unique() if pd.notna(x)])}")
print(f"delivery_priority unique values: {sorted([x for x in df['delivery_priority'].unique() if pd.notna(x)])}")
print(f"parcel_category unique values: {sorted([x for x in df['parcel_category'].unique() if pd.notna(x)])}")
print(f"payment_method unique values: {sorted([x for x in df['payment_method'].unique() if pd.notna(x)])}")

# Value counts for verification
print("\n" + "="*100)
print("VALUE DISTRIBUTION (Standardized)")
print("="*100)
print(f"\nvehicle_type distribution:")
print(df['vehicle_type'].value_counts().to_string())

print(f"\nbranch distribution:")
print(df['branch'].value_counts().to_string())

print(f"\ndelivery_priority distribution:")
print(df['delivery_priority'].value_counts().to_string())

# Save standardized CSV
output_path = 'data_exports/deliveries_feedback_merged.csv'
df.to_csv(output_path, index=False, encoding='latin-1')
print(f"\n✅ Standardized data saved to: {output_path}")
print(f"   Total rows: {len(df):,}")
print(f"   Total columns: {len(df.columns)}")
print("\n📊 Data quality improved - all categorical columns now in lowercase!")
