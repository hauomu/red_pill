import pandas as pd
import re

df = pd.read_csv('data_exports/deliveries_feedback_merged.csv', encoding='latin-1')
df['booking_dt'] = pd.to_datetime(df['booking_datetime'], format='%d/%m/%Y %H:%M', errors='coerce')
feedback_df = df[df['rating'].notna()].copy()
feedback_df['sentiment'] = feedback_df['rating'].apply(lambda x: 'Positive' if x >= 4 else ('Negative' if x <= 2 else 'Neutral'))

negative_feedback = feedback_df[feedback_df['sentiment'] == 'Negative'].copy()

# Complaint categorization
complaint_patterns = {
    'Late Delivery': r'(late|slow|hours late|promised window|delay)',
    'Poor Communication': r'(communication|no (update|notification)|not informed)',
    'Driver Behavior': r'(rude|unprofessional|careless|rough)',
    'Package Damage': r'(damage|broken|damaged|roughly handled)',
    'Other': r'.*'
}

def categorize_complaint(comment):
    if pd.isna(comment):
        return 'No Comment'
    comment_lower = str(comment).lower()
    for category, pattern in complaint_patterns.items():
        if re.search(pattern, comment_lower):
            return category
    return 'Other'

negative_feedback['complaint_category'] = negative_feedback['comment'].apply(categorize_complaint)

print("\n" + "="*160)
print("FULL VEHICLE TYPE CORRELATION WITH COMPLAINT CATEGORIES")
print("="*160)

vehicle_complaint = pd.crosstab(
    negative_feedback['vehicle_type'], 
    negative_feedback['complaint_category'], 
    margins=True
)

# Set pandas display options for full output
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

print(vehicle_complaint)

print("\n" + "="*160)
print("VEHICLE TYPE - COMPLAINT PERCENTAGE BREAKDOWN")
print("="*160)

# Calculate percentages by vehicle type
for vehicle in vehicle_complaint.index[:-1]:  # Exclude 'All' row
    print(f"\n{vehicle}:")
    total = vehicle_complaint.loc[vehicle, 'All']
    for complaint in vehicle_complaint.columns[:-1]:  # Exclude 'All' column
        count = vehicle_complaint.loc[vehicle, complaint]
        pct = (count / total * 100) if total > 0 else 0
        print(f"  {complaint:20} : {count:4} ({pct:5.1f}%)")

print("\n" + "="*160)
print("INSIGHTS: VEHICLE QUALITY ISSUES")
print("="*160)

# Rank vehicles by complaint severity
print("\nVehicles Ranked by Complaint Rate (Total Complaints / Total Deliveries):")
for vehicle in ['van', 'bike', 'truck']:
    vehicle_df = feedback_df[feedback_df['vehicle_type'] == vehicle]
    negative_count = len(vehicle_df[vehicle_df['sentiment'] == 'Negative'])
    total_count = len(vehicle_df)
    complaint_rate = (negative_count / total_count * 100) if total_count > 0 else 0
    print(f"  {vehicle:10} : {negative_count:4} complaints / {total_count:5} deliveries = {complaint_rate:5.2f}% complaint rate")
