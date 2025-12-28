import pandas as pd
import os

file_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\ca31a900-d51f-11f0-8600-af36ab325207.csv'

try:
    df = pd.read_csv(file_path)
    print("### DataFrame Info ###")
    print(df.info())
    print("\n### DataFrame Description ###")
    print(df.describe())
    print("\n### Missing Values ###")
    print(df.isnull().sum())
    print("\n### Column Names ###")
    print(df.columns.tolist())
    
    # Check for duplicate rows
    duplicates = df.duplicated().sum()
    print(f"\n### Duplicate Rows: {duplicates} ###")

except Exception as e:
    print(f"Error analyzing file: {e}")
