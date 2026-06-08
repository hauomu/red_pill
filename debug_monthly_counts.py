"""
Debug monthly feedback count discrepancy
"""
import pandas as pd

print("\n" + "=" * 100)
print("DEBUG: Monthly Feedback Count Discrepancy")
print("=" * 100)

# Load source data
feedback = pd.read_csv('Db-Browser/feedback.csv', encoding='latin-1')
print(f"\n1. Source feedback data:")
print(f"   Total rows: {len(feedback)}")
print(f"   Columns: {list(feedback.columns)}")

# Check date column
print(f"\n2. feedback_datetime sample values:")
print(feedback['feedback_datetime'].head(10).tolist())

# Parse dates
feedback['feedback_dt'] = pd.to_datetime(feedback['feedback_datetime'], format='%d/%m/%Y %H:%M', errors='coerce')
feedback['month'] = feedback['feedback_dt'].dt.to_period('M').astype(str)

print(f"\n3. After parsing:")
print(f"   Valid dates: {feedback['feedback_dt'].notna().sum()}")
print(f"   Invalid dates (NaT): {feedback['feedback_dt'].isna().sum()}")

# Group by month
monthly_counts = feedback.groupby('month').size().reset_index(name='count')
monthly_counts = monthly_counts.sort_values('month')

print(f"\n4. Monthly feedback counts from source:")
print(monthly_counts.to_string(index=False))

# Load file and check month format
enhanced = pd.read_excel('data_exports/Monthly_Feedback_Enhanced.xlsx', sheet_name='Depot Monthly Breakdown')
months_in_file = enhanced['Month'].unique()
print(f"\n5. Month values in Monthly_Feedback_Enhanced.xlsx:")
print(f"   {sorted([m for m in months_in_file if pd.notna(m)])}")

monthly_summary = pd.read_excel('data_exports/Monthly_Feedback_Summary_Detailed.xlsx', sheet_name='Monthly Feedback Summary')
print(f"\n6. Month values in Monthly_Feedback_Summary_Detailed.xlsx:")
print(f"   {monthly_summary['Month'].tolist()}")
print(f"\n   Total Feedback values:")
print(f"   {monthly_summary['Total Feedback'].tolist()}")

print("\n" + "=" * 100)
print("FINDINGS:")
print("=" * 100)
print(f"Source data has {len(monthly_counts)} months")
print(f"File expects {len(monthly_summary)} months")
print(f"\nFile months: {monthly_summary['Month'].tolist()}")
print(f"Source months: {monthly_counts['month'].tolist()}")
print(f"\nIssue: Month format mismatch - source uses period format, file uses different format")
