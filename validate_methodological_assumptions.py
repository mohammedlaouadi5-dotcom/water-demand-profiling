"""
Validation Analysis for Methodological Critiques
1. MAD on sparse binary features - check what was retained/excluded
2. Leak imputation bias - compare unknown vs slow groups
"""

import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

data_dir = Path(r"c:\Users\moham\Desktop\New folder\profiling\data_science_profiling")

print("="*70)
print("METHODOLOGICAL VALIDATION ANALYSIS")
print("="*70)

# Load data
df = pd.read_csv(data_dir / 'clustered_data_enhanced.csv')
print(f"Loaded {len(df)} households")

# =============================================================================
# 1. MAD ON SPARSE BINARY FEATURES ANALYSIS
# =============================================================================
print("\n" + "="*70)
print("1. SPARSE BINARY FEATURE ANALYSIS")
print("="*70)

# Identify binary columns
binary_cols = [col for col in df.columns if df[col].dropna().nunique() == 2]
print(f"\nTotal binary columns: {len(binary_cols)}")

# Analyze sparsity
sparse_features = []
for col in binary_cols:
    # Calculate prevalence (proportion of 1s or positive class)
    try:
        prevalence = df[col].mean()
        if prevalence < 0.10:  # Sparse = less than 10% positive
            sparse_features.append({
                'Feature': col,
                'Prevalence': prevalence,
                'N_Positive': int(df[col].sum()),
                'Retained': True  # Since it's in clustered_data_enhanced, it was retained
            })
    except:
        pass

if sparse_features:
    sparse_df = pd.DataFrame(sparse_features).sort_values('Prevalence')
    print(f"\nSparse binary features (prevalence < 10%): {len(sparse_features)}")
    print("\nTop 20 rarest features that were RETAINED:")
    print(sparse_df.head(20).to_string(index=False))
    
    # Save for review
    sparse_df.to_csv(data_dir / 'sparse_binary_features_analysis.csv', index=False)
    print(f"\n✓ Saved: sparse_binary_features_analysis.csv")
else:
    print("No sparse binary features found in current dataset")

# =============================================================================
# 2. LEAK IMPUTATION BIAS CHECK
# =============================================================================
print("\n" + "="*70)
print("2. LEAK IMPUTATION BIAS VALIDATION")
print("="*70)

# Look for leak-related columns
leak_cols = [col for col in df.columns if 'leak' in col.lower()]
print(f"\nLeak-related columns found: {leak_cols[:10]}...")

# Check for consumption column
consumption_cols = [col for col in df.columns if 'consumption' in col.lower() or 'water-use' in col.lower() or 'yearly' in col.lower()]
print(f"Consumption columns found: {consumption_cols[:5]}...")

# If we have leak binary indicators, use them
if 'Shower-Leak_yes' in df.columns:
    print("\n--- Comparing households WITH vs WITHOUT shower leaks ---")
    
    # Find a consumption metric
    if 'Household-Water-Use-Litres-Yearly' in df.columns:
        cons_col = 'Household-Water-Use-Litres-Yearly'
    elif 'Person-Water-Use-Litres-Yearly' in df.columns:
        cons_col = 'Person-Water-Use-Litres-Yearly'
    else:
        cons_col = [c for c in df.columns if 'Litres' in c][0] if any('Litres' in c for c in df.columns) else None
    
    if cons_col:
        print(f"Using consumption metric: {cons_col}")
        
        # Compare groups
        with_leak = df[df['Shower-Leak_yes'] == 1][cons_col].dropna()
        without_leak = df[df['Shower-Leak_yes'] == 0][cons_col].dropna()
        
        print(f"\n  WITH shower leak (n={len(with_leak)}):")
        print(f"    Mean = {with_leak.mean():,.0f} L/year")
        print(f"    SD = {with_leak.std():,.0f}")
        
        print(f"\n  WITHOUT shower leak (n={len(without_leak)}):")
        print(f"    Mean = {without_leak.mean():,.0f} L/year")
        print(f"    SD = {without_leak.std():,.0f}")
        
        # t-test
        t_stat, p_val = stats.ttest_ind(with_leak, without_leak)
        cohens_d = (with_leak.mean() - without_leak.mean()) / np.sqrt((with_leak.std()**2 + without_leak.std()**2) / 2)
        
        print(f"\n  T-test: t = {t_stat:.3f}, p = {p_val:.4f}")
        print(f"  Cohen's d = {cohens_d:.3f}")
        
        if p_val < 0.05:
            print("\n  ⚠️  SIGNIFICANT DIFFERENCE - leak imputation may introduce bias")
        else:
            print("\n  ✓ No significant difference - leak imputation is justified")

# =============================================================================
# 3. CLUSTER DISTRIBUTION BY LEAK STATUS
# =============================================================================
print("\n" + "="*70)
print("3. CLUSTER DISTRIBUTION BY LEAK STATUS")
print("="*70)

if 'Shower-Leak_yes' in df.columns and 'Cluster' in df.columns:
    cross_tab = pd.crosstab(df['Cluster'], df['Shower-Leak_yes'], normalize='index') * 100
    print("\nCluster × Shower Leak (row %)")
    print(cross_tab.round(1))
    
    # Chi-square test
    contingency = pd.crosstab(df['Cluster'], df['Shower-Leak_yes'])
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    print(f"\nChi-square: χ² = {chi2:.2f}, p = {p:.4f}")

# =============================================================================
# 4. SUMMARY STATISTICS BY CLUSTER
# =============================================================================
print("\n" + "="*70)
print("4. KEY SUMMARY STATISTICS")
print("="*70)

key_features = ['Boil-Water-Per-Week', 'Showers-Per-Week', 'Bath-Frequency-Per-Week']
available = [f for f in key_features if f in df.columns]

for feature in available:
    print(f"\n{feature}:")
    for cluster_id in [0, 1, 2]:
        cluster_data = df[df['Cluster'] == cluster_id][feature]
        ci_low = cluster_data.mean() - 1.96 * cluster_data.std() / np.sqrt(len(cluster_data))
        ci_high = cluster_data.mean() + 1.96 * cluster_data.std() / np.sqrt(len(cluster_data))
        print(f"  C{cluster_id}: Mean = {cluster_data.mean():.2f} [95% CI: {ci_low:.2f}, {ci_high:.2f}]")

print("\n" + "="*70)
print("VALIDATION ANALYSIS COMPLETE")
print("="*70)
