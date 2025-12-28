"""
Generate Analytical Pipeline Overview Figure
Per academic review recommendation for Methods section
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path
import numpy as np

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'

data_dir = Path(r"c:\Users\moham\Desktop\New folder\profiling\data_science_profiling")

print("="*60)
print("GENERATING ANALYTICAL PIPELINE FIGURE")
print("="*60)

# Create figure
fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Define box style
box_style = "round,pad=0.03,rounding_size=0.2"

# Color scheme
colors = {
    'data': '#3498db',      # Blue - Data
    'preprocess': '#9b59b6', # Purple - Preprocessing
    'feature': '#e74c3c',    # Red - Feature Selection
    'reduce': '#f39c12',     # Orange - Dimensionality
    'cluster': '#2ecc71',    # Green - Clustering
    'validate': '#1abc9c',   # Teal - Validation
    'xai': '#e91e63',        # Pink - XAI
    'output': '#34495e'      # Dark - Output
}

# Define boxes (x, y, width, height, label, sublabel, color)
boxes = [
    # Row 1: Data Input
    (1, 8.5, 5, 0.8, "Survey + Meter Data", "N=13,061 households, 97 features", colors['data']),
    (7, 8.5, 5, 0.8, "Preprocessing Module", "KNN imputation, consistency corrections", colors['preprocess']),
    
    # Row 2: Feature Engineering
    (1, 6.5, 5, 0.8, "MAD-Bootstrap Feature Selection", "Stability threshold > 0.5, 100 iterations", colors['feature']),
    (7, 6.5, 5, 0.8, "Correlation Filtering", "Remove |r| > 0.85, retain 18 features", colors['feature']),
    
    # Row 3: Modeling
    (1, 4.5, 5, 0.8, "NMF Dimensionality Reduction", "K=2 components (60.5% variance)", colors['reduce']),
    (7, 4.5, 5, 0.8, "GMM Clustering", "K=3 clusters (BIC optimized)", colors['cluster']),
    
    # Row 4: Validation
    (1, 2.5, 5, 0.8, "Internal Validation", "Silhouette, CH, Davies-Bouldin", colors['validate']),
    (7, 2.5, 5, 0.8, "Monte Carlo Stability", "ARI = 0.981 (100 bootstraps)", colors['validate']),
    
    # Row 5: XAI & Output
    (1, 0.5, 5, 0.8, "XAI Explainability Module", "SHAP values + Decision Tree rules", colors['xai']),
    (7, 0.5, 5, 0.8, "Intervention Design", "Counterfactual analysis, KOGAMI", colors['output']),
]

# Draw boxes
for (x, y, w, h, label, sublabel, color) in boxes:
    # Main box
    box = FancyBboxPatch((x, y), w, h, 
                         boxstyle=box_style,
                         facecolor=color, 
                         edgecolor='white',
                         linewidth=2,
                         alpha=0.9)
    ax.add_patch(box)
    
    # Main label
    ax.text(x + w/2, y + h/2 + 0.15, label, 
            ha='center', va='center', 
            fontsize=9, fontweight='bold', color='white')
    
    # Sublabel
    ax.text(x + w/2, y + h/2 - 0.2, sublabel, 
            ha='center', va='center', 
            fontsize=7, color='white', alpha=0.9)

# Draw arrows
arrow_style = "Simple,tail_width=0.5,head_width=4,head_length=6"
kw = dict(arrowstyle=arrow_style, color='#2c3e50', lw=2)

# Horizontal arrows (same row)
arrows_h = [
    (6, 8.9),    # Data -> Preprocess
    (6, 6.9),    # MAD -> Correlation
    (6, 4.9),    # NMF -> GMM
    (6, 2.9),    # Internal -> Monte Carlo
    (6, 0.9),    # XAI -> Intervention
]

for (x, y) in arrows_h:
    ax.annotate('', xy=(x+1, y), xytext=(x, y),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=2))

# Vertical arrows (between rows)
arrows_v = [
    (3.5, 8.5, 3.5, 7.3),    # Preprocess -> MAD
    (9.5, 8.5, 9.5, 7.3),    # (hidden, just for alignment)
    (3.5, 6.5, 3.5, 5.3),    # Correlation -> NMF
    (9.5, 6.5, 9.5, 5.3),    # -> GMM
    (3.5, 4.5, 3.5, 3.3),    # NMF -> Internal
    (9.5, 4.5, 9.5, 3.3),    # GMM -> Monte Carlo
    (3.5, 2.5, 3.5, 1.3),    # Internal -> XAI
    (9.5, 2.5, 9.5, 1.3),    # Monte Carlo -> Intervention
]

for (x1, y1, x2, y2) in arrows_v:
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=2))

# Add section labels on left
sections = [
    (0.3, 8.9, "1. Data"),
    (0.3, 6.9, "2. Features"),
    (0.3, 4.9, "3. Modeling"),
    (0.3, 2.9, "4. Validation"),
    (0.3, 0.9, "5. Output"),
]

for (x, y, label) in sections:
    ax.text(x, y, label, ha='left', va='center', 
            fontsize=10, fontweight='bold', color='#2c3e50',
            rotation=0)

# Title
ax.text(7, 10.2, "Figure 6: XClustering Analytical Pipeline", 
        ha='center', va='center', fontsize=14, fontweight='bold')
ax.text(7, 9.8, "Survey-Informed Water Demand Behavioral Profiling Framework", 
        ha='center', va='center', fontsize=11, color='#7f8c8d')

# Legend
legend_elements = [
    mpatches.Patch(facecolor=colors['data'], label='Data Input'),
    mpatches.Patch(facecolor=colors['preprocess'], label='Preprocessing'),
    mpatches.Patch(facecolor=colors['feature'], label='Feature Engineering'),
    mpatches.Patch(facecolor=colors['reduce'], label='Dimensionality Reduction'),
    mpatches.Patch(facecolor=colors['cluster'], label='Clustering'),
    mpatches.Patch(facecolor=colors['validate'], label='Validation'),
    mpatches.Patch(facecolor=colors['xai'], label='Explainability'),
    mpatches.Patch(facecolor=colors['output'], label='Application'),
]

ax.legend(handles=legend_elements, loc='lower center', 
          ncol=4, fontsize=8, frameon=True,
          bbox_to_anchor=(0.5, -0.08))

plt.tight_layout()
plt.savefig(data_dir / 'Figure6_Analytical_Pipeline.png', dpi=300, bbox_inches='tight')
plt.savefig(data_dir / 'Figure6_Analytical_Pipeline.pdf', bbox_inches='tight')
print("✓ Saved: Figure6_Analytical_Pipeline.png/.pdf")
plt.close()

print("\n" + "="*60)
print("PIPELINE FIGURE COMPLETE")
print("="*60)
