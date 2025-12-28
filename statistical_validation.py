import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\clustered_data_enhanced.csv'
ALPHA = 0.05  # Significance level

def main():
    print("### Statistical Validation - Workstream III ###\n")
    
    # Load clustered data
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    print(f"Shape: {df.shape}")
    print(f"Clusters: {df['Cluster'].nunique()}")
    
    # Separate columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove 'Cluster' from lists
    if 'Cluster' in categorical_cols:
        categorical_cols.remove('Cluster')
    if 'Cluster' in numeric_cols:
        numeric_cols.remove('Cluster')
    
    print(f"\nCategorical variables: {len(categorical_cols)}")
    print(f"Numeric variables: {len(numeric_cols)}")
    
    # --- T.5.1: Chi-square Tests ---
    print("\n" + "="*60)
    print("T.5.1: Chi-Square Tests (Categorical Variables)")
    print("="*60)
    
    chi2_results = []
    significant_count = 0
    
    for col in categorical_cols:
        # Skip if too many unique values (likely not truly categorical)
        if df[col].nunique() > 50:
            continue
            
        # Create contingency table
        contingency = pd.crosstab(df[col], df['Cluster'])
        
        # Perform Chi-square test
        chi2, p_value, dof, expected = chi2_contingency(contingency)
        
        is_significant = p_value < ALPHA
        if is_significant:
            significant_count += 1
        
        chi2_results.append({
            'Variable': col,
            'Chi2': chi2,
            'p-value': p_value,
            'DOF': dof,
            'Significant': is_significant
        })
    
    # Display results
    chi2_df = pd.DataFrame(chi2_results).sort_values('p-value')
    print(f"\nTotal tests: {len(chi2_df)}")
    print(f"Significant (p < {ALPHA}): {significant_count} ({significant_count/len(chi2_df)*100:.1f}%)")
    print("\nTop 10 most significant associations:")
    print(chi2_df.head(10)[['Variable', 'p-value', 'Significant']].to_string(index=False))
    
    # --- T.5.2: ANOVA + Tukey HSD ---
    print("\n" + "="*60)
    print("T.5.2: ANOVA Tests (Numeric Variables)")
    print("="*60)
    
    anova_results = []
    significant_anova_count = 0
    
    # Focus on key usage metrics
    key_metrics = [c for c in numeric_cols if any(keyword in c for keyword in 
                   ['Water-Use', 'Energy-Use', 'Duration', 'Shower', 'Frequency', 'Per-Week'])]
    
    if not key_metrics:
        key_metrics = numeric_cols[:20]  # Fallback to first 20 numeric
    
    print(f"\nTesting {len(key_metrics)} key numeric variables...")
    
    for col in key_metrics:
        # Group data by cluster
        groups = [df[df['Cluster'] == c][col].dropna() for c in df['Cluster'].unique()]
        
        # Remove empty groups
        groups = [g for g in groups if len(g) > 0]
        
        if len(groups) < 2:
            continue
        
        # Perform ANOVA
        f_stat, p_value = f_oneway(*groups)
        
        is_significant = p_value < ALPHA
        if is_significant:
            significant_anova_count += 1
        
        anova_results.append({
            'Variable': col,
            'F-statistic': f_stat,
            'p-value': p_value,
            'Significant': is_significant
        })
    
    # Display ANOVA results
    anova_df = pd.DataFrame(anova_results).sort_values('p-value')
    print(f"\nTotal tests: {len(anova_df)}")
    print(f"Significant (p < {ALPHA}): {significant_anova_count} ({significant_anova_count/len(anova_df)*100:.1f}%)")
    print("\nTop 10 most significant differences:")
    print(anova_df.head(10)[['Variable', 'p-value', 'Significant']].to_string(index=False))
    
    # Tukey HSD for top significant variable
    if significant_anova_count > 0:
        top_var = anova_df.iloc[0]['Variable']
        print(f"\n--- Tukey HSD Post-Hoc Test for: {top_var} ---")
        tukey_result = pairwise_tukeyhsd(df[top_var].dropna(), 
                                          df.loc[df[top_var].notna(), 'Cluster'])
        print(tukey_result)
    
    # --- Summary Report ---
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(f"Chi-square tests: {significant_count}/{len(chi2_df)} significant")
    print(f"ANOVA tests: {significant_anova_count}/{len(anova_df)} significant")
    
    # Q1 Criteria Check
    chi2_pass = (significant_count / len(chi2_df)) > 0.5 if len(chi2_df) > 0 else False
    anova_pass = (significant_anova_count / len(anova_df)) > 0.5 if len(anova_df) > 0 else False
    
    print(f"\nQ1 Criteria Assessment:")
    print(f"  ✓ Majority of Chi-square tests significant: {'PASS' if chi2_pass else 'FAIL'}")
    print(f"  ✓ Majority of ANOVA tests significant: {'PASS' if anova_pass else 'FAIL'}")
    
    # Save results
    output_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\validation_results.csv'
    combined_df = pd.concat([
        chi2_df.assign(Test='Chi-Square')[['Variable', 'p-value', 'Significant', 'Test']],
        anova_df[['Variable', 'p-value', 'Significant']].assign(Test='ANOVA')
    ])
    combined_df.to_csv(output_path, index=False)
    print(f"\nResults saved to: {output_path}")
    
    print("\nValidation complete.")

if __name__ == "__main__":
    main()
