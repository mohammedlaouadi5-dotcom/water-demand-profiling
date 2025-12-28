import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
from sklearn import tree
import warnings
warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\clustered_data_optimized.csv'
MAX_DEPTH = 5  # Control rule complexity
MIN_SAMPLES_LEAF = 50  # Ensure rules are generalizable

def main():
    print("### XAI: Global Rule Extraction (Workstream IV - T.7.1) ###\n")
    
    # Load clustered data
    print(f"Loading data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    print(f"Shape: {df.shape}")
    print(f"Clusters: {df['Cluster'].nunique()}")
    
    # Prepare features and target
    X = df.drop(columns=['Cluster'])
    y = df['Cluster']
    
    # Handle categorical variables (one-hot encode)
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
    
    # --- Train Decision Tree for Rule Extraction ---
    print(f"\n{'='*60}")
    print("Training Decision Tree Classifier")
    print(f"{'='*60}")
    
    dt_classifier = DecisionTreeClassifier(
        max_depth=MAX_DEPTH,
        min_samples_leaf=MIN_SAMPLES_LEAF,
        random_state=42,
        class_weight='balanced'  # Handle imbalanced clusters
    )
    
    dt_classifier.fit(X_train, y_train)
    
    # Evaluate
    y_pred = dt_classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    # --- Extract Rules ---
    print(f"\n{'='*60}")
    print("GLOBAL RULE-LISTS (IF-THEN Format)")
    print(f"{'='*60}\n")
    
    # Generate text rules
    feature_names = X_encoded.columns.tolist()
    tree_rules = export_text(dt_classifier, feature_names=feature_names, max_depth=MAX_DEPTH)
    print(tree_rules)
    
    # --- Feature Importance ---
    print(f"\n{'='*60}")
    print("TOP 15 MOST IMPORTANT FEATURES FOR CLUSTER PREDICTION")
    print(f"{'='*60}\n")
    
    feature_importance = pd.DataFrame({
        'Feature': feature_names,
        'Importance': dt_classifier.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print(feature_importance.head(15).to_string(index=False))
    
    # --- Visualize Tree (Top 3 levels) ---
    print("\nGenerating decision tree visualization...")
    plt.figure(figsize=(20, 10))
    tree.plot_tree(
        dt_classifier,
        feature_names=feature_names,
        class_names=[f"Cluster {i}" for i in sorted(y.unique())],
        filled=True,
        rounded=True,
        fontsize=8,
        max_depth=3  # Only top levels for visualization
    )
    plt.title("Decision Tree - Cluster Prediction Rules (Top 3 Levels)", fontsize=16)
    
    viz_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\decision_tree_rules.png'
    plt.savefig(viz_path, dpi=150, bbox_inches='tight')
    print(f"Decision tree visualization saved to: {viz_path}")
    plt.close()
    
    # --- Save outputs ---
    # Save feature importance
    importance_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\feature_importance.csv'
    feature_importance.to_csv(importance_path, index=False)
    print(f"\nFeature importance saved to: {importance_path}")
    
    # Save text rules
    rules_path = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\decision_rules.txt'
    with open(rules_path, 'w') as f:
        f.write("="*60 + "\n")
        f.write("DECISION TREE RULES FOR CLUSTER ASSIGNMENT\n")
        f.write("="*60 + "\n\n")
        f.write(f"Model Accuracy: {accuracy:.2%}\n\n")
        f.write(tree_rules)
    print(f"Rules saved to: {rules_path}")
    
    # --- Generate Semantic Cluster Labels ---
    print(f"\n{'='*60}")
    print("CLUSTER PROFILING FOR SEMANTIC LABELING")
    print(f"{'='*60}\n")
    
    # Analyze top features per cluster
    for cluster_id in sorted(y.unique()):
        cluster_data = df[df['Cluster'] == cluster_id]
        print(f"\n--- Cluster {cluster_id} (n={len(cluster_data)}) ---")
        
        # Show key numeric stats
        key_metrics = [c for c in numeric_cols if any(keyword in c for keyword in 
                      ['Water-Use', 'Energy-Use', 'Duration', 'Shower', 'Frequency'])][:5]
        
        if key_metrics:
            print("Key metrics (mean):")
            for metric in key_metrics:
                if metric in cluster_data.columns:
                    mean_val = cluster_data[metric].mean()
                    overall_mean = df[metric].mean()
                    pct_diff = ((mean_val - overall_mean) / overall_mean * 100) if overall_mean != 0 else 0
                    print(f"  {metric}: {mean_val:.2f} ({pct_diff:+.1f}% vs overall)")
    
    print("\n" + "="*60)
    print("Rule extraction complete.")
    print("="*60)
    
if __name__ == "__main__":
    main()
