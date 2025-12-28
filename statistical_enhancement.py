import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def calculate_eta_squared(f_value, df_between, df_error):
    """Calculate Eta-squared for ANOVA."""
    return (f_value * df_between) / ((f_value * df_between) + df_error)

def calculate_cramers_v(chi2, n, min_dim):
    """Calculate Cramer's V for Chi-square."""
    return np.sqrt(chi2 / (n * (min_dim - 1)))

def run_comprehensive_validation(df, cluster_col='Cluster', output_path='validation_report.csv'):
    results = []
    
    # 1. Numerical Validation (ANOVA)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [c for c in numeric_cols if c not in [cluster_col, 'Max_Prob']]
    
    print(f"Validating {len(numeric_cols)} numerical features...")
    
    for col in numeric_cols:
        groups = [df[df[cluster_col] == k][col].dropna() for k in sorted(df[cluster_col].unique())]
        
        # Skip if not enough data
        if any(len(g) < 2 for g in groups):
            continue
            
        # ANOVA
        f_stat, p_val = stats.f_oneway(*groups)
        
        # Effect Size (Eta Squared)
        k = len(groups)
        n = len(df)
        eta_sq = calculate_eta_squared(f_stat, k-1, n-k)
        
        # Normality & Homogeneity
        # shapiro_stat, shapiro_p = stats.shapiro(df[col].dropna()) # Too slow for large N
        levene_stat, levene_p = stats.levene(*groups)
        
        results.append({
            'Feature': col,
            'Test': 'ANOVA',
            'Statistic': f_stat,
            'P-Value': p_val,
            'Effect_Size': eta_sq,
            'Effect_Metric': 'Eta-Squared',
            'Assumption_Levene_P': levene_p,
            'Significant': p_val < 0.05
        })
        
    # 2. Categorical Validation (Chi-Square)
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns
    categorical_cols = [c for c in categorical_cols if c != cluster_col]
    
    print(f"Validating {len(categorical_cols)} categorical features...")
    
    for col in categorical_cols:
        contingency_table = pd.crosstab(df[col], df[cluster_col])
        
        # Chi-Square
        chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
        
        # Effect Size (Cramer's V)
        n = contingency_table.sum().sum()
        min_dim = min(contingency_table.shape)
        cramers_v = calculate_cramers_v(chi2, n, min_dim)
        
        results.append({
            'Feature': col,
            'Test': 'Chi-Square',
            'Statistic': chi2,
            'P-Value': p,
            'Effect_Size': cramers_v,
            'Effect_Metric': 'Cramers-V',
            'Assumption_Levene_P': np.nan,
            'Significant': p < 0.05
        })
        
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False)
    print(f"Validation report saved to {output_path}")
    return results_df

if __name__ == "__main__":
    # Test run
    df = pd.read_csv(r'clustered_data_optimized.csv')
    run_comprehensive_validation(df)
