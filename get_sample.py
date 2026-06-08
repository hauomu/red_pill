import pandas as pd
import json

df = pd.read_csv('data_exports/deliveries_feedback_merged.csv', encoding='latin-1')

# Parse dates
df['delivery_datetime'] = pd.to_datetime(df['delivery_datetime'], format='%d/%m/%Y %H:%M', errors='coerce')
df['promised_delivery_datetime'] = pd.to_datetime(df['promised_delivery_datetime'], format='%d/%m/%Y %H:%M', errors='coerce')
df['on_time'] = df['delivery_datetime'] <= df['promised_delivery_datetime']

# Get samples
late_sample = df[(df['rating'].notna()) & (df['on_time'] == False)].iloc[0]
ontime_sample = df[(df['rating'].notna()) & (df['on_time'] == True)].iloc[0]

print("LATE DELIVERY SAMPLE:")
print(json.dumps({
    'delivery_id': str(late_sample['delivery_id']),
    'branch': str(late_sample['branch']),
    'vehicle': str(late_sample['vehicle_type']),
    'priority': str(late_sample['priority_level']),
    'distance_km': str(late_sample['distance_km']),
    'rating': str(late_sample['rating']),
    'comment': str(late_sample['comment'])[:100]
}, indent=2))

print("\n\nON-TIME DELIVERY SAMPLE:")
print(json.dumps({
    'delivery_id': str(ontime_sample['delivery_id']),
    'branch': str(ontime_sample['branch']),
    'vehicle': str(ontime_sample['vehicle_type']),
    'priority': str(ontime_sample['priority_level']),
    'distance_km': str(ontime_sample['distance_km']),
    'rating': str(ontime_sample['rating']),
    'comment': str(ontime_sample['comment'])[:100]
}, indent=2))
