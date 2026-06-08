import pandas as pd

# Check what sheets exist in Monthly_Feedback_Summary_Detailed.xlsx
excel_file = 'data_exports/Monthly_Feedback_Summary_Detailed.xlsx'

try:
    xl_file = pd.ExcelFile(excel_file)
    print("Sheet names in Monthly_Feedback_Summary_Detailed.xlsx:")
    for sheet in xl_file.sheet_names:
        print(f"  - {sheet}")
        df = pd.read_excel(excel_file, sheet_name=sheet)
        print(f"    Rows: {len(df)}, Columns: {list(df.columns)}\n")
except Exception as e:
    print(f"Error: {e}")
