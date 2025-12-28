import csv
import statistics
from collections import defaultdict

file_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\ca31a900-d51f-11f0-8600-af36ab325207.csv'

def analyze_csv(path):
    print(f"Analyzing {path}...")
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        data = list(reader)
        
    row_count = len(data)
    print(f"Total Rows: {row_count}")
    print(f"Total Columns: {len(headers)}")
    print("-" * 30)
    
    # Column analysis
    for i, col_name in enumerate(headers):
        values = [row[i] for row in data if i < len(row)]
        
        # Missing values (empty strings or 'NULL')
        missing_count = sum(1 for v in values if v == '' or v.upper() == 'NULL')
        
        # Try to convert to float to check if numeric
        numeric_values = []
        for v in values:
            if v and v.upper() != 'NULL':
                try:
                    numeric_values.append(float(v))
                except ValueError:
                    pass
        
        is_numeric = len(numeric_values) > 0 and len(numeric_values) > (len(values) - missing_count) * 0.9
        
        print(f"Column: {col_name}")
        print(f"  Missing: {missing_count} ({missing_count/row_count*100:.1f}%)")
        
        if is_numeric:
            print(f"  Type: Numeric")
            if numeric_values:
                print(f"  Min: {min(numeric_values)}")
                print(f"  Max: {max(numeric_values)}")
                print(f"  Mean: {statistics.mean(numeric_values):.2f}")
        else:
            unique_vals = set(values)
            print(f"  Type: Categorical")
            print(f"  Unique Values: {len(unique_vals)}")
            if len(unique_vals) < 10:
                print(f"  Values: {list(unique_vals)}")
        print("-" * 20)

if __name__ == "__main__":
    try:
        analyze_csv(file_path)
    except Exception as e:
        print(f"Error: {e}")
