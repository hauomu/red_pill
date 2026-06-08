import pandas as pd

categories_df = pd.read_excel('data_exports/Monthly_Feedback_Summary_Detailed.xlsx', sheet_name='Categories')
print("Categories sheet columns:")
print(list(categories_df.columns))
print("\nShape:", categories_df.shape)
print("\nFirst few rows:")
print(categories_df.head())
