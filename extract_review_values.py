"""
Extract Actual Values for Second Review Fixes
1. BIC/AIC comparison values
2. SHAP surrogate model confusion matrix
3. Cluster assignment probabilities
"""

import pandas as pd
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path

data_dir = Path(r"c:\Users\moham\Desktop\New folder\profiling\data_science_profiling")

print("="*70)
print("EXTRACTING VALUES FOR SECOND REVIEW")
print("="*70)

# Load data
df = pd.read_csv(data_dir / 'clustered_data_enhanced.csv')
W = pd.read_csv(data_dir / 'nmf_W_matrix_enhanced.csv', index_col=0)
print(f"Loaded {len(df)} households")

# =============================================================================
# 1. BIC/AIC COMPARISON
# =============================================================================
print("\n" + "="*70)
print("1. BIC vs AIC COMPARISON (K=1 to 10)")
print("="*70)

X = W.values
results = []

for k in range(1, 11):
    gmm = GaussianMixture(n_components=k, random_state=42, n_init=3)
    gmm.fit(X)
    results.append({
        'K': k,
        'BIC': gmm.bic(X),
        'AIC': gmm.aic(X)
    })
    print(f"K={k}: BIC={gmm.bic(X):.0f}, AIC={gmm.aic(X):.0f}")

results_df = pd.DataFrame(results)

# Find optimal K
bic_optimal = results_df.loc[results_df['BIC'].idxmin()]
aic_optimal = results_df.loc[results_df['AIC'].idxmin()]

print(f"\n✅ BIC optimal: K={int(bic_optimal['K'])} (BIC={bic_optimal['BIC']:.0f})")
print(f"✅ AIC optimal: K={int(aic_optimal['K'])} (AIC={aic_optimal['AIC']:.0f})")

if bic_optimal['K'] == aic_optimal['K']:
    print("✅ Both criteria converge on same K")
else:
    print(f"⚠️ Criteria differ: BIC selects K={int(bic_optimal['K'])}, AIC selects K={int(aic_optimal['K'])}")

# Save for reference
results_df.to_csv(data_dir / 'bic_aic_comparison.csv', index=False)

# =============================================================================
# 2. SHAP SURROGATE MODEL VALIDATION
# =============================================================================
print("\n" + "="*70)
print("2. SHAP SURROGATE MODEL (XGBoost) VALIDATION")
print("="*70)

# Prepare features
exclude_cols = ['Cluster', 'Max_Prob']
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
feature_cols = [c for c in numeric_cols if c not in exclude_cols]

X_features = df[feature_cols].fillna(0)
y = df['Cluster']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_features, y, test_size=0.2, random_state=42, stratify=y)

# Train XGBoost (using GradientBoosting as similar)
from sklearn.ensemble import GradientBoostingClassifier
clf = GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# Cross-validation
cv_scores = cross_val_score(clf, X_features, y, cv=5)
print(f"\n5-Fold CV Accuracy: {cv_scores.mean():.3f} (SD={cv_scores.std():.3f})")
print(f"95% CI: [{cv_scores.mean() - 1.96*cv_scores.std():.3f}, {cv_scores.mean() + 1.96*cv_scores.std():.3f}]")

# Test set predictions
y_pred = clf.predict(X_test)

# Classification report
print("\nClassification Report (Test Set):")
print(classification_report(y_test, y_pred, target_names=['C0 (Moderate)', 'C1 (High-Intensity)', 'C2 (Conservers)']))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(f"            Predicted")
print(f"            C0    C1    C2")
print(f"Actual C0  {cm[0,0]:4d}  {cm[0,1]:4d}  {cm[0,2]:4d}")
print(f"       C1  {cm[1,0]:4d}  {cm[1,1]:4d}  {cm[1,2]:4d}")
print(f"       C2  {cm[2,0]:4d}  {cm[2,1]:4d}  {cm[2,2]:4d}")

# =============================================================================
# 3. CLUSTER ASSIGNMENT CONFIDENCE
# =============================================================================
print("\n" + "="*70)
print("3. CLUSTER ASSIGNMENT CONFIDENCE (GMM Probabilities)")
print("="*70)

if 'Max_Prob' in df.columns:
    max_probs = df['Max_Prob']
    
    print(f"\nAssignment Probability Statistics:")
    print(f"  Mean: {max_probs.mean():.3f}")
    print(f"  SD: {max_probs.std():.3f}")
    print(f"  Median: {max_probs.median():.3f}")
    print(f"  Min: {max_probs.min():.3f}")
    print(f"  Max: {max_probs.max():.3f}")
    
    # Confidence categories
    high_conf = (max_probs > 0.85).mean() * 100
    mod_conf = ((max_probs >= 0.70) & (max_probs <= 0.85)).mean() * 100
    low_conf = (max_probs < 0.70).mean() * 100
    
    print(f"\nConfidence Distribution:")
    print(f"  High (>0.85): {high_conf:.1f}%")
    print(f"  Moderate (0.70-0.85): {mod_conf:.1f}%")
    print(f"  Low (<0.70): {low_conf:.1f}%")
else:
    print("Max_Prob column not found - need to recalculate GMM")

# =============================================================================
# 4. CLUSTER-SPECIFIC METRICS
# =============================================================================
print("\n" + "="*70)
print("4. CLUSTER-SPECIFIC PERFORMANCE")
print("="*70)

for cluster_id in [0, 1, 2]:
    cluster_mask = y_test == cluster_id
    pred_mask = y_pred == cluster_id
    
    tp = ((y_test == cluster_id) & (y_pred == cluster_id)).sum()
    fp = ((y_test != cluster_id) & (y_pred == cluster_id)).sum()
    fn = ((y_test == cluster_id) & (y_pred != cluster_id)).sum()
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    print(f"\nC{cluster_id}: Precision={precision:.2f}, Recall={recall:.2f}, F1={f1:.2f}")

print("\n" + "="*70)
print("EXTRACTION COMPLETE")
print("="*70)
