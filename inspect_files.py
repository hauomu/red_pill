import pandas as pd
import os

data_dir = 'data_exports'
files_to_check = [
    'Monthly_Feedback_Enhanced.xlsx',
    'Monthly_Feedback_Summary_Detailed.xlsx',
    'deliveries_feedback_merged.csv',
    'priority_analysis.xlsx',
    'vehicle_analysis.xlsx'
]

for file in files_to_check:
    filepath = os.path.join(data_dir, file)
    if not os.path.exists(filepath):
        print(f'{file}: NOT FOUND')
        continue
    
    print(f'\n{"="*80}')
    print(f'{file}')
    print("="*80)
    
    if file.endswith('.xlsx'):
        xl = pd.ExcelFile(filepath)
        print(f'Sheets: {xl.sheet_names}')
        for sheet in xl.sheet_names:
            # Skip first 3 rows (banners)
            df = pd.read_excel(filepath, sheet_name=sheet, skiprows=3, nrows=10)
            print(f'\n[{sheet}] Shape: {df.shape}')
            print(f'Columns: {list(df.columns)}')
            if df.shape[0] > 0:
                print(f'Sample:\n{df.head(3).to_string()}')
    elif file.endswith('.csv'):
        try:
            # Skip comment lines, try different encodings
            df = pd.read_csv(filepath, skiprows=8, encoding='latin-1', nrows=5)
            print(f'Shape: {df.shape}')
            print(f'Columns: {list(df.columns)}')
            if df.shape[0] > 0:
                print(f'Sample:\n{df.head(3).to_string()}')
        except Exception as e:
            print(f'Error reading {file}: {str(e)[:100]}')
