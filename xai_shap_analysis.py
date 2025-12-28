import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import shap
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\clustered_data_enhanced.csv'
SHAP_SAMPLE_SIZE = 1000  # Sample for SHAP computation (computationally expensive)

def main():
    print("### XAI: SHAP Analysis (Workstream IV - T.7.2) ###\n")
    
    # Load clustered data
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    print(f"Shape: {df.shape}")
    print(f"Clusters: {df['Cluster'].nunique()}")
    
    # Prepare features and target
    X = df.drop(columns=['Cluster'])
    y = df['Cluster']
    
    # Handle categorical variables
    categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
    numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    
    print(f"\nCategorical features: {len(categorical_cols)}")
    print(f"Numeric features: {len(numeric_cols)}")
    
    # One-hot encode categoricals
    if categorical_cols:
        X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    else:
        X_encoded = X
    
    print(f"Encoded feature matrix shape: {X_encoded.shape}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # --- Train XGBoost Proxy Classifier ---
    print(f"\n{'='*60}")
    print("Training XGBoost Proxy Classifier for SHAP")
    print(f"{'='*60}")
    
    xgb_model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        eval_metric='mlogloss',
        use_label_encoder=False
    )
    
    xgb_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = xgb_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nProxy Model Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # --- SHAP Analysis ---
    print(f"\n{'='*60}")
    print("Computing SHAP Values")
    print(f"{'='*60}\n")
    
    # Use a sample for SHAP computation (full dataset too expensive)
    sample_size = min(SHAP_SAMPLE_SIZE, len(X_test))
    X_shap = X_test.sample(n=sample_size, random_state=42)
    
    print(f"Computing SHAP values for {sample_size} samples...")
    
    # Create SHAP explainer
    explainer = shap.TreeExplainer(xgb_model)
    shap_values = explainer.shap_values(X_shap)
    
    print("SHAP computation complete.")
    
    # --- SHAP Summary Plot (Global Feature Importance) ---
    print("\nGenerating SHAP summary plot...")
    
    plt.figure(figsize=(12, 8))
    shap.summary_plot(
        shap_values,
        X_shap,
        plot_type="bar",
        show=False,
        max_display=20
    )
    plt.title("SHAP Feature Importance (Global)", fontsize=14, pad=20)
    plt.tight_layout()
    
    summary_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\shap_summary.png'
    plt.savefig(summary_path, dpi=150, bbox_inches='tight')
    print(f"SHAP summary plot saved to: {summary_path}")
    plt.close()
    
    # --- SHAP Beeswarm Plot (Feature Impact) ---
    print("Generating SHAP beeswarm plot...")
    
    plt.figure(figsize=(12, 10))
    shap.summary_plot(
        shap_values,
        X_shap,
        show=False,
        max_display=20
    )
    plt.title("SHAP Feature Impact on Cluster Assignment", fontsize=14, pad=20)
    plt.tight_layout()
    
    beeswarm_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\shap_beeswarm.png'
    plt.savefig(beeswarm_path, dpi=150, bbox_inches='tight')
    print(f"SHAP beeswarm plot saved to: {beeswarm_path}")
    plt.close()
    
    # --- Local Explanation Example ---
    print(f"\n{'='*60}")
    print("EXAMPLE LOCAL EXPLANATION (SHAP)")
    print(f"{'='*60}\n")
    
    # Select a sample household for local explanation
    sample_idx = 0
    sample_household = X_shap.iloc[sample_idx:sample_idx+1]
    sample_cluster = xgb_model.predict(sample_household)[0]
    
    print(f"Example Household (Index: {X_shap.index[sample_idx]})")
    print(f"Predicted Cluster: {sample_cluster}")
    print("\nTop 10 features contributing to this prediction:")
    
    # Get SHAP values for this sample
    print(f"DEBUG: type(shap_values): {type(shap_values)}")
    if isinstance(shap_values, list):
        print(f"DEBUG: len(shap_values): {len(shap_values)}")
        sample_shap = shap_values[sample_cluster][sample_idx]
    elif len(shap_values.shape) == 3:
        print(f"DEBUG: shap_values.shape (3D): {shap_values.shape}")
        # Multi-class single array: (n_samples, n_features, n_classes)
        sample_shap = shap_values[sample_idx, :, sample_cluster]
    else:
        print(f"DEBUG: shap_values.shape (2D): {shap_values.shape}")
        # Single output
        sample_shap = shap_values[sample_idx]
    
    feature_names = X_shap.columns.tolist()
    
    # Ensure arrays are 1D
    if hasattr(sample_shap, 'shape') and len(sample_shap.shape) > 1:
        sample_shap = sample_shap.flatten()
    
    sample_values = sample_household.values.flatten()
    
    print(f"DEBUG: feature_names length: {len(feature_names)}")
    print(f"DEBUG: sample_shap shape: {sample_shap.shape}")
    print(f"DEBUG: sample_values shape: {sample_values.shape}")
    
    shap_df = pd.DataFrame({
        'Feature': feature_names,
        'SHAP_Value': sample_shap,
        'Actual_Value': sample_values
    }).sort_values('SHAP_Value', key=abs, ascending=False)
    
    print(shap_df.head(10).to_string(index=False))
    
    # --- SHAP Force Plot for one prediction ---
    print("\nGenerating SHAP force plot for example household...")
    
    try:
        shap.initjs()
        if isinstance(shap_values, list):
            exp_value = explainer.expected_value[sample_cluster]
            shap_val = shap_values[sample_cluster][sample_idx]
        else:
            exp_value = explainer.expected_value
            shap_val = shap_values[sample_idx]
        
        force_plot = shap.force_plot(
            exp_value,
            shap_val,
            sample_household,
            matplotlib=True,
            show=False
        )
        
        force_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\shap_force_plot.png'
        plt.savefig(force_path, dpi=150, bbox_inches='tight')
        print(f"SHAP force plot saved to: {force_path}")
        plt.close()
    except Exception as e:
        print(f"Could not generate force plot: {e}")
    
    # --- Save SHAP Values ---
    print("\nSaving SHAP values to CSV...")
    
    # Average absolute SHAP values across all samples
    if isinstance(shap_values, list):
        # Multi-class: average across all classes
        mean_shap = np.mean([np.mean(np.abs(sv), axis=0) for sv in shap_values], axis=0)
    elif len(shap_values.shape) == 3:
        # (n_samples, n_features, n_classes)
        mean_shap = np.mean(np.abs(shap_values), axis=(0, 2))
    else:
        mean_shap = np.mean(np.abs(shap_values), axis=0)
    
    shap_importance = pd.DataFrame({
        'Feature': feature_names,
        'Mean_Abs_SHAP': mean_shap
    }).sort_values('Mean_Abs_SHAP', ascending=False)
    
    shap_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\shap_importance.csv'
    shap_importance.to_csv(shap_path, index=False)
    print(f"SHAP importance saved to: {shap_path}")
    
    print("\n" + "="*60)
    print("SHAP analysis complete.")
    print("="*60)
    
    # --- XAI Quality Assessment ---
    print(f"\n{'='*60}")
    print("XAI QUALITY ASSESSMENT")
    print(f"{'='*60}")
    print(f"✓ Proxy Model Accuracy: {accuracy:.2%}")
    print(f"✓ SHAP Values Computed: {len(X_shap)} samples")
    print(f"✓ Top Features Identified: {len(shap_importance)}")
    print("\nTop 5 globally important features:")
    print(shap_importance.head(5).to_string(index=False))
    
if __name__ == "__main__":
    main()
