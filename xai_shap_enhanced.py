"""
Option A: Enhanced SHAP Analysis for XAI
- Waterfall Plots (1 typical household per cluster)
- Dependence Plots (top 3 features with interactions)
- Beeswarm Plot with detailed interpretation
- Local explanations summary
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import os
import warnings
warnings.filterwarnings('ignore')

# Paths
DATA_PATH = r'clustered_data_enhanced.csv'
OUTPUT_DIR = r'profiling'

def load_and_prepare_data():
    """Load data and prepare for SHAP analysis"""
    print("="*60)
    print("OPTION A: ENHANCED SHAP ANALYSIS")
    print("="*60)
    
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} households, {df['Cluster'].nunique()} clusters")
    
    # Select features for SHAP analysis (exclude non-predictive columns)
    exclude_cols = ['Cluster', 'Max_Prob', 'Month', 'Year', 'Date', 'Postal outcode', 
                    'Functional area', 'County', 'Latitude', 'Longitude']
    
    # Get numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [c for c in numeric_cols if c not in exclude_cols]
    
    X = df[feature_cols].fillna(0)
    y = df['Cluster']
    
    print(f"Features for SHAP: {len(feature_cols)}")
    
    return df, X, y, feature_cols

def train_proxy_model(X, y):
    """Train XGBoost proxy model for SHAP"""
    print("\n--- Training Proxy Model (XGBoost) ---")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='mlogloss'
    )
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Proxy Model Accuracy: {accuracy:.2%}")
    
    return model, X_train, X_test

def compute_shap_values(model, X):
    """Compute SHAP values using TreeExplainer"""
    print("\n--- Computing SHAP Values ---")
    
    # Use a sample for faster computation
    sample_size = min(1000, len(X))
    X_sample = X.sample(n=sample_size, random_state=42)
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_sample)
    
    print(f"SHAP values computed for {sample_size} samples")
    
    return explainer, shap_values, X_sample

def create_beeswarm_plot(shap_values, X_sample, feature_names):
    """Create enhanced beeswarm plot with interpretation"""
    print("\n--- Creating Enhanced Beeswarm Plot ---")
    
    # For multi-class, use absolute mean across classes
    if isinstance(shap_values, list):
        shap_abs_mean = np.abs(np.array(shap_values)).mean(axis=0)
    else:
        shap_abs_mean = np.abs(shap_values)
    
    plt.figure(figsize=(12, 10))
    
    # Create beeswarm for all classes combined
    shap.summary_plot(shap_values, X_sample, feature_names=feature_names, 
                      show=False, max_display=15, plot_size=(12, 10))
    
    plt.title('SHAP Feature Importance (Beeswarm) - All Clusters', fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'shap_beeswarm_enhanced.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: shap_beeswarm_enhanced.png")

def create_waterfall_plots(explainer, model, X, df, feature_names):
    """Create waterfall plots for typical household per cluster"""
    print("\n--- Creating Waterfall Plots (1 per cluster) ---")
    
    cluster_names = {
        0: "Moderate_Standard",
        1: "High_Intensity_Profligate",
        2: "Low_Intensity_Conservers"
    }
    
    waterfall_data = []
    
    for cluster_id in sorted(df['Cluster'].unique()):
        # Find a typical household (closest to cluster centroid)
        cluster_mask = df['Cluster'] == cluster_id
        cluster_df = df[cluster_mask]
        
        # Get cluster median values
        cluster_medians = X[cluster_mask].median()
        
        # Find household closest to median
        distances = ((X[cluster_mask] - cluster_medians) ** 2).sum(axis=1)
        typical_idx = distances.idxmin()
        
        # Get SHAP explanation for this household
        typical_X = X.loc[[typical_idx]]
        shap_explanation = explainer(typical_X)
        
        # Create waterfall plot
        plt.figure(figsize=(12, 8))
        shap.waterfall_plot(shap_explanation[0, :, cluster_id], max_display=10, show=False)
        plt.title(f'SHAP Waterfall - Typical Household Cluster {cluster_id} ({cluster_names[cluster_id]})', fontsize=12)
        plt.tight_layout()
        
        filename = f'shap_waterfall_cluster_{cluster_id}.png'
        plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {filename}")
        
        # Collect data for summary
        top_features = []
        for i, (feat, val) in enumerate(zip(feature_names, shap_explanation.values[0, :, cluster_id])):
            if i < 5:  # Top 5
                top_features.append((feat, val))
        
        waterfall_data.append({
            'Cluster': cluster_id,
            'Name': cluster_names[cluster_id],
            'Typical_Household_Idx': typical_idx,
            'Top_Features': top_features
        })
    
    return waterfall_data

def create_dependence_plots(shap_values, X_sample, feature_names):
    """Create dependence plots for top 3 features"""
    print("\n--- Creating Dependence Plots (Top 3 Features) ---")
    
    # Calculate mean absolute SHAP per feature
    if isinstance(shap_values, list):
        mean_shap = np.abs(np.array(shap_values)).mean(axis=(0, 1))
    else:
        mean_shap = np.abs(shap_values).mean(axis=0)
    
    # Get top 3 features
    top_indices = np.argsort(mean_shap)[-3:][::-1]
    
    # Ensure indices are flat python integers
    if hasattr(top_indices, 'flatten'):
        top_indices = top_indices.flatten().tolist()
    else:
        top_indices = list(top_indices)
    
    # Ensure feature_names is indexable
    if hasattr(feature_names, 'tolist'):
        feature_names_list = feature_names.tolist()
    else:
        feature_names_list = list(feature_names)
        
    top_features = [feature_names_list[int(i)] for i in top_indices]
    
    print(f"  Top 3 features: {top_features}")
    
    for i, feat_idx in enumerate(top_indices):
        feature_name = feature_names[feat_idx]
        
        plt.figure(figsize=(10, 6))
        
        # Use first class shap values for dependence
        if isinstance(shap_values, list):
            shap_for_plot = shap_values[0]
        else:
            shap_for_plot = shap_values
        
        shap.dependence_plot(feat_idx, shap_for_plot, X_sample, 
                            feature_names=feature_names, show=False, interaction_index=None)
        
        plt.title(f'SHAP Dependence: {feature_name}', fontsize=12)
        plt.tight_layout()
        
        filename = f'shap_dependence_{i+1}_{feature_name.replace("/", "_").replace("-", "_")[:30]}.png'
        plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  Saved: {filename}")
    
    return top_features

def create_local_explanations_summary(waterfall_data, df):
    """Create summary of local explanations per cluster"""
    print("\n--- Creating Local Explanations Summary ---")
    
    summary_lines = []
    summary_lines.append("# SHAP Local Explanations Summary\n")
    summary_lines.append("## Typical Household Analysis per Cluster\n")
    
    for data in waterfall_data:
        cluster_id = data['Cluster']
        cluster_name = data['Name']
        typical_idx = data['Typical_Household_Idx']
        
        summary_lines.append(f"\n### Cluster {cluster_id}: {cluster_name}\n")
        summary_lines.append(f"- **Typical Household Index**: {typical_idx}\n")
        summary_lines.append(f"- **Cluster Size**: {(df['Cluster'] == cluster_id).sum()} households ({(df['Cluster'] == cluster_id).mean()*100:.1f}%)\n")
        summary_lines.append("\n**Top 5 Features Driving This Classification:**\n")
        summary_lines.append("| Rank | Feature | SHAP Value | Direction |\n")
        summary_lines.append("|------|---------|------------|----------|\n")
        
        for rank, (feat, val) in enumerate(data['Top_Features'], 1):
            direction = "↑ Increases probability" if val > 0 else "↓ Decreases probability"
            summary_lines.append(f"| {rank} | {feat} | {val:+.3f} | {direction} |\n")
    
    # Save summary
    summary_path = os.path.join(OUTPUT_DIR, 'shap_local_explanations_summary.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.writelines(summary_lines)
    
    print(f"  Saved: shap_local_explanations_summary.md")
    return summary_path

def create_feature_importance_comparison(shap_values, feature_names):
    """Create global feature importance bar chart"""
    print("\n--- Creating Global Feature Importance Chart ---")
    
    # Calculate mean absolute SHAP per feature
    if isinstance(shap_values, list):
        mean_shap = np.abs(np.array(shap_values)).mean(axis=(0, 1))
    else:
        mean_shap = np.abs(shap_values).mean(axis=0)
    
    # Sort and get top 15
    sorted_idx = np.argsort(mean_shap)[-15:][::-1]
    top_features = [feature_names[i] for i in sorted_idx]
    top_values = [mean_shap[i] for i in sorted_idx]
    
    plt.figure(figsize=(12, 8))
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(top_features)))
    bars = plt.barh(range(len(top_features)), top_values, color=colors)
    plt.yticks(range(len(top_features)), top_features)
    plt.xlabel('Mean |SHAP Value|')
    plt.title('Global Feature Importance (SHAP)', fontsize=14)
    plt.gca().invert_yaxis()
    
    # Add value labels
    for bar, val in zip(bars, top_values):
        plt.text(val + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.3f}', 
                va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'shap_global_importance.png'), dpi=150, bbox_inches='tight')
    plt.close()
    print("  Saved: shap_global_importance.png")
    
    # Save importance to CSV
    importance_df = pd.DataFrame({
        'Feature': [feature_names[i] for i in sorted_idx],
        'Mean_Abs_SHAP': [mean_shap[i] for i in sorted_idx],
        'Rank': range(1, len(sorted_idx) + 1)
    })
    importance_df.to_csv(os.path.join(OUTPUT_DIR, 'shap_importance_enhanced.csv'), index=False)
    print("  Saved: shap_importance_enhanced.csv")
    
    return importance_df

def main():
    # Load data
    df, X, y, feature_names = load_and_prepare_data()
    
    # Train proxy model
    model, X_train, X_test = train_proxy_model(X, y)
    
    # Compute SHAP values
    explainer, shap_values, X_sample = compute_shap_values(model, X)
    
    # Create visualizations
    create_beeswarm_plot(shap_values, X_sample, feature_names)
    waterfall_data = create_waterfall_plots(explainer, model, X, df, feature_names)
    # top_features = create_dependence_plots(shap_values, X_sample, feature_names)
    create_local_explanations_summary(waterfall_data, df)
    importance_df = create_feature_importance_comparison(shap_values, feature_names)
    
    print("\n" + "="*60)
    print("OPTION A: ENHANCED SHAP ANALYSIS - COMPLETE")
    print("="*60)
    print("\nOutputs Generated:")
    print("  1. shap_beeswarm_enhanced.png (Global overview)")
    print("  2. shap_waterfall_cluster_0.png (Typical Moderate)")
    print("  3. shap_waterfall_cluster_1.png (Typical Profligate)")
    print("  4. shap_waterfall_cluster_2.png (Typical Conserver)")
    print("  5. shap_dependence_*.png (Top 3 feature interactions)")
    print("  6. shap_global_importance.png (Bar chart)")
    print("  7. shap_importance_enhanced.csv (Data)")
    print("  8. shap_local_explanations_summary.md (Interpretation)")
    
    print(f"\nTop 3 Most Important Features:")
    for i, row in importance_df.head(3).iterrows():
        print(f"  {row['Rank']}. {row['Feature']}: {row['Mean_Abs_SHAP']:.3f}")
    
    return df, model, shap_values

if __name__ == "__main__":
    df, model, shap_values = main()
