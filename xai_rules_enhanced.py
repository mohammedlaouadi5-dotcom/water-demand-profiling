"""
Option B: Enhanced Decision Rules Analysis
- Decision Tree Classifier (max_depth=5)
- Confusion Matrix Visualization
- Detailed Rule Extraction (IF-THEN)
- Rule Coverage Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, export_text, _tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import os

# Paths
DATA_PATH = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\clustered_data_enhanced.csv'
OUTPUT_DIR = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling'

def load_data():
    """Load and prepare data"""
    print("="*60)
    print("OPTION B: ENHANCED DECISION RULES ANALYSIS")
    print("="*60)
    
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} households")
    
    exclude_cols = ['Cluster', 'Max_Prob', 'Month', 'Year', 'Date', 'Postal outcode', 
                    'Functional area', 'County', 'Latitude', 'Longitude']
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [c for c in numeric_cols if c not in exclude_cols]
    
    X = df[feature_cols].fillna(0)
    y = df['Cluster']
    
    return df, X, y, feature_cols

def train_decision_tree(X, y):
    """Train Decision Tree"""
    print("\n--- Training Decision Tree ---")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    dt = DecisionTreeClassifier(max_depth=4, min_samples_leaf=50, random_state=42)
    dt.fit(X_train, y_train)
    
    y_pred = dt.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Decision Tree Accuracy: {acc:.2%}")
    
    return dt, X_test, y_test, y_pred

def plot_confusion_matrix(y_test, y_pred):
    """Generate and save confusion matrix"""
    print("\n--- Generating Confusion Matrix ---")
    
    cm = confusion_matrix(y_test, y_pred)
    cluster_names = ['Moderate (C0)', 'Profligate (C1)', 'Conservers (C2)']
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=cluster_names, yticklabels=cluster_names)
    plt.xlabel('Predicted Cluster')
    plt.ylabel('True Cluster')
    plt.title('Decision Tree Confusion Matrix')
    plt.tight_layout()
    
    plt.savefig(os.path.join(OUTPUT_DIR, 'decision_tree_confusion_matrix.png'), dpi=150)
    plt.close()
    print("  Saved: decision_tree_confusion_matrix.png")
    
    # Save classification report
    report = classification_report(y_test, y_pred, target_names=cluster_names, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_df.to_csv(os.path.join(OUTPUT_DIR, 'decision_tree_metrics.csv'))
    print("  Saved: decision_tree_metrics.csv")

def extract_rules(tree, feature_names, class_names):
    """Extract rules from decision tree"""
    print("\n--- Extracting Rules ---")
    
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    
    rules = []
    
    def recurse(node, depth, path_str):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            
            # Left child (<= threshold)
            recurse(tree_.children_left[node], depth + 1, path_str + [f"{name} <= {threshold:.2f}"])
            
            # Right child (> threshold)
            recurse(tree_.children_right[node], depth + 1, path_str + [f"{name} > {threshold:.2f}"])
        else:
            # Leaf node
            class_idx = np.argmax(tree_.value[node])
            class_name = class_names[class_idx]
            samples = tree_.n_node_samples[node]
            purity = tree_.value[node][0][class_idx] / samples
            
            rules.append({
                'Class': class_name,
                'Class_Idx': class_idx,
                'Confidence': purity,
                'Samples': samples,
                'Conditions': path_str
            })
    
    recurse(0, 1, [])
    
    # Sort rules by samples (coverage)
    rules.sort(key=lambda x: x['Samples'], reverse=True)
    
    return rules

def save_rules(rules, total_samples):
    """Save rules to text file and CSV"""
    print("\n--- Saving Rules ---")
    
    output_txt = os.path.join(OUTPUT_DIR, 'decision_tree_rules_enhanced.txt')
    output_csv = os.path.join(OUTPUT_DIR, 'decision_tree_rules_coverage.csv')
    
    # Save text format
    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write("ENHANCED DECISION TREE RULES\n")
        f.write("============================\n\n")
        
        for i, rule in enumerate(rules, 1):
            coverage = (rule['Samples'] / total_samples) * 100
            f.write(f"RULE {i}: Predict {rule['Class']}\n")
            f.write(f"  Confidence: {rule['Confidence']:.1%}\n")
            f.write(f"  Coverage: {rule['Samples']} samples ({coverage:.1f}%)\n")
            f.write("  IF:\n")
            for cond in rule['Conditions']:
                f.write(f"    AND {cond}\n")
            f.write("\n")
            
    print(f"  Saved: decision_tree_rules_enhanced.txt")
    
    # Save CSV format
    csv_data = []
    for i, rule in enumerate(rules, 1):
        csv_data.append({
            'Rule_ID': i,
            'Predicted_Class': rule['Class'],
            'Confidence': rule['Confidence'],
            'Samples': rule['Samples'],
            'Coverage_Pct': (rule['Samples'] / total_samples) * 100,
            'Conditions': " AND ".join(rule['Conditions'])
        })
    
    pd.DataFrame(csv_data).to_csv(output_csv, index=False)
    print(f"  Saved: decision_tree_rules_coverage.csv")

def main():
    df, X, y, feature_names = load_data()
    
    dt, X_test, y_test, y_pred = train_decision_tree(X, y)
    
    plot_confusion_matrix(y_test, y_pred)
    
    class_names = ['Moderate (C0)', 'Profligate (C1)', 'Conservers (C2)']
    rules = extract_rules(dt, feature_names, class_names)
    
    # Calculate total samples in training set (approx)
    total_samples = len(y) * 0.8
    save_rules(rules, total_samples)
    
    print("\n" + "="*60)
    print("OPTION B: DECISION RULES ANALYSIS - COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
