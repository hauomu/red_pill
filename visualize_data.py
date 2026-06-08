import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

conn = sqlite3.connect('delivery.db')

# Create figure with subplots
fig = plt.figure(figsize=(16, 14))

# 1. Deliveries by Branch
ax1 = plt.subplot(3, 3, 1)
query = "SELECT branch, COUNT(*) as count FROM deliveries WHERE branch IN ('Central', 'East', 'West', 'North') GROUP BY branch ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
ax1.bar(df['branch'], df['count'], color=colors, edgecolor='black', linewidth=1.5)
ax1.set_title('Deliveries by Branch', fontsize=12, fontweight='bold')
ax1.set_ylabel('Count')
for i, v in enumerate(df['count']):
    ax1.text(i, v, f'{v:,}', ha='center', va='bottom', fontsize=9)

# 2. Vehicle Type Distribution
ax2 = plt.subplot(3, 3, 2)
query = "SELECT vehicle_type, COUNT(*) as count FROM deliveries WHERE vehicle_type IN ('van', 'bike', 'truck') GROUP BY vehicle_type ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
ax2.pie(df['count'], labels=df['vehicle_type'], autopct='%1.1f%%', colors=['#FF9999', '#66B2FF', '#99FF99'], startangle=90)
ax2.set_title('Vehicle Type Distribution', fontsize=12, fontweight='bold')

# 3. Delivery Priority Distribution
ax3 = plt.subplot(3, 3, 3)
query = "SELECT delivery_priority, COUNT(*) as count FROM deliveries GROUP BY delivery_priority ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
ax3.barh(df['delivery_priority'], df['count'], color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A'], edgecolor='black', linewidth=1.5)
ax3.set_title('Delivery Priority Distribution', fontsize=12, fontweight='bold')
ax3.set_xlabel('Count')
for i, v in enumerate(df['count']):
    ax3.text(v, i, f'{v:,}', ha='left', va='center', fontsize=9)

# 4. Parcel Category Distribution
ax4 = plt.subplot(3, 3, 4)
query = "SELECT parcel_category, COUNT(*) as count FROM deliveries WHERE parcel_category IN ('standard', 'fragile', 'oversized', 'refrigerated') GROUP BY parcel_category ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
ax4.pie(df['count'], labels=df['parcel_category'], autopct='%1.1f%%', colors=['#FFD700', '#FF6347', '#4169E1', '#32CD32'], startangle=45)
ax4.set_title('Parcel Category Distribution', fontsize=12, fontweight='bold')

# 5. On-time vs Late Deliveries
ax5 = plt.subplot(3, 3, 5)
query = """
SELECT 
    CASE WHEN delivery_datetime <= promised_delivery_datetime THEN 'On-time' ELSE 'Late' END as status,
    COUNT(*) as count
FROM deliveries
GROUP BY status
"""
df = pd.read_sql_query(query, conn)
colors_status = ['#90EE90', '#FF6B6B']
ax5.bar(df['status'], df['count'], color=colors_status, edgecolor='black', linewidth=2, width=0.6)
ax5.set_title('On-time vs Late Deliveries', fontsize=12, fontweight='bold')
ax5.set_ylabel('Count')
for i, v in enumerate(df['count']):
    pct = (v / df['count'].sum()) * 100
    ax5.text(i, v, f'{v:,}\n({pct:.1f}%)', ha='center', va='bottom', fontsize=9, fontweight='bold')

# 6. Rating Distribution (Stars)
ax6 = plt.subplot(3, 3, 6)
query = "SELECT rating, COUNT(*) as count FROM feedback WHERE rating IS NOT NULL GROUP BY rating ORDER BY rating"
df = pd.read_sql_query(query, conn)
df['rating'] = df['rating'].astype(int)
colors_rating = ['#FF6B6B', '#FFA07A', '#FFD700', '#90EE90', '#32CD32']
bars = ax6.bar(df['rating'].astype(str), df['count'], color=colors_rating, edgecolor='black', linewidth=1.5)
ax6.set_title('Customer Rating Distribution', fontsize=12, fontweight='bold')
ax6.set_xlabel('Stars')
ax6.set_ylabel('Count')
for i, (idx, row) in enumerate(df.iterrows()):
    ax6.text(i, row['count'], f"{row['count']:,}", ha='center', va='bottom', fontsize=9)

# 7. Distance Distribution
ax7 = plt.subplot(3, 3, 7)
query = "SELECT distance_km FROM deliveries WHERE distance_km > 0 ORDER BY distance_km"
df = pd.read_sql_query(query, conn)
ax7.hist(df['distance_km'], bins=30, color='#4ECDC4', edgecolor='black', alpha=0.7)
ax7.set_title('Distance Distribution', fontsize=12, fontweight='bold')
ax7.set_xlabel('Distance (km)')
ax7.set_ylabel('Frequency')
ax7.axvline(df['distance_km'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["distance_km"].mean():.2f} km')
ax7.legend()

# 8. Payment Method Distribution
ax8 = plt.subplot(3, 3, 8)
query = "SELECT payment_method, COUNT(*) as count FROM deliveries WHERE payment_method IN ('prepaid', 'cod') GROUP BY payment_method ORDER BY count DESC"
df = pd.read_sql_query(query, conn)
ax8.pie(df['count'], labels=df['payment_method'], autopct='%1.1f%%', colors=['#FF9999', '#66B2FF'], startangle=90)
ax8.set_title('Payment Method Distribution', fontsize=12, fontweight='bold')

# 9. Rating by Delivery Status (Most Important)
ax9 = plt.subplot(3, 3, 9)
query = """
SELECT 
    CASE WHEN delivery_datetime <= promised_delivery_datetime THEN 'On-time' ELSE 'Late' END as delivery_status,
    rating,
    COUNT(*) as count
FROM deliveries d
LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
WHERE f.rating IS NOT NULL
GROUP BY delivery_status, rating
ORDER BY delivery_status, rating
"""
df = pd.read_sql_query(query, conn)

# Separate on-time and late
on_time = df[df['delivery_status'] == 'On-time'].sort_values('rating')
late = df[df['delivery_status'] == 'Late'].sort_values('rating')

x = range(1, 6)
width = 0.35
ax9.bar([i - width/2 for i in x], on_time['count'].values if len(on_time) == 5 else [on_time[on_time['rating']==i]['count'].values[0] if i in on_time['rating'].values else 0 for i in range(1, 6)], width, label='On-time', color='#90EE90', edgecolor='black', linewidth=1.5)
ax9.bar([i + width/2 for i in x], late['count'].values if len(late) == 5 else [late[late['rating']==i]['count'].values[0] if i in late['rating'].values else 0 for i in range(1, 6)], width, label='Late', color='#FF6B6B', edgecolor='black', linewidth=1.5)

ax9.set_title('Rating by Delivery Status', fontsize=12, fontweight='bold')
ax9.set_xlabel('Rating')
ax9.set_ylabel('Count')
ax9.set_xticks(x)
ax9.legend()

plt.tight_layout()
plt.savefig('delivery_analysis_dashboard.png', dpi=300, bbox_inches='tight')
print("✅ Dashboard saved: delivery_analysis_dashboard.png")

# Create a second figure for key metrics
fig2, axes = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle('MoveEasy Delivery Performance - Key Metrics', fontsize=16, fontweight='bold', y=0.995)

# Metric 1: On-time rate by branch
ax = axes[0, 0]
query = """
SELECT branch, 
       COUNT(*) as total,
       SUM(CASE WHEN delivery_datetime <= promised_delivery_datetime THEN 1 ELSE 0 END) as on_time
FROM deliveries 
WHERE branch IN ('Central', 'East', 'West', 'North')
GROUP BY branch
ORDER BY total DESC
"""
df = pd.read_sql_query(query, conn)
df['on_time_pct'] = (df['on_time'] / df['total'] * 100).round(1)
bars = ax.bar(df['branch'], df['on_time_pct'], color=['#90EE90', '#FFD700', '#FFA07A', '#FF6B6B'], edgecolor='black', linewidth=2)
ax.set_title('On-time Delivery Rate by Branch', fontsize=12, fontweight='bold')
ax.set_ylabel('On-time %')
ax.set_ylim(0, 100)
for i, (idx, row) in enumerate(df.iterrows()):
    ax.text(i, row['on_time_pct'], f"{row['on_time_pct']:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

# Metric 2: Average rating by branch
ax = axes[0, 1]
query = """
SELECT d.branch, AVG(f.rating) as avg_rating, COUNT(f.rating) as count
FROM deliveries d
LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
WHERE d.branch IN ('Central', 'East', 'West', 'North') AND f.rating IS NOT NULL
GROUP BY d.branch
ORDER BY avg_rating DESC
"""
df = pd.read_sql_query(query, conn)
bars = ax.bar(df['branch'], df['avg_rating'], color=['#32CD32', '#90EE90', '#FFD700', '#FFA07A'], edgecolor='black', linewidth=2)
ax.set_title('Average Customer Rating by Branch', fontsize=12, fontweight='bold')
ax.set_ylabel('Average Rating')
ax.set_ylim(0, 5)
for i, (idx, row) in enumerate(df.iterrows()):
    ax.text(i, row['avg_rating'], f"{row['avg_rating']:.2f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

# Metric 3: Late deliveries by priority
ax = axes[1, 0]
query = """
SELECT delivery_priority,
       COUNT(*) as total,
       SUM(CASE WHEN delivery_datetime > promised_delivery_datetime THEN 1 ELSE 0 END) as late
FROM deliveries
GROUP BY delivery_priority
ORDER BY delivery_priority
"""
df = pd.read_sql_query(query, conn)
df['late_pct'] = (df['late'] / df['total'] * 100).round(1)
bars = ax.bar(df['delivery_priority'], df['late_pct'], color=['#FF6B6B', '#FFA07A', '#FFD700', '#FF1493'], edgecolor='black', linewidth=2)
ax.set_title('Late Delivery Rate by Priority', fontsize=12, fontweight='bold')
ax.set_ylabel('Late %')
for i, (idx, row) in enumerate(df.iterrows()):
    ax.text(i, row['late_pct'], f"{row['late_pct']:.1f}%", ha='center', va='bottom', fontsize=9, fontweight='bold')

# Metric 4: Feedback coverage by branch
ax = axes[1, 1]
query = """
SELECT d.branch, 
       COUNT(DISTINCT d.delivery_id) as total_deliveries,
       COUNT(DISTINCT f.delivery_id) as with_feedback
FROM deliveries d
LEFT JOIN feedback f ON d.delivery_id = f.delivery_id
WHERE d.branch IN ('Central', 'East', 'West', 'North')
GROUP BY d.branch
ORDER BY total_deliveries DESC
"""
df = pd.read_sql_query(query, conn)
df['feedback_pct'] = (df['with_feedback'] / df['total_deliveries'] * 100).round(1)
bars = ax.bar(df['branch'], df['feedback_pct'], color=['#4ECDC4', '#45B7D1', '#40E0D0', '#20B2AA'], edgecolor='black', linewidth=2)
ax.set_title('Feedback Coverage by Branch', fontsize=12, fontweight='bold')
ax.set_ylabel('Feedback %')
ax.set_ylim(0, 100)
for i, (idx, row) in enumerate(df.iterrows()):
    ax.text(i, row['feedback_pct'], f"{row['feedback_pct']:.1f}%", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('delivery_key_metrics.png', dpi=300, bbox_inches='tight')
print("✅ Key metrics saved: delivery_key_metrics.png")

conn.close()
plt.show()
print("\n✅ All visualizations complete!")
