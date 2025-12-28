"""
Verify cluster sizes from actual data files
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Try to load the most recent clustered data
data_dir = Path(r"c:\Users\moham\Desktop\New folder\profiling\data_science_profiling")

print("="*80)
print("CLUSTER SIZE VERIFICATION")
print("="*80)

# Try different versions of clustered data
files_to_try = [
    'clustered_data_enhanced.csv',
    'clustered_data_behavioral_deep.csv',
    'clustered_data_optimized.csv',
    'clustered_data.csv'
]

results = {}

for filename in files_to_try:
    filepath = data_dir / filename
    if filepath.exists():
        try:
            print(f"\n{'='*80}")
            print(f"READING: {filename}")
            print('='*80)
            
            df = pd.read_csv(filepath)
            
            # Check if Cluster column exists
            if 'Cluster' in df.columns:
                total = len(df)
                cluster_counts = df['Cluster'].value_counts().sort_index()
                
                print(f"\n📊 Total households: {total:,}")
                print(f"\n📌 Cluster Distribution:")
                
                for cluster_id in sorted(cluster_counts.index):
                    count = cluster_counts[cluster_id]
                    percentage = (count / total) * 100
                    print(f"   Cluster {cluster_id}: n={count:,} ({percentage:.1f}%)")
                
                # Verification
                sum_check = cluster_counts.sum() == total
                print(f"\n✓ Verification: {cluster_counts.sum():,} == {total:,}? {sum_check}")
                
                # Store results
                results[filename] = {
                    'total': total,
                    'clusters': cluster_counts.to_dict(),
                    'percentages': {k: (v/total)*100 for k, v in cluster_counts.items()}
                }
                
                # Check for cluster labels column
                label_cols = [col for col in df.columns if 'label' in col.lower() or 'profile' in col.lower()]
                if label_cols:
                    print(f"\n🏷️  Found label columns: {label_cols}")
                    for col in label_cols[:2]:  # Show first 2
                        print(f"\n   {col}:")
                        print(df.groupby('Cluster')[col].first())
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print(f"\n   ⚠️  {filename} not found")

# Summary comparison
if results:
    print("\n" + "="*80)
    print("SUMMARY COMPARISON")
    print("="*80)
    
    for filename, data in results.items():
        print(f"\n{filename}:")
        print(f"  Total: {data['total']:,}")
        for cluster_id in sorted(data['clusters'].keys()):
            count = data['clusters'][cluster_id]
            pct = data['percentages'][cluster_id]
            print(f"  C{cluster_id}: {count:,} ({pct:.1f}%)")

# Check against review report claims
print("\n" + "="*80)
print("COMPARISON TO REVIEW REPORT")
print("="*80)

print("\n📄 Abstract claims:")
print("   - Low-Intensity Conservers: 41%")
print("   - Moderate Standard Users: 34%")
print("   - High-Intensity Profligate: 25%")

print("\n📄 Section 3.3 claims:")
print("   - Cluster 0 (Moderate): 62.8% (n=8,198)")
print("   - Cluster 1 (Profligate): 11.8% (n=1,545)")
print("   - Cluster 2 (Conservers): 25.4% (n=3,318)")
print("   - Total: 13,061")

if results:
    # Get the most likely correct file (enhanced version)
    latest_file = 'clustered_data_enhanced.csv' if 'clustered_data_enhanced.csv' in results else list(results.keys())[0]
    actual_data = results[latest_file]
    
    print(f"\n✅ ACTUAL DATA (from {latest_file}):")
    for cluster_id in sorted(actual_data['clusters'].keys()):
        count = actual_data['clusters'][cluster_id]
        pct = actual_data['percentages'][cluster_id]
        print(f"   Cluster {cluster_id}: {pct:.1f}% (n={count:,})")
    
    # Check which claim matches
    print("\n🔍 INCONSISTENCY CHECK:")
    total_actual = actual_data['total']
    section_total = 8198 + 1545 + 3318
    print(f"   Section 3.3 claimed total (8198+1545+3318) = {section_total}")
    print(f"   Actual total from data = {total_actual:,}")
    print(f"   Match? {section_total == total_actual}")

print("\n" + "="*80)
print("DONE")
print("="*80)
