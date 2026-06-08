import pandas as pd

df = pd.read_csv('data_exports/deliveries_feedback_merged.csv', encoding='latin-1', nrows=5)
print("Sample data:\n")
print(df[['booking_datetime', 'promised_delivery_datetime', 'delivery_datetime']].head(10))
print("\n\nData types:")
print(df.dtypes)
