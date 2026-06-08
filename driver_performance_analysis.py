import pandas as pd
import numpy as np

print("Generating Best and Worst Drivers Performance Report...\n")

df = pd.read_csv('data_exports/deliveries_feedback_merged.csv', encoding='latin-1')
print(f"✅ Loaded: {len(df):,} rows")

# Note: delivery_datetime and promised_delivery_datetime are truncated in export
# For now, we'll exclude on_time metric from driver analysis
# We'll focus on feedback-based metrics instead

# Calculate driver performance metrics
print("\n🔍 Analyzing driver performance...\n")

driver_stats = []

for driver_id in df['driver_id'].unique():
    if pd.isna(driver_id):
        continue
        
    driver_df = df[df['driver_id'] == driver_id]
    
    # Basic metrics
    total_deliveries = len(driver_df)
    if total_deliveries < 10:  # Only consider drivers with 10+ deliveries
        continue
    
    # Rating metrics
    feedback_df = driver_df[driver_df['rating'].notna()]
    num_with_feedback = len(feedback_df)
    
    if num_with_feedback == 0:
        continue
    
    avg_rating = feedback_df['rating'].mean()
    std_rating = feedback_df['rating'].std()
    min_rating = feedback_df['rating'].min()
    max_rating = feedback_df['rating'].max()
    
    # Sentiment
    positive = len(feedback_df[feedback_df['rating'] >= 4])
    negative = len(feedback_df[feedback_df['rating'] <= 2])
    positive_pct = (positive / num_with_feedback * 100)
    negative_pct = (negative / num_with_feedback * 100)
    
    # On-time performance (skipped due to data quality issue)
    on_time_pct = 0  # Placeholder
    
    # Vehicle and experience
    vehicle_type = driver_df['vehicle_type'].mode()[0] if len(driver_df['vehicle_type'].mode()) > 0 else 'Unknown'
    avg_experience = driver_df['driver_experience_months'].mean()
    avg_distance = driver_df['distance_km'].mean()
    depot = driver_df['branch'].mode()[0] if len(driver_df['branch'].mode()) > 0 else 'Unknown'
    
    driver_stats.append({
        'Driver ID': driver_id,
        'Total Deliveries': total_deliveries,
        'Deliveries with Feedback': num_with_feedback,
        'Avg Rating': round(avg_rating, 2),
        'Service Consistency (Std Dev)': round(std_rating, 2),
        'Min Rating': min_rating,
        'Max Rating': max_rating,
        'Positive %': round(positive_pct, 1),
        'Negative %': round(negative_pct, 1),
        'Avg Distance (km)': round(avg_distance, 2),
        'Avg Experience (months)': round(avg_experience, 1),
        'Vehicle Type': vehicle_type,
        'Primary Depot': depot
    })

all_drivers = pd.DataFrame(driver_stats)

# Create performance score (weighted metric)
all_drivers['Performance Score'] = (
    all_drivers['Avg Rating'] * 0.5 +           # 50% - rating quality
    (10 - all_drivers['Service Consistency (Std Dev)']) * 0.3 +  # 30% - consistency (lower std dev is better)
    all_drivers['Positive %'] * 0.2             # 20% - positive feedback %
).round(1)

# Separate best and worst drivers
top_20_pct = int(len(all_drivers) * 0.2)
best_drivers = all_drivers.nlargest(top_20_pct, 'Performance Score').reset_index(drop=True)
worst_drivers = all_drivers.nsmallest(top_20_pct, 'Performance Score').reset_index(drop=True)

# Save CSVs
best_drivers_sorted = best_drivers.sort_values('Performance Score', ascending=False)
worst_drivers_sorted = worst_drivers.sort_values('Performance Score', ascending=True)

best_drivers_sorted.to_csv('data_exports/best_drivers.csv', index=False, encoding='latin-1')
worst_drivers_sorted.to_csv('data_exports/worst_drivers.csv', index=False, encoding='latin-1')
all_drivers.sort_values('Performance Score', ascending=False).to_csv('data_exports/all_drivers_ranked.csv', index=False, encoding='latin-1')

print("="*140)
print("BEST DRIVERS (Top 20%)")
print("="*140)
print(best_drivers_sorted[['Driver ID', 'Total Deliveries', 'Avg Rating', 'Service Consistency (Std Dev)', 'Positive %', 'Performance Score', 'Vehicle Type', 'Primary Depot']].head(10).to_string(index=False))

print("\n" + "="*140)
print("WORST DRIVERS (Bottom 20%)")
print("="*140)
print(worst_drivers_sorted[['Driver ID', 'Total Deliveries', 'Avg Rating', 'Service Consistency (Std Dev)', 'Negative %', 'Performance Score', 'Vehicle Type', 'Primary Depot']].head(10).to_string(index=False))

print("\n" + "="*140)
print("SUMMARY STATISTICS")
print("="*140)
print(f"Total Drivers Analyzed: {len(all_drivers)}")
print(f"Best Drivers (Top 20%): {len(best_drivers)}")
print(f"Worst Drivers (Bottom 20%): {len(worst_drivers)}")
print(f"\nOverall Avg Rating: {all_drivers['Avg Rating'].mean():.2f}/5.0")
print(f"Overall Avg Service Consistency: ±{all_drivers['Service Consistency (Std Dev)'].mean():.2f}")
print(f"Overall Avg Performance Score: {all_drivers['Performance Score'].mean():.1f}")

print("\n" + "="*140)
print("FILES CREATED")
print("="*140)
print(f"✅ data_exports/best_drivers.csv ({len(best_drivers)} drivers)")
print(f"✅ data_exports/worst_drivers.csv ({len(worst_drivers)} drivers)")
print(f"✅ data_exports/all_drivers_ranked.csv ({len(all_drivers)} drivers - full ranking)")
