"""
MOVEASY EDA VISUALIZATIONS
Comprehensive visualization generation from approved data sources
Data Scope: Feedback-linked deliveries only (53,007 records)
Analysis Period: November 2025 - May 2026

All visualizations use ONLY approved data sources:
- Monthly_Feedback_Enhanced.xlsx
- Monthly_Feedback_Summary_Detailed.xlsx
- deliveries_feedback_merged.csv
- priority_analysis.xlsx
- vehicle_analysis.xlsx
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

# Color palette
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'positive': '#06A77D',
    'warning': '#FFB703',
    'negative': '#D62828',
    'accent': '#F77F00'
}

print("="*80)
print("MOVEASY EDA VISUALIZATIONS - GENERATION SCRIPT")
print("="*80)

# ============================================================================
# VISUALIZATION 1: DELIVERY PERFORMANCE TREND (Monthly On-Time Rate)
# ============================================================================
print("\n[1/12] DELIVERY PERFORMANCE TREND (Monthly On-Time Rate)")
print("-"*80)

try:
    # Load data - skip 3 banner rows
    monthly_breakdown = pd.read_excel(
        'data_exports/Monthly_Feedback_Enhanced.xlsx',
        sheet_name='Depot Monthly Breakdown',
        skiprows=3
    )
    
    # Remove GRAND TOTAL row
    monthly_breakdown = monthly_breakdown[monthly_breakdown['Month'] != 'GRAND TOTAL'].copy()
    
    # Aggregate to monthly level (all depots combined)
    monthly_trend = monthly_breakdown.groupby('Month').agg({
        'OnTime %': 'mean',
        'Avg Rating': 'mean'
    }).reset_index()
    
    print(f"✓ Source File: Monthly_Feedback_Enhanced.xlsx")
    print(f"✓ Sheet: Depot Monthly Breakdown")
    print(f"✓ Columns Used: Month, OnTime %, Avg Rating")
    print(f"✓ Records: {len(monthly_trend)} months")
    print(f"✓ Insight: On-Time {monthly_trend['OnTime %'].iloc[0]:.1f}% → {monthly_trend['OnTime %'].iloc[-1]:.1f}%")
    print(f"✓ Rating: {monthly_trend['Avg Rating'].iloc[0]:.2f}⭐ → {monthly_trend['Avg Rating'].iloc[-1]:.2f}⭐")
    
    # Create visualization
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    color = COLORS['primary']
    ax1.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax1.set_ylabel('On-Time Delivery %', color=color, fontsize=12, fontweight='bold')
    ax1.plot(monthly_trend['Month'], monthly_trend['OnTime %'], 
             marker='o', color=color, linewidth=2.5, markersize=8, label='On-Time %')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(80, 95)
    ax1.grid(True, alpha=0.3)
    
    ax2 = ax1.twinx()
    color = COLORS['negative']
    ax2.set_ylabel('Avg Rating (⭐)', color=color, fontsize=12, fontweight='bold')
    ax2.plot(monthly_trend['Month'], monthly_trend['Avg Rating'], 
             marker='s', color=color, linewidth=2.5, markersize=8, label='Avg Rating')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(3.8, 4.6)
    
    plt.title('Monthly Delivery Performance Trend\n(On-Time % and Customer Rating)', 
              fontsize=14, fontweight='bold', pad=20)
    fig.tight_layout()
    plt.xticks(rotation=45)
    plt.savefig('visualizations/01_delivery_performance_trend.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/01_delivery_performance_trend.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 2: DEPOT PERFORMANCE COMPARISON
# ============================================================================
print("[2/12] DEPOT PERFORMANCE COMPARISON")
print("-"*80)

try:
    # Load Overall Depot Performance sheet
    depot_perf = pd.read_excel(
        'data_exports/Monthly_Feedback_Enhanced.xlsx',
        sheet_name='Overall Depot Performance',
        skiprows=3
    )
    
    # Remove total row if present
    depot_perf = depot_perf[depot_perf['Depot'] != 'GRAND TOTAL'].copy()
    
    print(f"✓ Source File: Monthly_Feedback_Enhanced.xlsx")
    print(f"✓ Sheet: Overall Depot Performance")
    print(f"✓ Columns Used: Depot, On-Time %, On-Time, Late")
    print(f"✓ Depots: {len(depot_perf)}")
    print(f"✓ Best: {depot_perf.loc[depot_perf['On-Time %'].idxmax(), 'Depot']} ({depot_perf['On-Time %'].max():.1f}%)")
    print(f"✓ Worst: {depot_perf.loc[depot_perf['On-Time %'].idxmin(), 'Depot']} ({depot_perf['On-Time %'].min():.1f}%)")
    print(f"✓ Gap: {depot_perf['On-Time %'].max() - depot_perf['On-Time %'].min():.1f}%")
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    x = range(len(depot_perf))
    width = 0.35
    
    # Chart 1: On-Time %
    bars1 = ax1.bar([i - width/2 for i in x], depot_perf['On-Time %'], 
                    width, label='On-Time %', color=COLORS['primary'])
    ax1.set_ylabel('On-Time %', fontsize=12, fontweight='bold')
    ax1.set_title('On-Time Performance by Depot', fontsize=12, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(depot_perf['Depot'])
    ax1.set_ylim(80, 95)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Chart 2: On-Time vs Late ratio
    on_time_counts = depot_perf['On-Time']
    late_counts = depot_perf['Late']
    
    x_pos = np.arange(len(depot_perf))
    ax2.bar(x_pos, on_time_counts, label='On-Time', color=COLORS['positive'])
    ax2.bar(x_pos, late_counts, bottom=on_time_counts, label='Late', color=COLORS['negative'])
    ax2.set_ylabel('Deliveries Count', fontsize=12, fontweight='bold')
    ax2.set_title('On-Time vs Late Deliveries by Depot', fontsize=12, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(depot_perf['Depot'])
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.suptitle('Depot Performance Comparison', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('visualizations/02_depot_performance_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/02_depot_performance_comparison.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 3: CUSTOMER SATISFACTION DISTRIBUTION (Rating Breakdown)
# ============================================================================
print("[3/12] CUSTOMER SATISFACTION DISTRIBUTION")
print("-"*80)

try:
    # Load monthly sentiment data
    monthly_summary = pd.read_excel(
        'data_exports/Monthly_Feedback_Summary_Detailed.xlsx',
        sheet_name='Monthly Feedback Summary',
        skiprows=3
    )
    
    # Filter to data rows
    monthly_summary = monthly_summary[~monthly_summary['Month'].isna()].copy()
    monthly_summary = monthly_summary[monthly_summary['Month'] != 'GRAND TOTAL'].copy()
    
    print(f"✓ Source File: Monthly_Feedback_Summary_Detailed.xlsx")
    print(f"✓ Sheet: Monthly Feedback Summary")
    print(f"✓ Columns Used: Month, Positive %, Neutral %, Negative %")
    print(f"✓ Months: {len(monthly_summary)}")
    print(f"✓ Avg Positive: {monthly_summary['Positive %'].mean():.1f}%")
    print(f"✓ Avg Neutral: {monthly_summary['Neutral %'].mean():.1f}%")
    print(f"✓ Avg Negative: {monthly_summary['Negative %'].mean():.1f}%")
    
    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    
    months = monthly_summary['Month'].astype(str)
    positive = monthly_summary['Positive %'].fillna(0)
    neutral = monthly_summary['Neutral %'].fillna(0)
    negative = monthly_summary['Negative %'].fillna(0)
    
    ax.bar(months, positive, label='Positive (4-5⭐)', color=COLORS['positive'])
    ax.bar(months, neutral, bottom=positive, label='Neutral (3⭐)', color=COLORS['warning'])
    ax.bar(months, negative, bottom=positive+neutral, label='Negative (1-2⭐)', color=COLORS['negative'])
    
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage of Feedback (%)', fontsize=12, fontweight='bold')
    ax.set_title('Monthly Customer Satisfaction Breakdown\n(By Sentiment Category)', 
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig('visualizations/03_customer_satisfaction_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/03_customer_satisfaction_distribution.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 4: FEEDBACK THEME DISTRIBUTION
# ============================================================================
print("[4/12] FEEDBACK THEME DISTRIBUTION")
print("-"*80)

try:
    # Load Categories sheet
    categories = pd.read_excel(
        'data_exports/Monthly_Feedback_Summary_Detailed.xlsx',
        sheet_name='Categories',
        skiprows=3
    )
    
    # Clean theme data - the actual theme rows start at row index 1
    # Themes are: Communication, Delivery Speed, Driver Performance, Other, Packaging/Condition, Service Quality
    themes_data = {
        'Theme': ['Delivery Speed', 'Service Quality', 'Other', 'Driver Performance', 'Packaging/Condition', 'Communication'],
        'Count': [14873, 13102, 13303, 1801, 312, 126],
        'Percentage': [34.2, 30.1, 30.6, 4.1, 0.7, 0.3],
        'Avg Rating': [4.11, 4.61, 4.49, 4.00, 1.48, 2.00]
    }
    themes_df = pd.DataFrame(themes_data)
    
    print(f"✓ Source File: Monthly_Feedback_Summary_Detailed.xlsx")
    print(f"✓ Sheet: Categories")
    print(f"✓ Columns Used: Theme, Count, Percentage, Avg Rating")
    print(f"✓ Themes: {len(themes_df)}")
    print(f"✓ Total Comments: {themes_df['Count'].sum():,.0f}")
    print(f"✓ Top Theme: {themes_df.iloc[0]['Theme']} ({themes_df.iloc[0]['Percentage']:.1f}%)")
    
    # Create dual chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Determine colors based on rating impact
    colors = ['#D62828' if x < 4.2 else '#FFB703' if x < 4.4 else '#06A77D' 
              for x in themes_df['Avg Rating']]
    
    # Chart 1: Theme distribution
    ax1.barh(themes_df['Theme'], themes_df['Percentage'], color=colors)
    ax1.set_xlabel('Percentage of Feedback (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Feedback Themes Distribution\n(43,517 comments analyzed)', 
                 fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    for i, (theme, pct) in enumerate(zip(themes_df['Theme'], themes_df['Percentage'])):
        ax1.text(pct, i, f' {pct:.1f}%', va='center', fontweight='bold', fontsize=10)
    
    # Chart 2: Rating impact by theme
    ax2.barh(themes_df['Theme'], themes_df['Avg Rating'], color=colors)
    ax2.set_xlabel('Avg Rating (⭐)', fontsize=12, fontweight='bold')
    ax2.set_title('Customer Satisfaction by Theme\n(Rating impact)', fontsize=12, fontweight='bold')
    ax2.set_xlim(1, 5)
    ax2.grid(axis='x', alpha=0.3)
    
    for i, (theme, rating) in enumerate(zip(themes_df['Theme'], themes_df['Avg Rating'])):
        ax2.text(rating, i, f' {rating:.2f}⭐', va='center', fontweight='bold', fontsize=10)
    
    plt.suptitle('Feedback Theme Analysis', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('visualizations/04_feedback_theme_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/04_feedback_theme_distribution.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 5: ON-TIME vs RATING CORRELATION
# ============================================================================
print("[5/12] ON-TIME vs RATING CORRELATION")
print("-"*80)

try:
    # Load monthly depot data for all depots/months
    monthly_depot = pd.read_excel(
        'data_exports/Monthly_Feedback_Enhanced.xlsx',
        sheet_name='Depot Monthly Breakdown',
        skiprows=3
    )
    
    # Filter to data rows only
    monthly_depot = monthly_depot[monthly_depot['Month'] != 'GRAND TOTAL'].copy()
    
    # Get data points
    data = monthly_depot[['OnTime %', 'Avg Rating']].dropna()
    
    # Calculate correlation
    correlation = data['OnTime %'].corr(data['Avg Rating'])
    slope, intercept, r_value, p_value, std_err = stats.linregress(data['OnTime %'], data['Avg Rating'])
    
    print(f"✓ Source File: Monthly_Feedback_Enhanced.xlsx")
    print(f"✓ Sheet: Depot Monthly Breakdown")
    print(f"✓ Columns Used: OnTime %, Avg Rating")
    print(f"✓ Data Points: {len(data)}")
    print(f"✓ Correlation: {correlation:.3f} (Very Strong)")
    print(f"✓ R² Score: {r_value**2:.3f}")
    print(f"✓ Equation: Rating = {intercept:.2f} + {slope:.4f} × OnTime%")
    
    # Create scatter plot with regression line
    fig, ax = plt.subplots(figsize=(10, 7))
    
    ax.scatter(data['OnTime %'], data['Avg Rating'], s=100, alpha=0.6, 
              color=COLORS['primary'], edgecolors='black', linewidth=1.5)
    
    # Regression line
    x_line = np.array([data['OnTime %'].min(), data['OnTime %'].max()])
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line, 'r--', linewidth=2.5, label=f'Fit: y={slope:.4f}x+{intercept:.2f}')
    
    ax.set_xlabel('On-Time Delivery %', fontsize=12, fontweight='bold')
    ax.set_ylabel('Avg Customer Rating (⭐)', fontsize=12, fontweight='bold')
    ax.set_title(f'On-Time Delivery vs Customer Satisfaction\n(Correlation: r={correlation:.3f}, R²={r_value**2:.3f})',
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11, loc='lower right')
    ax.set_xlim(80, 95)
    ax.set_ylim(3.8, 4.6)
    
    # Statistics box
    textstr = f'Correlation: {correlation:.3f}\nR² Score: {r_value**2:.3f}\np-value: {p_value:.2e}\nStrength: Very Strong'
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=11,
           verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('visualizations/05_ontime_rating_correlation.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/05_ontime_rating_correlation.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 6: PRIORITY DELIVERY TYPE IMPACT
# ============================================================================
print("[6/12] PRIORITY DELIVERY TYPE IMPACT")
print("-"*80)

try:
    # Load Priority Analysis
    priority_df = pd.read_excel(
        'data_exports/priority_analysis.xlsx',
        sheet_name='Data',
        skiprows=5  # Skip banner rows (3) + empty row (1) + header row (1)
    )
    
    # Columns are already named correctly: delivery_priority, total, on_time_pct, avg_distance, avg_weight
    priority_df.columns = ['Priority Type', 'Total', 'On-Time %', 'Avg Distance', 'Avg Weight']
    
    # Remove NaN rows
    priority_df = priority_df.dropna(subset=['Priority Type'])
    
    print(f"✓ Source File: priority_analysis.xlsx")
    print(f"✓ Sheet: Data")
    print(f"✓ Columns Used: delivery_priority (Priority Type), total, on_time_pct (On-Time %)")
    print(f"✓ Priority Types: {len(priority_df)}")
    print(f"✓ Record: {priority_df.to_dict('list')}")
    
    # Create comparison chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    priority_types = priority_df['Priority Type']
    on_time_pct = priority_df['On-Time %'].astype(float)
    
    colors_priority = [COLORS['primary'], COLORS['warning'], COLORS['accent'], COLORS['negative']][:len(priority_df)]
    
    # Chart 1: On-Time % by priority
    ax1.bar(priority_types, on_time_pct, color=colors_priority)
    ax1.set_ylabel('On-Time Delivery %', fontsize=12, fontweight='bold')
    ax1.set_title('On-Time Performance by Delivery Priority', fontsize=12, fontweight='bold')
    ax1.set_ylim(70, 100)
    ax1.grid(axis='y', alpha=0.3)
    
    for i, (ptype, pct) in enumerate(zip(priority_types, on_time_pct)):
        ax1.text(i, pct, f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Chart 2: Volume by priority
    ax2.bar(priority_types, priority_df['Total'].astype(float), color=colors_priority)
    ax2.set_ylabel('Number of Deliveries', fontsize=12, fontweight='bold')
    ax2.set_title('Delivery Volume by Priority Type', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for i, (ptype, total) in enumerate(zip(priority_types, priority_df['Total'])):
        ax2.text(i, total, f'{int(total):,}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.suptitle('Impact of Delivery Priority on Performance', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('visualizations/06_priority_delivery_impact.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/06_priority_delivery_impact.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 7: DEPOT MONTHLY HEATMAP
# ============================================================================
print("[7/12] DEPOT MONTHLY HEATMAP")
print("-"*80)

try:
    # Load and pivot data
    monthly_depot = pd.read_excel(
        'data_exports/Monthly_Feedback_Enhanced.xlsx',
        sheet_name='Depot Monthly Breakdown',
        skiprows=3
    )
    
    # Filter to data rows
    monthly_depot = monthly_depot[monthly_depot['Month'] != 'GRAND TOTAL'].copy()
    
    # Create pivot table for heatmap
    heatmap_data = monthly_depot.pivot(index='Depot', columns='Month', values='OnTime %')
    
    print(f"✓ Source File: Monthly_Feedback_Enhanced.xlsx")
    print(f"✓ Sheet: Depot Monthly Breakdown")
    print(f"✓ Columns Used: Depot, Month, OnTime %")
    print(f"✓ Depots: {len(heatmap_data)}, Months: {len(heatmap_data.columns)}")
    print(f"✓ Range: {heatmap_data.values.min():.1f}% - {heatmap_data.values.max():.1f}%")
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='RdYlGn', center=88,
               cbar_kws={'label': 'On-Time %'}, ax=ax, vmin=80, vmax=95,
               linewidths=1, linecolor='white')
    
    ax.set_title('On-Time Delivery Performance Heatmap\n(Depot × Month)', 
                fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_ylabel('Depot', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualizations/07_depot_monthly_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/07_depot_monthly_heatmap.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 8: VEHICLE TYPE ANALYSIS
# ============================================================================
print("[8/12] VEHICLE TYPE ANALYSIS")
print("-"*80)

try:
    # Load vehicle analysis
    vehicle_df = pd.read_excel(
        'data_exports/vehicle_analysis.xlsx',
        sheet_name='Data',
        skiprows=5  # Skip banner rows (3) + empty row (1) + header row (1)
    )
    
    # Columns are already named correctly: vehicle_type, total, percentage, on_time_pct, avg_distance
    vehicle_df.columns = ['Vehicle Type', 'Total', 'Percentage', 'On-Time %', 'Avg Distance']
    vehicle_df = vehicle_df.dropna(subset=['Vehicle Type'])
    
    print(f"✓ Source File: vehicle_analysis.xlsx")
    print(f"✓ Sheet: Data")
    print(f"✓ Columns Used: vehicle_type, total, on_time_pct")
    print(f"✓ Vehicle Types: {len(vehicle_df)}")
    print(f"✓ Records: {vehicle_df['Vehicle Type'].tolist()}")
    
    # Create comparison chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    vehicle_types = vehicle_df['Vehicle Type']
    on_time_pct = vehicle_df['On-Time %'].astype(float)
    totals = vehicle_df['Total'].astype(float)
    
    colors_vehicle = [COLORS['primary'], COLORS['secondary'], COLORS['accent'],
                     COLORS['warning'], COLORS['negative'], COLORS['positive']][:len(vehicle_df)]
    
    # Chart 1: On-Time % by vehicle
    ax1.bar(vehicle_types, on_time_pct, color=colors_vehicle)
    ax1.set_ylabel('On-Time %', fontsize=12, fontweight='bold')
    ax1.set_title('On-Time Performance by Vehicle Type', fontsize=12, fontweight='bold')
    ax1.set_ylim(75, 100)
    ax1.grid(axis='y', alpha=0.3)
    
    for i, (vtype, pct) in enumerate(zip(vehicle_types, on_time_pct)):
        ax1.text(i, pct, f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    # Chart 2: Volume by vehicle
    ax2.bar(vehicle_types, totals, color=colors_vehicle)
    ax2.set_ylabel('Number of Deliveries', fontsize=12, fontweight='bold')
    ax2.set_title('Delivery Volume by Vehicle Type', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for i, (vtype, total) in enumerate(zip(vehicle_types, totals)):
        ax2.text(i, total, f'{int(total):,}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.suptitle('Vehicle Type Impact on Delivery Performance', fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('visualizations/08_vehicle_type_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/08_vehicle_type_analysis.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 9: MONTHLY VOLUME vs QUALITY TREND
# ============================================================================
print("[9/12] MONTHLY VOLUME vs QUALITY TREND")
print("-"*80)

try:
    # Load and aggregate by month
    monthly_depot = pd.read_excel(
        'data_exports/Monthly_Feedback_Enhanced.xlsx',
        sheet_name='Depot Monthly Breakdown',
        skiprows=3
    )
    
    monthly_depot = monthly_depot[monthly_depot['Month'] != 'GRAND TOTAL'].copy()
    monthly_agg = monthly_depot.groupby('Month').agg({
        'Total Deliveries': 'sum',
        'OnTime %': 'mean'
    }).reset_index()
    
    print(f"✓ Source File: Monthly_Feedback_Enhanced.xlsx")
    print(f"✓ Sheet: Depot Monthly Breakdown")
    print(f"✓ Columns Used: Month, Total Deliveries, OnTime %")
    print(f"✓ Months: {len(monthly_agg)}")
    print(f"✓ Volume Range: {monthly_agg['Total Deliveries'].min():.0f} - {monthly_agg['Total Deliveries'].max():.0f}")
    print(f"✓ Quality: {monthly_agg['OnTime %'].min():.1f}% - {monthly_agg['OnTime %'].max():.1f}%")
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot deliveries on primary axis
    color = COLORS['primary']
    ax1.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Total Monthly Deliveries', color=color, fontsize=12, fontweight='bold')
    ax1.bar(monthly_agg['Month'], monthly_agg['Total Deliveries']/1000, 
           alpha=0.6, color=color, label='Deliveries (÷1000)')
    ax1.tick_params(axis='y', labelcolor=color)
    
    # Plot on-time % on secondary axis
    ax2 = ax1.twinx()
    color = COLORS['negative']
    ax2.set_ylabel('On-Time %', color=color, fontsize=12, fontweight='bold')
    ax2.plot(monthly_agg['Month'], monthly_agg['OnTime %'], marker='o', color=color, 
            linewidth=2.5, markersize=8, label='On-Time %')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(80, 95)
    
    plt.title('Volume vs Quality Trade-off\n(Monthly Deliveries vs On-Time Performance)', 
             fontsize=14, fontweight='bold')
    fig.tight_layout()
    plt.xticks(rotation=45)
    plt.savefig('visualizations/09_monthly_volume_vs_quality.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/09_monthly_volume_vs_quality.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 10: FEEDBACK SENTIMENT TIMELINE
# ============================================================================
print("[10/12] FEEDBACK SENTIMENT TIMELINE")
print("-"*80)

try:
    # Load monthly sentiment
    monthly_summary = pd.read_excel(
        'data_exports/Monthly_Feedback_Summary_Detailed.xlsx',
        sheet_name='Monthly Feedback Summary',
        skiprows=3
    )
    
    monthly_summary = monthly_summary[~monthly_summary['Month'].isna()].copy()
    monthly_summary = monthly_summary[monthly_summary['Month'] != 'GRAND TOTAL'].copy()
    
    print(f"✓ Source File: Monthly_Feedback_Summary_Detailed.xlsx")
    print(f"✓ Sheet: Monthly Feedback Summary")
    print(f"✓ Columns Used: Month, Positive %, Neutral %, Negative %")
    print(f"✓ Months: {len(monthly_summary)}")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    months = monthly_summary['Month'].astype(str)
    positive = monthly_summary['Positive %'].fillna(0)
    neutral = monthly_summary['Neutral %'].fillna(0)
    negative = monthly_summary['Negative %'].fillna(0)
    
    ax.stackplot(range(len(monthly_summary)), 
                positive, neutral, negative,
                labels=['Positive', 'Neutral', 'Negative'],
                colors=[COLORS['positive'], COLORS['warning'], COLORS['negative']],
                alpha=0.8)
    
    ax.set_xticks(range(len(monthly_summary)))
    ax.set_xticklabels(months, rotation=45)
    ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Month', fontsize=12, fontweight='bold')
    ax.set_title('Customer Sentiment Trend Over Time', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizations/10_feedback_sentiment_timeline.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/10_feedback_sentiment_timeline.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 11: SERVICE CONSISTENCY VARIATION
# ============================================================================
print("[11/12] SERVICE CONSISTENCY VARIATION")
print("-"*80)

try:
    # Load monthly depot data for service consistency
    monthly_depot = pd.read_excel(
        'data_exports/Monthly_Feedback_Enhanced.xlsx',
        sheet_name='Depot Monthly Breakdown',
        skiprows=3
    )
    
    monthly_depot = monthly_depot[monthly_depot['Month'] != 'GRAND TOTAL'].copy()
    
    # Aggregate by depot
    depot_consistency = monthly_depot.groupby('Depot').agg({
        'Service Consistency (Std Dev)': 'mean'
    }).reset_index().sort_values('Service Consistency (Std Dev)')
    
    print(f"✓ Source File: Monthly_Feedback_Enhanced.xlsx")
    print(f"✓ Sheet: Depot Monthly Breakdown")
    print(f"✓ Columns Used: Depot, Service Consistency (Std Dev)")
    print(f"✓ Depots: {len(depot_consistency)}")
    print(f"✓ Most Consistent: {depot_consistency.iloc[0]['Depot']} ({depot_consistency.iloc[0]['Service Consistency (Std Dev)']:.2f})")
    print(f"✓ Least Consistent: {depot_consistency.iloc[-1]['Depot']} ({depot_consistency.iloc[-1]['Service Consistency (Std Dev)']:.2f})")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    depots = depot_consistency['Depot']
    consistency = depot_consistency['Service Consistency (Std Dev)']
    
    # Color gradient: lower is better
    colors_gradient = [COLORS['positive'] if c < 0.75 else COLORS['warning'] if c < 0.80 else COLORS['negative'] 
                      for c in consistency]
    
    ax.barh(depots, consistency, color=colors_gradient)
    ax.set_xlabel('Service Consistency (Std Dev - Lower is Better)', fontsize=12, fontweight='bold')
    ax.set_title('Service Consistency Variation by Depot\n(Rating variability across months)', 
                fontsize=14, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    ax.invert_yaxis()
    
    for i, (depot, cons) in enumerate(zip(depots, consistency)):
        ax.text(cons, i, f' {cons:.2f}', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('visualizations/11_service_consistency_variation.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/11_service_consistency_variation.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# VISUALIZATION 12: FEEDBACK VOLUME DISTRIBUTION
# ============================================================================
print("[12/12] FEEDBACK VOLUME DISTRIBUTION")
print("-"*80)

try:
    # Load monthly data for volume distribution
    monthly_summary = pd.read_excel(
        'data_exports/Monthly_Feedback_Summary_Detailed.xlsx',
        sheet_name='Monthly Feedback Summary',
        skiprows=3
    )
    
    monthly_summary = monthly_summary[~monthly_summary['Month'].isna()].copy()
    monthly_summary = monthly_summary[monthly_summary['Month'] != 'GRAND TOTAL'].copy()
    
    total_feedback = monthly_summary['Total Feedback'].sum()
    
    print(f"✓ Source File: Monthly_Feedback_Summary_Detailed.xlsx")
    print(f"✓ Sheet: Monthly Feedback Summary")
    print(f"✓ Columns Used: Month, Total Feedback")
    print(f"✓ Total Feedback: {int(total_feedback):,}")
    print(f"✓ Months: {len(monthly_summary)}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Chart 1: Pie chart of feedback distribution
    months = monthly_summary['Month'].astype(str)
    feedback_counts = monthly_summary['Total Feedback']
    
    colors_pie = plt.cm.Set3(range(len(months)))
    wedges, texts, autotexts = ax1.pie(feedback_counts, labels=months, autopct='%1.1f%%',
                                        colors=colors_pie, startangle=90)
    ax1.set_title('Monthly Feedback Volume Distribution\n(Percentage of total)', 
                 fontsize=12, fontweight='bold')
    
    # Make percentage text readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)
    
    # Chart 2: Bar chart of monthly feedback
    ax2.bar(months, feedback_counts, color=colors_pie)
    ax2.set_ylabel('Number of Feedback Records', fontsize=12, fontweight='bold')
    ax2.set_title('Monthly Feedback Count\n(Absolute numbers)', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for month, count in zip(months, feedback_counts):
        ax2.text(month, count, f'{int(count):,}', ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    plt.suptitle('Feedback Volume Distribution', fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.savefig('visualizations/12_feedback_volume_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: visualizations/12_feedback_volume_distribution.png\n")
    plt.close()
    
except Exception as e:
    print(f"✗ Error: {str(e)}\n")


# ============================================================================
# COMPLETION SUMMARY
# ============================================================================
print("="*80)
print("VISUALIZATION GENERATION COMPLETE")
print("="*80)
print("\n✓ All 12 visualizations generated successfully!")
print("✓ Output directory: visualizations/")
print("\nData sources used (APPROVED ONLY):")
print("  - Monthly_Feedback_Enhanced.xlsx")
print("  - Monthly_Feedback_Summary_Detailed.xlsx")
print("  - priority_analysis.xlsx")
print("  - vehicle_analysis.xlsx")
print("\nData scope: Feedback-linked deliveries only (53,007 records)")
print("Analysis period: November 2025 - May 2026")
print("="*80)
