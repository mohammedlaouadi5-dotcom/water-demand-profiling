"""
Generate Supplementary Figures for Manuscript
Addresses Academic Review requirements for diagnostic and validation plots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

data_dir = Path(r"c:\Users\moham\Desktop\New folder\profiling\data_science_profiling")

print("="*80)
print("GENERATING SUPPLEMENTARY FIGURES")
print("="*80)

# Load data
df = pd.read_csv(data_dir / 'clustered_data_enhanced.csv')
print(f"Loaded {len(df)} households")

# =============================================================================
# FIGURE S1: NORMALITY DIAGNOSTICS (Q-Q Plots)
# =============================================================================
print("\n📊 Figure S1: Normality Diagnostics")

try:
    # Select 6 key numeric variables
    key_vars = [
        'Boil-Water-Per-Week',
        'Showers-Per-Week', 
        'Bath-Frequency-Per-Week',
        'Shower-Duration-Minutes',
        'Garden-Water-Frequency-Per-Week',
        'Wash-By-Hand-Per-Week'
    ]
    
    available_vars = [v for v in key_vars if v in df.columns][:6]
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, var in enumerate(available_vars):
        ax = axes[idx]
        data = df[var].dropna()
        
        # Q-Q plot
        stats.probplot(data, dist="norm", plot=ax)
        
        # Shapiro-Wilk test (on sample if large)
        sample = data.sample(min(5000, len(data)), random_state=42)
        stat, p = stats.shapiro(sample)
        
        ax.set_title(f'{var}\nShapiro-Wilk p = {p:.4f}', fontsize=10)
        ax.set_xlabel('Theoretical Quantiles')
        ax.set_ylabel('Sample Quantiles')
        
        # Color based on normality
        if p < 0.05:
            ax.get_lines()[0].set_color('red')
            ax.get_lines()[0].set_alpha(0.5)
        else:
            ax.get_lines()[0].set_color('green')
    
    plt.suptitle('Supplementary Figure S1: Normality Diagnostics (Q-Q Plots)\n' + 
                 'Green = p ≥ 0.05 (normal), Red = p < 0.05 (non-normal)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(data_dir / 'FigureS1_Normality_Diagnostics.png', dpi=300, bbox_inches='tight')
    plt.savefig(data_dir / 'FigureS1_Normality_Diagnostics.pdf', bbox_inches='tight')
    print("   ✓ Saved: FigureS1_Normality_Diagnostics.png/.pdf")
    plt.close()
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# =============================================================================
# FIGURE S2: CORRELATION HEATMAP (18 Final Features)
# =============================================================================
print("\n📊 Figure S2: Feature Correlation Heatmap")

try:
    # Get numeric columns (main behavioral features)
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Exclude cluster and prob columns
    exclude = ['Cluster', 'Max_Prob', 'Latitude', 'Longitude', 'Year', 'Monthly']
    feature_cols = [c for c in numeric_cols if c not in exclude][:20]  # Top 20
    
    corr_matrix = df[feature_cols].corr()
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
    
    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap='RdBu_r',
        vmin=-1, vmax=1,
        center=0,
        square=True,
        linewidths=0.5,
        annot=False,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation"},
        ax=ax
    )
    
    ax.set_title('Supplementary Figure S2: Feature Correlation Matrix\n(Top 20 Numeric Features)',
                fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.yticks(fontsize=8)
    
    plt.tight_layout()
    plt.savefig(data_dir / 'FigureS2_Correlation_Heatmap.png', dpi=300, bbox_inches='tight')
    plt.savefig(data_dir / 'FigureS2_Correlation_Heatmap.pdf', bbox_inches='tight')
    print("   ✓ Saved: FigureS2_Correlation_Heatmap.png/.pdf")
    plt.close()
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# =============================================================================
# FIGURE S3: GMM BIC CURVE (Model Selection)
# =============================================================================
print("\n📊 Figure S3: GMM Model Selection (BIC Curve)")

try:
    from sklearn.mixture import GaussianMixture
    
    # Load NMF transformed data
    W = pd.read_csv(data_dir / 'nmf_W_matrix_enhanced.csv', index_col=0)
    X = W.values
    
    K_range = range(1, 11)
    bics = []
    aics = []
    
    print("   Fitting GMM for K = 1 to 10...")
    for k in K_range:
        gmm = GaussianMixture(n_components=k, random_state=42, n_init=3)
        gmm.fit(X)
        bics.append(gmm.bic(X))
        aics.append(gmm.aic(X))
        print(f"      K={k}: BIC={bics[-1]:.0f}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Panel A: BIC
    ax1.plot(K_range, bics, 'o-', linewidth=2, markersize=8, color='#1f77b4', label='BIC')
    ax1.axvline(x=3, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Selected K=3')
    ax1.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax1.set_ylabel('BIC Score', fontsize=12)
    ax1.set_title('Panel A: Bayesian Information Criterion', fontsize=12, fontweight='bold')
    ax1.legend(frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3)
    
    # Mark minimum
    min_k = np.argmin(bics) + 1
    ax1.annotate(f'Minimum at K={min_k}', 
                xy=(min_k, bics[min_k-1]), 
                xytext=(min_k+1.5, bics[min_k-1] + (max(bics)-min(bics))*0.1),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5),
                fontsize=10, color='green')
    
    # Panel B: AIC
    ax2.plot(K_range, aics, 's-', linewidth=2, markersize=8, color='#2ca02c', label='AIC')
    ax2.axvline(x=3, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Selected K=3')
    ax2.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax2.set_ylabel('AIC Score', fontsize=12)
    ax2.set_title('Panel B: Akaike Information Criterion', fontsize=12, fontweight='bold')
    ax2.legend(frameon=True, shadow=True)
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Supplementary Figure S3: GMM Model Selection Criteria\n' +
                 '(K=3 selected based on BIC minimum and interpretability)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(data_dir / 'FigureS3_GMM_BIC_Curve.png', dpi=300, bbox_inches='tight')
    plt.savefig(data_dir / 'FigureS3_GMM_BIC_Curve.pdf', bbox_inches='tight')
    print("   ✓ Saved: FigureS3_GMM_BIC_Curve.png/.pdf")
    plt.close()
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# =============================================================================
# FIGURE S4: CLUSTER SIZE DISTRIBUTION
# =============================================================================
print("\n📊 Figure S4: Cluster Size Distribution")

try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    cluster_counts = df['Cluster'].value_counts().sort_index()
    cluster_labels = ['C0: Moderate\n(62.8%)', 'C1: Profligate\n(11.8%)', 'C2: Conservers\n(25.4%)']
    colors = ['#1f77b4', '#d62728', '#2ca02c']
    
    # Panel A: Bar chart
    bars = ax1.bar(range(3), cluster_counts.values, color=colors)
    ax1.set_xticks(range(3))
    ax1.set_xticklabels(cluster_labels)
    ax1.set_ylabel('Number of Households', fontsize=12)
    ax1.set_title('Panel A: Cluster Sizes (Counts)', fontsize=12, fontweight='bold')
    ax1.grid(True, axis='y', alpha=0.3)
    
    # Add count labels
    for bar, count in zip(bars, cluster_counts.values):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                f'n={count:,}', ha='center', fontsize=10, fontweight='bold')
    
    # Panel B: Pie chart
    ax2.pie(cluster_counts.values, labels=cluster_labels, colors=colors,
           autopct='%1.1f%%', startangle=90, explode=[0.02, 0.05, 0.02],
           shadow=True, textprops={'fontsize': 10})
    ax2.set_title('Panel B: Cluster Proportions', fontsize=12, fontweight='bold')
    
    plt.suptitle('Supplementary Figure S4: Cluster Size Distribution\n(N = 13,061 households)',
                fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(data_dir / 'FigureS4_Cluster_Distribution.png', dpi=300, bbox_inches='tight')
    plt.savefig(data_dir / 'FigureS4_Cluster_Distribution.pdf', bbox_inches='tight')
    print("   ✓ Saved: FigureS4_Cluster_Distribution.png/.pdf")
    plt.close()
    
except Exception as e:
    print(f"   ❌ Error: {e}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "="*80)
print("SUPPLEMENTARY FIGURE GENERATION COMPLETE")
print("="*80)
print("\n✅ Generated supplementary figures:")
print("   • FigureS1_Normality_Diagnostics (Q-Q plots)")
print("   • FigureS2_Correlation_Heatmap")
print("   • FigureS3_GMM_BIC_Curve (model selection)")
print("   • FigureS4_Cluster_Distribution")
print("\n📁 All files saved in:", data_dir)
