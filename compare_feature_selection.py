import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.feature_selection import VarianceThreshold, mutual_info_regression, RFE
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration
FILE_PATH = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\ca31a900-d51f-11f0-8600-af36ab325207.csv'
OUTPUT_DIR = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling'
RANDOM_SEED = 42

def load_and_preprocess(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Basic cleaning
    df.dropna(axis=1, how='all', inplace=True)
    
    # Identify Target (Total Water Use)
    # Looking for columns like 'Household-Water-Use-Litres-Per-Day'
    target_cols = [c for c in df.columns if 'Household-Water-Use' in c and 'Litres-Per-Day' in c]
    if not target_cols:
        target_cols = [c for c in df.columns if 'Household-Water-Use' in c]
    
    if not target_cols:
        raise ValueError("No target column found for supervised feature selection!")
    
    target_col = target_cols[0]
    print(f"Target for supervised methods: {target_col}")
    
    y = df[target_col].copy()
    X_raw = df.drop(columns=[target_col])
    
    # Drop other potential target-leak columns (e.g., other total use metrics)
    leak_cols = [c for c in X_raw.columns if 'Household-Water-Use' in c]
    X_raw.drop(columns=leak_cols, inplace=True)
    
    # Impute X
    numeric_cols = X_raw.select_dtypes(include=[np.number]).columns
    categorical_cols = X_raw.select_dtypes(exclude=[np.number]).columns
    
    if len(numeric_cols) > 0:
        X_raw[numeric_cols] = SimpleImputer(strategy='median').fit_transform(X_raw[numeric_cols])
    if len(categorical_cols) > 0:
        X_raw[categorical_cols] = SimpleImputer(strategy='most_frequent').fit_transform(X_raw[categorical_cols])
        
    # Impute y
    y = y.fillna(y.median())
    
    # Encode & Scale
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_cats = encoder.fit_transform(X_raw[categorical_cols])
    feature_names = encoder.get_feature_names_out(categorical_cols)
    df_encoded = pd.DataFrame(encoded_cats, columns=feature_names, index=X_raw.index)
    
    X = pd.concat([X_raw[numeric_cols], df_encoded], axis=1)
    
    scaler = MinMaxScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    
    return X_scaled, y

def get_mad_features(X, top_n=50):
    # MAD = median(|x - median(x)|)
    mad = (X - X.median()).abs().median()
    # Select top N features with highest MAD (most variation)
    selected = mad.sort_values(ascending=False).head(top_n).index.tolist()
    return selected, mad

def get_variance_features(X, top_n=50):
    var = X.var()
    selected = var.sort_values(ascending=False).head(top_n).index.tolist()
    return selected, var

def get_lasso_features(X, y, top_n=50):
    # LassoCV automatically finds best alpha
    lasso = LassoCV(cv=3, random_state=RANDOM_SEED)
    lasso.fit(X, y)
    
    importance = pd.Series(np.abs(lasso.coef_), index=X.columns)
    selected = importance.sort_values(ascending=False).head(top_n).index.tolist()
    return selected, importance

def get_rf_features(X, y, top_n=50):
    rf = RandomForestRegressor(n_estimators=50, random_state=RANDOM_SEED, n_jobs=-1)
    rf.fit(X, y)
    
    importance = pd.Series(rf.feature_importances_, index=X.columns)
    selected = importance.sort_values(ascending=False).head(top_n).index.tolist()
    return selected, importance

def get_mi_features(X, y, top_n=50):
    # Mutual Information
    mi = mutual_info_regression(X, y, random_state=RANDOM_SEED)
    importance = pd.Series(mi, index=X.columns)
    selected = importance.sort_values(ascending=False).head(top_n).index.tolist()
    return selected, importance

def main():
    X, y = load_and_preprocess(FILE_PATH)
    print(f"Processed Data: {X.shape}")
    
    TOP_N = 50
    results = {}
    
    print("\nRunning MAD (Unsupervised)...")
    mad_feats, mad_scores = get_mad_features(X, TOP_N)
    results['MAD'] = set(mad_feats)
    
    print("Running Variance (Unsupervised - Baseline)...")
    var_feats, var_scores = get_variance_features(X, TOP_N)
    results['Variance'] = set(var_feats)
    
    print("Running LASSO (Supervised)...")
    lasso_feats, lasso_scores = get_lasso_features(X, y, TOP_N)
    results['LASSO'] = set(lasso_feats)
    
    print("Running Random Forest (Supervised)...")
    rf_feats, rf_scores = get_rf_features(X, y, TOP_N)
    results['RandomForest'] = set(rf_feats)
    
    print("Running Mutual Information (Supervised)...")
    mi_feats, mi_scores = get_mi_features(X, y, TOP_N)
    results['MutualInfo'] = set(mi_feats)
    
    # Compare Overlaps (Jaccard Index)
    methods = list(results.keys())
    similarity_matrix = pd.DataFrame(index=methods, columns=methods)
    
    print("\n--- Jaccard Similarity between Methods (Top 50 Features) ---")
    for m1 in methods:
        for m2 in methods:
            s1 = results[m1]
            s2 = results[m2]
            jaccard = len(s1.intersection(s2)) / len(s1.union(s2))
            similarity_matrix.loc[m1, m2] = jaccard
            
    print(similarity_matrix)
    similarity_matrix.to_csv(os.path.join(OUTPUT_DIR, 'feature_selection_similarity.csv'))
    
    # Save top features for each
    comparison_df = pd.DataFrame({
        'Rank': range(1, TOP_N + 1),
        'MAD': mad_feats,
        'Variance': var_feats,
        'LASSO': lasso_feats,
        'RandomForest': rf_feats,
        'MutualInfo': mi_feats
    })
    comparison_df.to_csv(os.path.join(OUTPUT_DIR, 'feature_selection_comparison.csv'), index=False)
    print(f"\nDetailed comparison saved to {os.path.join(OUTPUT_DIR, 'feature_selection_comparison.csv')}")

if __name__ == "__main__":
    main()
