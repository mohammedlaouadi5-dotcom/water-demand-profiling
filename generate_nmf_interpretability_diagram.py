"""
Generate NMF vs PCA Interpretability Comparison Diagram
Per reviewer request: Demonstrate why NMF components are additive and interpretable
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
import numpy as np

plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'

data_dir = Path(r"c:\Users\moham\Desktop\New folder\profiling\data_science_profiling")

print("="*60)
print("GENERATING NMF vs PCA INTERPRETABILITY DIAGRAM")
print("="*60)

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

# =============================================================================
# PANEL A: PCA COMPONENTS
# =============================================================================
ax = axes[0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Panel A: PCA Components\n(Orthogonal, can be negative)', fontsize=12, fontweight='bold')

# Component 1
ax.add_patch(FancyBboxPatch((0.5, 7), 9, 1.5, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#e74c3c', alpha=0.7, edgecolor='white', linewidth=2))
ax.text(5, 7.75, 'PC1 = +0.5×Showers - 0.3×Baths + 0.2×Garden', 
        ha='center', va='center', fontsize=9, color='white', fontweight='bold')

# Component 2
ax.add_patch(FancyBboxPatch((0.5, 5), 9, 1.5, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#e74c3c', alpha=0.7, edgecolor='white', linewidth=2))
ax.text(5, 5.75, 'PC2 = -0.4×Showers + 0.6×Baths - 0.1×Leaks', 
        ha='center', va='center', fontsize=9, color='white', fontweight='bold')

# Issues
ax.add_patch(FancyBboxPatch((0.5, 1.5), 9, 2.5, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#f5f5f5', alpha=0.9, edgecolor='#e74c3c', linewidth=2))
ax.text(5, 3, '⚠️ Interpretation Issues:', ha='center', va='center', fontsize=10, fontweight='bold', color='#e74c3c')
ax.text(5, 2.4, '• Negative loadings: "High showers MINUS baths"', ha='center', va='center', fontsize=8)
ax.text(5, 1.9, '• Difficult to explain as behavioral patterns', ha='center', va='center', fontsize=8)

# =============================================================================
# PANEL B: NMF COMPONENTS
# =============================================================================
ax = axes[1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Panel B: NMF Components\n(Non-negative, additive parts)', fontsize=12, fontweight='bold')

# Component 1
ax.add_patch(FancyBboxPatch((0.5, 7), 9, 1.5, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#2ecc71', alpha=0.7, edgecolor='white', linewidth=2))
ax.text(5, 7.75, 'H1 = +0.7×Showers + 0.4×Baths + 0.0×Garden', 
        ha='center', va='center', fontsize=9, color='white', fontweight='bold')
ax.text(5, 7.2, '"Indoor Bathing Intensity"', ha='center', va='center', fontsize=8, color='white', style='italic')

# Component 2
ax.add_patch(FancyBboxPatch((0.5, 5), 9, 1.5, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#2ecc71', alpha=0.7, edgecolor='white', linewidth=2))
ax.text(5, 5.75, 'H2 = +0.0×Showers + 0.0×Baths + 0.6×Leaks', 
        ha='center', va='center', fontsize=9, color='white', fontweight='bold')
ax.text(5, 5.2, '"Infrastructure Quality"', ha='center', va='center', fontsize=8, color='white', style='italic')

# Benefits
ax.add_patch(FancyBboxPatch((0.5, 1.5), 9, 2.5, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#e8f8f5', alpha=0.9, edgecolor='#2ecc71', linewidth=2))
ax.text(5, 3, '✓ Interpretation Benefits:', ha='center', va='center', fontsize=10, fontweight='bold', color='#27ae60')
ax.text(5, 2.4, '• All loadings ≥ 0: No subtraction needed', ha='center', va='center', fontsize=8)
ax.text(5, 1.9, '• Intuitive "behavioral pattern" interpretation', ha='center', va='center', fontsize=8)

# =============================================================================
# PANEL C: HOUSEHOLD REPRESENTATION
# =============================================================================
ax = axes[2]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Panel C: Household Representation\n(Additive combination)', fontsize=12, fontweight='bold')

# Equation
ax.add_patch(FancyBboxPatch((0.5, 7), 9, 2, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#3498db', alpha=0.7, edgecolor='white', linewidth=2))
ax.text(5, 8, 'Household i = w₁ × H₁ + w₂ × H₂', 
        ha='center', va='center', fontsize=11, color='white', fontweight='bold')
ax.text(5, 7.3, '(Purely additive: no negative weights)', 
        ha='center', va='center', fontsize=9, color='white')

# Example
ax.add_patch(FancyBboxPatch((0.5, 4), 9, 2.5, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#f0f8ff', alpha=0.9, edgecolor='#3498db', linewidth=2))
ax.text(5, 5.8, 'Example: High-Intensity Household', ha='center', va='center', fontsize=10, fontweight='bold', color='#2980b9')
ax.text(5, 5.1, 'w₁ = 0.9 (high indoor intensity)', ha='center', va='center', fontsize=9)
ax.text(5, 4.5, 'w₂ = 0.7 (poor infrastructure)', ha='center', va='center', fontsize=9)

# Arrow to interpretation
ax.annotate('', xy=(5, 1.8), xytext=(5, 3.8),
            arrowprops=dict(arrowstyle='->', color='#3498db', lw=2))

# Interpretation
ax.add_patch(FancyBboxPatch((0.5, 0.5), 9, 1.5, boxstyle="round,pad=0.03,rounding_size=0.2",
                            facecolor='#9b59b6', alpha=0.7, edgecolor='white', linewidth=2))
ax.text(5, 1.25, '→ Intervention: Target behavior + fix leaks', 
        ha='center', va='center', fontsize=10, color='white', fontweight='bold')

plt.suptitle('NMF vs PCA: Why Non-Negative Matrix Factorization Enhances Interpretability',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(data_dir / 'Figure_NMF_vs_PCA_Interpretability.png', dpi=300, bbox_inches='tight')
plt.savefig(data_dir / 'Figure_NMF_vs_PCA_Interpretability.pdf', bbox_inches='tight')
print("✓ Saved: Figure_NMF_vs_PCA_Interpretability.png/.pdf")
plt.close()

print("\n" + "="*60)
print("DIAGRAM COMPLETE")
print("="*60)
