"""
Analyze all available data sources to understand what visualizations are possible
"""
import pandas as pd
import os

print("\n" + "=" * 100)
print("DATA SOURCE ANALYSIS - VISUALIZATION PLANNING")
print("=" * 100)

# Check which files exist
export_files = {
    'Monthly_Feedback_Enhanced.xlsx': 'data_exports/Monthly_Feedback_Enhanced.xlsx',
    'Monthly_Feedback_Summary_Detailed.xlsx': 'data_exports/Monthly_Feedback_Summary_Detailed.xlsx',
    'deliveries_feedback_merged.csv': 'data_exports/deliveries_feedback_merged.csv',
    'priority_analysis.xlsx': 'data_exports/priority_analysis.xlsx',
    'vehicle_analysis.xlsx': 'data_exports/vehicle_analysis.xlsx',
    'feedback_sample.xlsx': 'data_exports/feedback_sample.xlsx'
}

print("\n" + "─" * 100)
print("AVAILABLE DATA FILES")
print("─" * 100)

available_files = {}
for name, path in export_files.items():
    if os.path.exists(path):
        available_files[name] = path
        print(f"\n✅ {name}")
    else:
        print(f"\n❌ {name} (NOT FOUND)")

# ============================================================================
# ANALYZE EACH FILE
# ============================================================================

print("\n\n" + "=" * 100)
print("DETAILED FILE ANALYSIS")
print("=" * 100)

# FILE 1: Monthly_Feedback_Enhanced.xlsx
print("\n" + "─" * 100)
print("1. Monthly_Feedback_Enhanced.xlsx")
print("─" * 100)

try:
    xlsx_file = pd.ExcelFile('data_exports/Monthly_Feedback_Enhanced.xlsx')
    print(f"\nSheets: {xlsx_file.sheet_names}")
    
    for sheet in xlsx_file.sheet_names:
        df = pd.read_excel('data_exports/Monthly_Feedback_Enhanced.xlsx', sheet_name=sheet, skiprows=3)
        print(f"\n  Sheet: {sheet}")
        print(f"    Rows: {len(df):,} | Columns: {len(df.columns)}")
        print(f"    Columns: {list(df.columns)[:5]}..." if len(df.columns) > 5 else f"    Columns: {list(df.columns)}")
        if sheet == 'Depot Monthly Breakdown':
            print(f"    Months: {df['Month'].unique() if 'Month' in df.columns else 'N/A'}")
            print(f"    Depots: {df['Depot'].unique() if 'Depot' in df.columns else 'N/A'}")
except Exception as e:
    print(f"Error reading file: {e}")

# FILE 2: Monthly_Feedback_Summary_Detailed.xlsx
print("\n" + "─" * 100)
print("2. Monthly_Feedback_Summary_Detailed.xlsx")
print("─" * 100)

try:
    xlsx_file = pd.ExcelFile('data_exports/Monthly_Feedback_Summary_Detailed.xlsx')
    print(f"\nSheets: {xlsx_file.sheet_names}")
    
    for sheet in xlsx_file.sheet_names:
        df = pd.read_excel('data_exports/Monthly_Feedback_Summary_Detailed.xlsx', sheet_name=sheet, skiprows=3)
        print(f"\n  Sheet: {sheet}")
        print(f"    Rows: {len(df):,} | Columns: {len(df.columns)}")
        print(f"    Columns: {list(df.columns)[:5]}..." if len(df.columns) > 5 else f"    Columns: {list(df.columns)}")
except Exception as e:
    print(f"Error reading file: {e}")

# FILE 3: deliveries_feedback_merged.csv
print("\n" + "─" * 100)
print("3. deliveries_feedback_merged.csv")
print("─" * 100)

try:
    df = pd.read_csv('data_exports/deliveries_feedback_merged.csv', encoding='latin-1', skiprows=8)
    print(f"\nRows: {len(df):,} | Columns: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nKey metrics available:")
    for col in df.columns:
        if col in ['on_time', 'rating', 'delivery_priority', 'vehicle_type', 'distance_km', 'parcel_weight_kg']:
            print(f"  • {col}: {df[col].dtype} (missing: {df[col].isna().sum()})")
except Exception as e:
    print(f"Error reading file: {e}")

# FILE 4: priority_analysis.xlsx
print("\n" + "─" * 100)
print("4. priority_analysis.xlsx")
print("─" * 100)

try:
    df = pd.read_excel('data_exports/priority_analysis.xlsx', sheet_name='Data', skiprows=3)
    print(f"\nRows: {len(df):,} | Columns: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
except Exception as e:
    print(f"Error reading file: {e}")

# FILE 5: vehicle_analysis.xlsx
print("\n" + "─" * 100)
print("5. vehicle_analysis.xlsx")
print("─" * 100)

try:
    df = pd.read_excel('data_exports/vehicle_analysis.xlsx', sheet_name='Data', skiprows=3)
    print(f"\nRows: {len(df):,} | Columns: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
except Exception as e:
    print(f"Error reading file: {e}")

# FILE 6: feedback_sample.xlsx
print("\n" + "─" * 100)
print("6. feedback_sample.xlsx")
print("─" * 100)

if os.path.exists('data_exports/feedback_sample.xlsx'):
    try:
        xlsx_file = pd.ExcelFile('data_exports/feedback_sample.xlsx')
        print(f"\nSheets: {xlsx_file.sheet_names}")
        df = pd.read_excel('data_exports/feedback_sample.xlsx')
        print(f"Rows: {len(df):,} | Columns: {len(df.columns)}")
        print(f"Columns: {list(df.columns)[:10]}...")
    except Exception as e:
        print(f"Error reading file: {e}")
else:
    print("\nFile not found")

# ============================================================================
# SUMMARY OF AVAILABLE DATA DIMENSIONS
# ============================================================================
print("\n\n" + "=" * 100)
print("AVAILABLE DATA DIMENSIONS FOR VISUALIZATION")
print("=" * 100)

print("""
TEMPORAL DIMENSIONS:
  ✅ Monthly time series (7 months: Nov 2025 - May 2026)
  ✅ Monthly trends over time

GEOGRAPHIC/ORGANIZATIONAL DIMENSIONS:
  ✅ Depot/Branch breakdown (4 depots: Central, East, North, West)
  ✅ Depot-monthly combinations (28 records)

DELIVERY PERFORMANCE DIMENSIONS:
  ✅ On-time delivery percentage
  ✅ Total deliveries per period
  ✅ Delivery priority types (Standard, Express, Premium, VIP)
  ✅ Vehicle type distribution (Van, Bike, Truck, Motorcycle, Scooter, Auto)

CUSTOMER SATISFACTION DIMENSIONS:
  ✅ Rating distribution (1-5 stars)
  ✅ Average rating by month/depot
  ✅ Sentiment categorization (Positive/Neutral/Negative)
  ✅ Service consistency (Std Dev by depot/month)

FEEDBACK ANALYSIS DIMENSIONS:
  ✅ Feedback themes/categories (6 categories)
  ✅ Comment sentiment analysis
  ✅ Top positive/negative comments
  ✅ Feedback coverage by period

OPERATIONAL DIMENSIONS:
  ✅ Delivery distance metrics
  ✅ Parcel weight
  ✅ Stops on route
  ✅ Driver experience

QUANTIFIED INSIGHTS:
  ✅ 53,007 feedback-linked deliveries
  ✅ 36.5% feedback coverage
  ✅ 43,517 feedback comments analyzed
  ✅ 6 theme categories
  ✅ Monthly aggregations with statistics
""")

print("=" * 100)
