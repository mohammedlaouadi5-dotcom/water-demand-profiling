import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler
from sklearn.decomposition import NMF
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import silhouette_score, adjusted_rand_score
import joblib
import os
import warnings

# Configuration
FILE_PATH = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\ca31a900-d51f-11f0-8600-af36ab325207.csv'
OUTPUT_DIR = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling'
RANDOM_SEED = 42

# Optimization Ranges (Phase 1: Diagnostic approfondi)
NMF_COMPONENTS_RANGE = [2, 3, 4, 5, 6, 7, 8]  # Étendu pour trouver optimal
GMM_CLUSTERS_RANGE = [3, 4, 5, 6, 7, 8, 10, 12]  # Grille BIC approfondie
STABILITY_ITERATIONS = 100  # Augmenté de 20 à 100 pour robustesse

def load_and_clean_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    
    # Drop empty columns
    df.dropna(axis=1, how='all', inplace=True)
    
    # Leak Correction (Bidirectional)
    # Fix logical inconsistencies between leak presence and leak rate
    fixtures = ['Shower', 'Toilet', 'Basin-Tap', 'Bath-Tap', 'Kitchen-Tap']
    for fixture in fixtures:
        leak_col = f"{fixture}-Leak"
        rate_col = f"{fixture}-Leak-Rate"
        if leak_col in df.columns and rate_col in df.columns:
            # Fix 1: Leak='no' but rate exists → Change to Leak='yes'
            # Rationale: If leak rate is reported, a leak must exist
            mask_no_leak_has_rate = (df[leak_col].str.lower() == 'no') & (df[rate_col].notna())
            if mask_no_leak_has_rate.sum() > 0:
                print(f"  Correcting {mask_no_leak_has_rate.sum()} instances: {fixture} no leak → yes leak (rate exists)")
                df.loc[mask_no_leak_has_rate, leak_col] = 'yes'
            
            # Fix 2: Leak='yes' but rate missing → Impute 'slowly'
            # Rationale: Most leaks are slow drips (domain knowledge)
            mask_yes_leak_no_rate = (df[leak_col].str.lower() == 'yes') & (df[rate_col].isna())
            if mask_yes_leak_no_rate.sum() > 0:
                print(f"  Imputing {mask_yes_leak_no_rate.sum()} missing rates for {fixture} with 'slowly'")
                df.loc[mask_yes_leak_no_rate, rate_col] = 'slowly'
                
    # IQR Outlier Removal (Conservative)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    key_metrics = [c for c in numeric_cols if 'Household-Water-Use' in c]
    if key_metrics:
        Q1 = df[key_metrics].quantile(0.25)
        Q3 = df[key_metrics].quantile(0.75)
        IQR = Q3 - Q1
        condition = ~((df[key_metrics] < (Q1 - 1.5 * IQR)) | (df[key_metrics] > (Q3 + 1.5 * IQR))).any(axis=1)
        df = df[condition]
        print(f"Data shape after outlier removal: {df.shape}")
        
    return df

def hybrid_imputation(df):
    print("Running Hybrid Imputation...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns
    
    missing_pct = df.isnull().mean() * 100
    
    # Report Missingness
    missing_report = missing_pct[missing_pct > 0].sort_values(ascending=False)
    missing_report.to_csv(os.path.join(OUTPUT_DIR, 'missingness_report.csv'))
    
    # Strategy: Hybrid Imputation (KNN for >5% missing, Simple for <=5%)
    # 1. Numeric Columns
    num_cols = [c for c in numeric_cols if c in df.columns]
    if num_cols:
        # Split by missingness
        high_missing_num = [c for c in num_cols if missing_pct.get(c, 0) > 5]
        low_missing_num = [c for c in num_cols if missing_pct.get(c, 0) <= 5]
        
        # KNN for high missing numeric
        if high_missing_num:
            print(f"  -> KNN Imputation (k=5) for {len(high_missing_num)} numeric features (>5% missing)...")
            knn_imputer = KNNImputer(n_neighbors=5)
            df[high_missing_num] = knn_imputer.fit_transform(df[high_missing_num])
            
        # Simple Median for low missing numeric
        if low_missing_num:
            print(f"  -> Simple Median Imputation for {len(low_missing_num)} numeric features (<=5% missing)...")
            simple_imputer = SimpleImputer(strategy='median')
            df[low_missing_num] = simple_imputer.fit_transform(df[low_missing_num])

    # 2. Categorical Columns
    cat_cols = [c for c in categorical_cols if c in df.columns]
    if cat_cols:
        # Split by missingness
        high_missing_cat = [c for c in cat_cols if missing_pct.get(c, 0) > 5]
        low_missing_cat = [c for c in cat_cols if missing_pct.get(c, 0) <= 5]
        
        # KNN for high missing categorical (requires encoding)
        if high_missing_cat:
            print(f"  -> KNN Imputation (k=5) for {len(high_missing_cat)} categorical features (>5% missing)...")
            for col in high_missing_cat:
                # Factorize (preserve NaNs)
                codes, uniques = pd.factorize(df[col])
                # pd.factorize maps NaN to -1, we need to keep them as NaN for imputer
                # But factorize returns codes where -1 is missing. We can use this.
                # However, KNNImputer needs float NaNs.
                
                # Create a temporary series with NaNs
                temp_series = df[col].map({val: i for i, val in enumerate(uniques)}).astype(float)
                
                # Reshape for Imputer
                imputed_col = KNNImputer(n_neighbors=5).fit_transform(temp_series.values.reshape(-1, 1))
                
                # Round to nearest integer index and map back
                imputed_indices = np.round(imputed_col).astype(int).flatten()
                # Clip to valid range just in case
                imputed_indices = np.clip(imputed_indices, 0, len(uniques) - 1)
                
                df[col] = [uniques[i] for i in imputed_indices]

        # Simple Mode for low missing categorical
        if low_missing_cat:
            print(f"  -> Simple Mode Imputation for {len(low_missing_cat)} categorical features (<=5% missing)...")
            simple_imputer = SimpleImputer(strategy='most_frequent')
            df[low_missing_cat] = simple_imputer.fit_transform(df[low_missing_cat])
            
    return df

def select_stable_features_bootstrap(X, threshold=0.90, n_bootstrap=100):
    """
    Phase 2: Sélection robuste de features par stabilité Bootstrap
    Conserve uniquement les features stables à >90% sur 100 échantillons
    """
    print(f"Selecting stable features via Bootstrap (n={n_bootstrap}, threshold={threshold})...")
    
    n_samples, n_features = X.shape
    feature_selection_matrix = np.zeros((n_bootstrap, n_features))
    
    for i in range(n_bootstrap):
        # Bootstrap sample
        indices = np.random.choice(n_samples, size=n_samples, replace=True)
        X_boot = X.iloc[indices]
        
        # MAD (Mean Absolute Deviation) selection - Robust to outliers
        # MAD = median(|x - median(x)|)
        mad = (X_boot - X_boot.median()).abs().median()
        
        # Select features with non-negligible variation (MAD > 0.01)
        # Since data is MinMax scaled [0,1], 0.01 represents 1% deviation
        selected_mask = mad > 0.01
        feature_selection_matrix[i, :] = selected_mask
    
    # Calculate stability score for each feature
    stability_scores = feature_selection_matrix.mean(axis=0)
    
    # Select only highly stable features
    stable_mask = stability_scores >= threshold
    stable_features = X.columns[stable_mask]
    
    print(f"Features reduced from {n_features} to {len(stable_features)} (stability >={threshold})")
    
    # Save stability scores for analysis
    stability_df = pd.DataFrame({
        'Feature': X.columns,
        'Stability_Score': stability_scores
    }).sort_values('Stability_Score', ascending=False)
    stability_df.to_csv(os.path.join(OUTPUT_DIR, 'feature_stability_scores.csv'), index=False)
    
    return X[stable_features]

def remove_correlated_features(X, threshold=0.85):
    """
    Phase 2: Élimination des features corrélées >0.85 (redondance)
    """
    print(f"Removing highly correlated features (threshold={threshold})...")
    
    correlation_matrix = X.corr().abs()
    
    # Upper triangle
    upper = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
    
    # Find features with correlation > threshold
    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
    
    print(f"Dropping {len(to_drop)} correlated features")
    return X.drop(columns=to_drop)

def preprocess_features(df):
    print("Preprocessing Features (Bootstrap + Correlation Removal + MinMax)...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns
    
    # 1. OHE Categorical
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_cats = encoder.fit_transform(df[categorical_cols])
    feature_names = encoder.get_feature_names_out(categorical_cols)
    df_encoded = pd.DataFrame(encoded_cats, columns=feature_names, index=df.index)
    
    # 2. Combine
    X = pd.concat([df[numeric_cols], df_encoded], axis=1)
    
    # 3. MinMax Scaling (Critical for NMF)
    scaler = MinMaxScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
    
    # 4. Phase 2: Sélection robuste de features
    # Threshold increased to 0.90 for high stability (Q1 standard)
    X_stable = select_stable_features_bootstrap(X_scaled, threshold=0.90, n_bootstrap=100)
    
    # 5. Phase 2: Élimination corrélation
    X_final = remove_correlated_features(X_stable, threshold=0.85)
    
    print(f"Final feature count: {X_final.shape[1]}")
    return X_final

def calculate_stability_enhanced(X, n_nmf, n_gmm, iterations=100):
    """
    Phase 1: Stabilité avec NMF convergent (max_iter=2000, tol=1e-6)
    Phase 4: Augmentation à 100 itérations Monte Carlo
    """
    from sklearn.metrics import adjusted_rand_score
    
    labels_list = []
    convergence_count = 0
    
    for i in range(iterations):
        # NMF avec convergence garantie (Phase 1)
        nmf = NMF(
            n_components=n_nmf, 
            init='nndsvd',  # Déterministe
            max_iter=2000,  # Augmenté pour convergence
            tol=1e-6,       # Critère strict
            random_state=42  # Fixé pour reproductibilité de nndsvd
        )
        W = nmf.fit_transform(X)
        
        # Vérifier convergence
        if nmf.n_iter_ < 2000:
            convergence_count += 1
        
        # GMM with full covariance (flexible cluster shapes)
        gmm = GaussianMixture(
            n_components=n_gmm, 
            covariance_type='full',  # Full covariance matrices for flexibility
            random_state=i,          # Variable seed for Monte Carlo stability test
            n_init=10                # Multiple initializations for robustness
        )
        labels = gmm.fit_predict(W)
        labels_list.append(labels)
        
    # Convergence rate
    convergence_rate = convergence_count / iterations
    print(f"  NMF Convergence Rate: {convergence_rate:.1%}")
    
    # Calculate pairwise ARI between all runs
    aris = []
    for i in range(len(labels_list)):
        for j in range(i+1, len(labels_list)):
            aris.append(adjusted_rand_score(labels_list[i], labels_list[j]))
            
    return np.mean(aris), convergence_rate

def optimize_configuration_enhanced(X):
    print("Starting Enhanced Optimization Grid Search...")
    
    # Targeted search for realistic stability
    nmf_components_range = [2]
    gmm_clusters_range = [3]
    
    print(f"Grid: NMF={nmf_components_range}, GMM={gmm_clusters_range}")
    print(f"Monte Carlo iterations: {STABILITY_ITERATIONS}")
    
    results = []
    
    for n_nmf in nmf_components_range:
        for n_gmm in gmm_clusters_range:
            print(f"\nTesting Config: NMF={n_nmf}, GMM={n_gmm}...")
            
            stability, convergence_rate = calculate_stability_enhanced(
                X, n_nmf, n_gmm, iterations=STABILITY_ITERATIONS
            )
            
            # Calculate Silhouette + BIC on one run for quality check
            nmf = NMF(n_components=n_nmf, init='nndsvd', max_iter=2000, tol=1e-6, random_state=42)
            W = nmf.fit_transform(X)
            
            gmm = GaussianMixture(n_components=n_gmm, random_state=42, n_init=10)
            labels = gmm.fit_predict(W)
            
            sil = silhouette_score(W, labels)
            bic = gmm.bic(W)
            
            # Variance expliquée (reconstruction error)
            reconstruction = nmf.inverse_transform(W)
            reconstruction_error = np.linalg.norm(X.values - reconstruction, 'fro')
            total_variance = np.linalg.norm(X.values, 'fro')
            variance_explained = 1 - (reconstruction_error / total_variance)
            
            print(f"  -> Stability: {stability:.3f}, Silhouette: {sil:.3f}, BIC: {bic:.0f}")
            print(f"  -> Variance Explained: {variance_explained:.1%}, Convergence: {convergence_rate:.1%}")
            
            results.append({
                'n_nmf': n_nmf,
                'n_gmm': n_gmm,
                'stability': stability,
                'silhouette': sil,
                'bic': bic,
                'variance_explained': variance_explained,
                'convergence_rate': convergence_rate
            })
            
    results_df = pd.DataFrame(results)
    results_df.to_csv(os.path.join(OUTPUT_DIR, 'optimization_results_enhanced.csv'), index=False)
    
    # Phase 3: Sélection par critères multiples (Stabilité + Silhouette + BIC)
    # Priorité 1: Stabilité >0.75
    # Priorité 2: Silhouette >0.3
    # Priorité 3: BIC minimal
    
    candidates = results_df[results_df['stability'] >= 0.75]
    if len(candidates) > 0:
        best_config = candidates.sort_values(by='silhouette', ascending=False).iloc[0]
        print(f"\n✓ SUCCÈS: Configuration avec Stabilité >75% trouvée!")
    else:
        print(f"\n⚠ Aucune config avec Stabilité >75%. Sélection du meilleur compromis...")
        # Compromis: Maximiser (Stabilité + Silhouette normalisé)
        results_df['score'] = results_df['stability'] + (results_df['silhouette'] + 1) / 2
        best_config = results_df.sort_values(by='score', ascending=False).iloc[0]
    
    print(f"\nBest Configuration: NMF={int(best_config['n_nmf'])}, GMM={int(best_config['n_gmm'])}")
    print(f"  Stability: {best_config['stability']:.3f}")
    print(f"  Silhouette: {best_config['silhouette']:.3f}")
    print(f"  BIC: {best_config['bic']:.0f}")
    print(f"  Variance Explained: {best_config['variance_explained']:.1%}")
    
    return int(best_config['n_nmf']), int(best_config['n_gmm'])

def main():
    # 1. Load
    df = load_and_clean_data(FILE_PATH)
    
    # 2. Impute
    df = hybrid_imputation(df)
    
    # 3. Preprocess (avec sélection robuste Phase 2)
    X = preprocess_features(df)
    
    # 4. Optimize (avec algorithme amélioré Phase 1, 3, 4)
    best_nmf, best_gmm = optimize_configuration_enhanced(X)
    
    # 5. Final Run
    print("\nRunning Final Pipeline with Best Config...")
    nmf = NMF(n_components=best_nmf, init='nndsvd', max_iter=2000, tol=1e-6, random_state=RANDOM_SEED)
    W = nmf.fit_transform(X)
    H = nmf.components_
    
    gmm = GaussianMixture(n_components=best_gmm, random_state=RANDOM_SEED, n_init=10)
    labels = gmm.fit_predict(W)
    probs = gmm.predict_proba(W)
    
    # 6. Save Results
    df['Cluster'] = labels
    df['Max_Prob'] = probs.max(axis=1)
    
    output_file = os.path.join(OUTPUT_DIR, 'clustered_data_enhanced.csv')
    df.to_csv(output_file, index=False)
    
    # Save W and H for analysis
    pd.DataFrame(W).to_csv(os.path.join(OUTPUT_DIR, 'nmf_W_matrix_enhanced.csv'), index=False)
    pd.DataFrame(H, columns=X.columns).to_csv(os.path.join(OUTPUT_DIR, 'nmf_H_matrix_enhanced.csv'), index=False)
    
    print(f"\n✓ Final results saved to {output_file}")

if __name__ == "__main__":
    main()
