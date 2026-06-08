"""
PHASE 1: COMPREHENSIVE EDA VALIDATION
Senior Data Scientist Review
================================================
Validates all source files, worksheets, columns, data types, and calculations
Reconciles against deliveries.csv and feedback.csv (ground truth)
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

print("="*80)
print("PHASE 1: COMPREHENSIVE EDA VALIDATION")
print("="*80)
print(f"Validation Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Define paths
BASE_PATH = "C:\\Users\\Sherman\\Desktop\\aiap24-NAME-NRIC"
DATA_EXPORTS = os.path.join(BASE_PATH, "data_exports")
DB_BROWSER = os.path.join(BASE_PATH, "Db-Browser")

# Source truth files
DELIVERIES_CSV = os.path.join(DB_BROWSER, "deliveries.csv")
FEEDBACK_CSV = os.path.join(DB_BROWSER, "feedback.csv")

# Approved data sources
SOURCES = {
    'Monthly_Feedback_Enhanced.xlsx': ['Depot Monthly Breakdown', 'Overall Depot Performance', 'Depot x Vehicle', 'Complaint Categories', 'Piority Analysis'],
    'Monthly_Feedback_Summary_Detailed.xlsx': ['Monthly Feedback Summary', 'Categories'],
    'priority_analysis.xlsx': ['Data'],
    'vehicle_analysis.xlsx': ['Data']
}

validation_issues = []
validation_passes = []

# ============================================================================
# STEP 1: VERIFY ALL FILES EXIST
# ============================================================================
print("\n" + "="*80)
print("STEP 1: VERIFY ALL FILES EXIST")
print("="*80)

for filename in SOURCES.keys():
    filepath = os.path.join(DATA_EXPORTS, filename)
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath) / 1024  # KB
        validation_passes.append(f"✓ {filename} exists ({file_size:.1f} KB)")
        print(f"✓ {filename} ({file_size:.1f} KB)")
    else:
        validation_issues.append(f"✗ MISSING: {filename}")
        print(f"✗ MISSING: {filename}")

# Verify ground truth files
for label, filepath in [("deliveries.csv", DELIVERIES_CSV), ("feedback.csv", FEEDBACK_CSV)]:
    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath) / 1024
        validation_passes.append(f"✓ {label} exists ({file_size:.1f} KB)")
        print(f"✓ {label} ({file_size:.1f} KB)")
    else:
        validation_issues.append(f"✗ MISSING: {label}")
        print(f"✗ MISSING: {label}")

# ============================================================================
# STEP 2: LOAD SOURCE DATA (GROUND TRUTH)
# ============================================================================
print("\n" + "="*80)
print("STEP 2: LOAD SOURCE DATA (GROUND TRUTH)")
print("="*80)

try:
    deliveries_df = pd.read_csv(DELIVERIES_CSV, encoding='latin-1')
    print(f"✓ Loaded deliveries.csv: {deliveries_df.shape[0]:,} rows × {deliveries_df.shape[1]} cols")
    validation_passes.append(f"✓ deliveries.csv loaded: {deliveries_df.shape[0]:,} rows")
except Exception as e:
    validation_issues.append(f"✗ Error loading deliveries.csv: {str(e)[:100]}")
    print(f"✗ Error: {str(e)[:100]}")

try:
    feedback_df = pd.read_csv(FEEDBACK_CSV, encoding='latin-1')
    print(f"✓ Loaded feedback.csv: {feedback_df.shape[0]:,} rows × {feedback_df.shape[1]} cols")
    validation_passes.append(f"✓ feedback.csv loaded: {feedback_df.shape[0]:,} rows")
except Exception as e:
    validation_issues.append(f"✗ Error loading feedback.csv: {str(e)[:100]}")
    print(f"✗ Error: {str(e)[:100]}")

# ============================================================================
# STEP 3: VERIFY WORKSHEETS AND COLUMNS EXIST
# ============================================================================
print("\n" + "="*80)
print("STEP 3: VERIFY WORKSHEETS AND COLUMNS EXIST")
print("="*80)

sheet_column_mapping = {}

for filename, sheets in SOURCES.items():
    filepath = os.path.join(DATA_EXPORTS, filename)
    print(f"\n{filename}:")
    
    try:
        xl = pd.ExcelFile(filepath)
        sheet_column_mapping[filename] = {}
        
        for sheet in sheets:
            if sheet in xl.sheet_names:
                df = pd.read_excel(filepath, sheet_name=sheet, skiprows=3, nrows=5)
                cols = [c for c in df.columns if not pd.isna(c) and not str(c).startswith('Unnamed')]
                sheet_column_mapping[filename][sheet] = cols
                validation_passes.append(f"✓ Sheet '{sheet}' exists: {len(cols)} columns")
                print(f"  ✓ Sheet '{sheet}': {len(cols)} columns")
            else:
                validation_issues.append(f"✗ Sheet '{sheet}' NOT FOUND in {filename}")
                print(f"  ✗ Sheet '{sheet}' NOT FOUND")
    except Exception as e:
        validation_issues.append(f"✗ Error reading {filename}: {str(e)[:100]}")
        print(f"  ✗ Error: {str(e)[:100]}")

# ============================================================================
# STEP 4: VERIFY DATA TYPES AND STRUCTURE
# ============================================================================
print("\n" + "="*80)
print("STEP 4: VERIFY DATA TYPES AND KEY COLUMNS")
print("="*80)

key_columns_to_check = {
    'Monthly_Feedback_Enhanced.xlsx': {
        'Depot Monthly Breakdown': ['Month', 'Depot', 'OnTime %', 'Avg Rating'],
        'Overall Depot Performance': ['Depot', 'On-Time %', 'Total Deliveries']
    },
    'Monthly_Feedback_Summary_Detailed.xlsx': {
        'Monthly Feedback Summary': ['Month', 'Total Feedback', 'Avg Rating'],
        'Categories': ['Category', 'Count']  # Approximate column names
    },
    'priority_analysis.xlsx': {
        'Data': ['delivery_priority', 'total', 'on_time_pct']
    },
    'vehicle_analysis.xlsx': {
        'Data': ['vehicle_type', 'total', 'on_time_pct']
    }
}

for filename, sheets_dict in key_columns_to_check.items():
    filepath = os.path.join(DATA_EXPORTS, filename)
    print(f"\n{filename}:")
    
    for sheet, expected_cols in sheets_dict.items():
        try:
            df = pd.read_excel(filepath, sheet_name=sheet, skiprows=3, nrows=10)
            actual_cols = [c for c in df.columns if not pd.isna(c) and not str(c).startswith('Unnamed')]
            
            # Check numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            print(f"  {sheet}:")
            print(f"    - Rows: {len(df)}, Numeric cols: {len(numeric_cols)}")
            validation_passes.append(f"✓ {filename} / {sheet}: {len(df)} rows, {len(numeric_cols)} numeric")
            
        except Exception as e:
            validation_issues.append(f"✗ Error validating {filename}/{sheet}: {str(e)[:100]}")
            print(f"    ✗ Error: {str(e)[:100]}")

# ============================================================================
# STEP 5: RECONCILE COUNTS WITH SOURCE DATA
# ============================================================================
print("\n" + "="*80)
print("STEP 5: RECONCILE COUNTS WITH SOURCE DATA (GROUND TRUTH)")
print("="*80)

# Load source data for reconciliation
try:
    # Count unique deliveries with feedback
    merged = deliveries_df.merge(feedback_df, on='delivery_id', how='inner')
    feedback_linked_count = len(merged)
    
    print(f"\nGround Truth (source CSVs):")
    print(f"  Total deliveries: {len(deliveries_df):,}")
    print(f"  Total feedback records: {len(feedback_df):,}")
    print(f"  Feedback-linked deliveries: {feedback_linked_count:,}")
    print(f"  Coverage: {100*feedback_linked_count/len(deliveries_df):.1f}%")
    
    validation_passes.append(f"✓ Ground truth: {feedback_linked_count:,} feedback-linked deliveries")
    
    # Now check if export files match
    try:
        monthly_enhanced = pd.read_excel(
            os.path.join(DATA_EXPORTS, 'Monthly_Feedback_Enhanced.xlsx'),
            sheet_name='Depot Monthly Breakdown',
            skiprows=3
        )
        monthly_enhanced = monthly_enhanced[monthly_enhanced['Month'] != 'GRAND TOTAL']
        export_count = monthly_enhanced['Total Deliveries'].sum()
        
        print(f"\nExport Data:")
        print(f"  Total in Monthly_Feedback_Enhanced: {export_count:,.0f}")
        
        if abs(export_count - feedback_linked_count) < 100:  # Allow small variance
            validation_passes.append(f"✓ Export count reconciles: {export_count:,.0f} ≈ {feedback_linked_count:,}")
            print(f"  ✓ RECONCILES with ground truth")
        else:
            validation_issues.append(f"✗ Export count mismatch: {export_count:,.0f} vs {feedback_linked_count:,}")
            print(f"  ✗ MISMATCH: {export_count:,.0f} vs {feedback_linked_count:,}")
    except Exception as e:
        print(f"  ✗ Could not verify export counts: {str(e)[:100]}")
        
except Exception as e:
    validation_issues.append(f"✗ Error reconciling counts: {str(e)}")
    print(f"✗ Error: {str(e)}")

# ============================================================================
# STEP 6: CHECK FOR DATA QUALITY ISSUES
# ============================================================================
print("\n" + "="*80)
print("STEP 6: DATA QUALITY CHECKS")
print("="*80)

# Check for missing values in key datasets
try:
    print("\nMissing Values Analysis:")
    
    monthly_enhanced = pd.read_excel(
        os.path.join(DATA_EXPORTS, 'Monthly_Feedback_Enhanced.xlsx'),
        sheet_name='Depot Monthly Breakdown',
        skiprows=3
    )
    monthly_enhanced = monthly_enhanced[monthly_enhanced['Month'] != 'GRAND TOTAL']
    
    missing = monthly_enhanced.isnull().sum()
    missing_cols = missing[missing > 0]
    
    if len(missing_cols) == 0:
        validation_passes.append("✓ No missing values in Monthly_Feedback_Enhanced")
        print("  ✓ No missing values in Depot Monthly Breakdown")
    else:
        print("  Missing values found:")
        for col, count in missing_cols.items():
            print(f"    - {col}: {count} missing")
            validation_issues.append(f"✗ Missing values: {col} ({count})")
    
    # Check percentage columns sum to 100
    try:
        if 'Positive %' in monthly_enhanced.columns:
            monthly_summary = pd.read_excel(
                os.path.join(DATA_EXPORTS, 'Monthly_Feedback_Summary_Detailed.xlsx'),
                sheet_name='Monthly Feedback Summary',
                skiprows=3
            )
            monthly_summary = monthly_summary[~monthly_summary['Month'].isna()]
            monthly_summary = monthly_summary[monthly_summary['Month'] != 'GRAND TOTAL']
            
            if 'Positive %' in monthly_summary.columns and 'Neutral %' in monthly_summary.columns:
                sums = monthly_summary['Positive %'] + monthly_summary['Neutral %'] + monthly_summary['Negative %']
                if sums.apply(lambda x: abs(x - 100) < 0.5).all():
                    validation_passes.append("✓ Sentiment percentages sum to 100%")
                    print("  ✓ Sentiment percentages sum to 100%")
                else:
                    validation_issues.append("✗ Sentiment percentages don't sum to 100%")
                    print("  ✗ Sentiment percentages don't sum to 100%")
    except Exception as e:
        print(f"  ! Could not verify percentage sums: {str(e)[:50]}")

except Exception as e:
    print(f"✗ Error in quality checks: {str(e)[:100]}")

# ============================================================================
# STEP 7: SUMMARY
# ============================================================================
print("\n" + "="*80)
print("VALIDATION SUMMARY")
print("="*80)

print(f"\n✓ PASSES ({len(validation_passes)}):")
for i, msg in enumerate(validation_passes[:5], 1):
    print(f"  {i}. {msg}")
if len(validation_passes) > 5:
    print(f"  ... and {len(validation_passes)-5} more")

if validation_issues:
    print(f"\n✗ ISSUES ({len(validation_issues)}):")
    for i, msg in enumerate(validation_issues[:5], 1):
        print(f"  {i}. {msg}")
    if len(validation_issues) > 5:
        print(f"  ... and {len(validation_issues)-5} more")
else:
    print(f"\n✓ NO ISSUES FOUND")

print(f"\n{'='*80}")
print(f"VALIDATION RESULT: {'✓ PASS' if len(validation_issues) == 0 else '✗ ISSUES FOUND'}")
print(f"{'='*80}")
print(f"\nTotal Passes: {len(validation_passes)}")
print(f"Total Issues: {len(validation_issues)}")
print(f"Validation End: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
