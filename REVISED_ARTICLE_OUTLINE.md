# REVISED ARTICLE OUTLINE
## Survey-Informed Water Demand Behavioral Profiling: A Robust Machine Learning Framework with Explainable AI

**Target Journal**: Water Research (Q1, IF: 12.8)
**Word Count Target**: 8,000-10,000 (main text)

---

# TITLE PAGE

**Title**: Survey-Informed Water Demand Behavioral Profiling: A Robust Machine Learning Framework with Explainable AI for Targeted Intervention Design

**Running Title**: XAI-Enabled Water Demand Behavioral Profiling

**Keywords**: Water scarcity; demand-side management; behavioral segmentation; explainable artificial intelligence (XAI); Gaussian mixture models; smart metering; residential water conservation

---

# HIGHLIGHTS (5 bullets, ≤85 characters each)

1. MAD-Bootstrap feature selection achieves 98.1% stability in behavioral profiling
2. Three distinct water demand clusters identified from 13,061 UK households
3. SHAP and Decision Tree rules enable interpretable intervention targeting
4. 64% of high-consumption households show transition potential via behavior change
5. Framework validated with Monte Carlo showing superior robustness to prior methods

---

# GRAPHICAL ABSTRACT
[Figure 6: Analytical Pipeline - already generated]

---

# ABSTRACT (250-300 words)

**Background**: [Current text - update cluster percentages]

**Methods**: [Current text - add MAD-Bootstrap, NMF, GMM, XAI]

**Results**: Three behaviorally distinct clusters emerged:
- **Moderate Standard Users (62.8%, n=8,198)**: Typical residential consumption patterns
- **Low-Intensity Conservers (25.4%, n=3,318)**: Smaller households, elevated eco-scores
- **High-Intensity Profligate (11.8%, n=1,545)**: Highest per-capita consumption, elevated leak rates

All cluster differences achieved statistical significance (p < 0.001) with very large effect sizes (79% of variables with η² ≥ 0.14).

**Conclusions**: [Current text]

**Policy Significance**: This framework enables water utilities to transition from universal awareness campaigns to targeted intervention design, with projected cost reductions of 61% compared to untargeted programs.

---

# 1. INTRODUCTION (1,500-2,000 words)

## 1.1 Background and Motivation
- Global water scarcity context
- UK water demand challenges
- Need for demand-side management
- Role of behavioral profiling in utility operations

## 1.2 Problem Statement
- Limitations of volumetric-only segmentation
- Gap between research prototypes and utility deployment
- Need for interpretable, robust methods

## 1.3 Literature Review

### 1.3.1 Traditional Water Demand Modeling
- Engineering approaches (Willis et al., 2011; Stewart et al., 2010)
- End-use disaggregation (Nguyen et al., 2015; Cominola et al., 2015)

### 1.3.2 Machine Learning Approaches
- Clustering methods (K-means, SOM, Hierarchical)
- Deep learning for demand prediction
- Limitations: interpretability, stability

### 1.3.3 XAI in Water Sector (NEW)
- Post-2022 XAI adoption (SHAP, LIME)
- Trust and accountability in utility operations
- Gap: No integrated XAI + robust clustering framework

### 1.3.4 Recent Advances (2020-2024) (NEW)
- Heydari & Stillwell (2024): ML comparison under class imbalance
- Pradeep & Bakeev (2024): XGBoost vs TabNet for XAI
- Pavlou & Polycarpou (2024): Edge deployment considerations
- Mazzoni & Franchini (2024): Cross-country validation
- Pelekanos & Makropoulos (2025): K-means + probabilistic approach
- **Gap**: Survey-informed profiling with bootstrap stability + XAI remains unexplored

### 1.3.5 Methodological Synthesis Need (NEW)
- Explicit statement of why integrating robustness, stability, and explainability is novel
- Positioning this work as synthesis rather than claiming 100% novelty

## 1.4 Research Gap
- No existing work combines: (1) survey-informed features, (2) bootstrap-stable feature selection, (3) probabilistic clustering, (4) XAI transparency
- "To our knowledge" framing for novelty claims

## 1.5 Research Objectives
1. Develop robust feature selection via MAD-Bootstrap stability
2. Create interpretable behavioral clusters using NMF + GMM
3. Provide actionable XAI explanations (SHAP + rules)
4. Validate framework robustness via Monte Carlo

## 1.6 Paper Structure
- Brief roadmap of sections

---

# 2. METHODS (3,000-3,500 words)

## 2.1 Study Area and Data Collection
- Yorkshire Water service region (Northern England)
- Survey instrument: 97 behavioral questions
- Smart meter integration: Annual consumption
- Sample: N = 13,061 households (after quality filtering)
- Temporal coverage: 2018-2020

**[Include Figure 6: Analytical Pipeline]**

## 2.2 Data Quality Assessment
- Completeness analysis: X% complete cases
- Missing data patterns: MCAR/MAR assessment
- Exclusion criteria: Response quality thresholds

## 2.3 Data Preprocessing

### 2.3.1 Categorical Variable Imputation (NEW)
- **Mode imputation** for missingness ≤5%
- **Factorized KNN** for missingness >5%:
  - Integer-encode categorical values
  - KNN (K=5) on standardized features
  - Round and decode imputed values
- **Limitation**: MICE recommended for future work

### 2.3.2 Numeric Variable Preprocessing
- Median imputation for continuous variables
- IQR outlier detection (1.5 × IQR rule; Tukey, 1977)
- Min-max normalization [0, 1]

### 2.3.3 Consistency Corrections
- Logical constraints: Appliance="No" → Usage=0
- Leak rate imputation: Leak="Yes" ∧ Rate=NaN → Rate="slowly"
  - Justification: 73% of household leaks are slow drips (WaterUK, 2018)
  - Sensitivity analysis: ARI = 0.97 with alternative imputation

## 2.4 Feature Selection: MAD-Bootstrap Stability

### 2.4.1 Rationale
- Traditional variance/univariate filters susceptible to sampling variability
- Bootstrap addresses instability (Meinshausen & Bühlmann, 2010)
- MAD robust to outliers vs. mean-based methods

### 2.4.2 Algorithm
```
For b = 1 to 100 (bootstrap iterations):
    1. Resample N with replacement
    2. Compute MAD for each feature
    3. Record features with MAD > 0.01
Selection: Features stable in >50% of iterations
```

### 2.4.3 Binary Feature Handling (NEW)
- Minimum prevalence filter (2%) for sparse OHE features
- Bootstrap selection frequency alternative for binary indicators
- Post-hoc SHAP verification: No high-importance features excluded

### 2.4.4 Multicollinearity Filtering
- Pearson correlation threshold: |r| > 0.85 (Dormann et al., 2013)
- 97 → 18 final features retained

## 2.5 Dimensionality Reduction: Non-Negative Matrix Factorization

### 2.5.1 NMF Formulation
- X ≈ W × H (non-negative constraint)
- W: Household loadings (N × K)
- H: Component patterns (K × M)

### 2.5.2 Component Selection
- Reconstruction error analysis (Figure 3)
- K = 2 optimal: RMSE = 0.024, plateau at K > 2
- 60.5% variance explained

### 2.5.3 Interpretability Advantage (NEW)
- Parts-based representation: additive, no negative loadings
- Component 1: "Indoor Bathing Intensity"
- Component 2: "Infrastructure Quality"
- **[Include Figure: NMF vs PCA Interpretability]**

### 2.5.4 Initialization
- NNDSVD initialization (Boutsidis & Gallopoulos, 2008)
- Deterministic for reproducibility
- Stability addressed via GMM Monte Carlo (Section 2.6.1)

## 2.6 Clustering: Gaussian Mixture Models

### 2.6.1 Model Selection
- BIC for cluster number selection (K = 1-10)
- K = 3 optimal (minimum BIC)
- **BIC preference over AIC** (NEW): Stronger complexity penalty appropriate for large N (Kass & Raftery, 1995)

### 2.6.2 GMM Configuration
- Full covariance matrices
- K-means++ initialization
- n_init = 10 for stability
- random_state = 42 for reproducibility

### 2.6.3 Cluster Assignment
- Soft probabilistic assignment
- Max probability for hard labels
- Mean assignment probability: 0.XX (high confidence)

## 2.7 Validation Framework

### 2.7.1 Internal Validation
- Silhouette Score: Cluster separation
- Calinski-Harabasz Index: Cluster density
- Davies-Bouldin Index: Cluster compactness (lower = better)

### 2.7.2 Monte Carlo Stability Analysis
- 100 bootstrap iterations
- Varied GMM seeds (0-99), fixed NMF initialization
- Adjusted Rand Index (ARI) for cluster agreement
- Cluster-specific stability (NEW): Check minority cluster (C1: 11.8%)

### 2.7.3 Statistical Significance
- ANOVA for continuous variables (Welch's correction if needed)
- Chi-square for categorical variables
- Effect sizes: η² (ANOVA), Cramér's V (Chi-square)
- Tukey HSD for pairwise comparisons

### 2.7.4 Power Analysis Acknowledgment (NEW)
- N = 13,061 provides power > 0.999 for small effects
- Emphasis on effect sizes over p-values (Wasserstein & Lazar, 2016)
- Multiple testing: 74 tests, FDR correction applied post-hoc

## 2.8 Explainable AI Framework

### 2.8.1 SHAP Analysis
- **Surrogate model approach** (NEW): XGBoost classifier as GMM proxy
- Proxy accuracy: 98.8% (5-fold CV)
- SHAP values reflect feature importance for cluster boundaries
- Mean |SHAP| for global importance ranking

### 2.8.2 Decision Tree Rules
- Interpretable decision tree (max_depth = 5)
- Rule extraction for utility deployment
- Coverage and precision metrics per cluster

### 2.8.3 Local Explanations
- Waterfall plots for individual households
- Cluster-specific driver identification

## 2.9 Counterfactual Analysis (NEW)

### 2.9.1 Transition Simulation
- Random Forest classifier for cluster prediction
- Target: C1 (High-Intensity) → C2 (Conservers)

### 2.9.2 Intervention Strategy
- **Stage 1**: Infrastructure remediation (leak repair)
- **Stage 2**: Behavioral frequency reduction (5% increments)

### 2.9.3 Cost-Benefit Analysis
| Component | Cost |
|-----------|------|
| Leak repair | £100 |
| Behavioral campaign | £20 |
| Administrative overhead | £48 |
| **Total** | **£168** |
| Annual savings | £151 |
| **Payback period** | **0.5-1.1 years** |

### 2.9.4 Limitations
- Model-based prediction assumptions
- Simplified cost estimates
- Validation with utility-specific data recommended

---

# 3. RESULTS (2,500-3,000 words)

## 3.1 Feature Selection Outcomes
- 97 → 18 features retained
- Stability score distribution (Figure X)
- Top 10 stable features by MAD score
- **[Table 1: Final Feature Set]**

## 3.2 NMF Representation
- Component loadings interpretation
- Variance explained: 60.5%
- **[Figure 3: NMF Component Selection]**

## 3.3 Cluster Characterization

### 3.3.1 Cluster Overview
| Cluster | Label | N | % | Key Characteristics |
|---------|-------|---|---|---------------------|
| C0 | Moderate Standard | 8,198 | 62.8% | Typical consumption |
| C1 | High-Intensity | 1,545 | 11.8% | Highest per-capita, poor infrastructure |
| C2 | Low-Intensity Conservers | 3,318 | 25.4% | Smallest HH, eco-conscious |

**[Figure 1: Cluster Visualization]**
**[Figure 2: Cluster Profiles Radar]**

### 3.3.2 Behavioral Profiles
- C0: Moderate behaviors across all dimensions
- C1: Elevated shower/bath frequency, highest leak rates (19.7%)
- C2: Smallest households (1.9 people), lowest usage

### 3.3.3 Statistical Significance
- All ANOVA tests: p < 0.001
- Effect sizes: 79% very large (η² ≥ 0.14)
- Top differentiator: Boil-Water-Per-Week (η² = 0.87)

**[Table 2: ANOVA Results with Effect Sizes]**
**[Table 3: Chi-Square Results for Categorical Variables]**

## 3.4 Validation Results

### 3.4.1 Internal Metrics
| Metric | Value | Interpretation |
|--------|-------|----------------|
| Silhouette | 0.XX | Good separation |
| Calinski-Harabasz | XXX | High density |
| Davies-Bouldin | 0.XX | Acceptable |

**[Figure 5: Validation Metrics]**

### 3.4.2 Monte Carlo Stability
- Mean ARI = 0.981 [95% CI: 0.972, 0.989]
- Cluster-specific: C0=0.99, C1=0.94, C2=0.97
- Minority cluster (C1) marginally lower but acceptable

### 3.4.3 Sensitivity Analyses (NEW)
| Parameter | Default | Alternative | ARI |
|-----------|---------|-------------|-----|
| MAD threshold | 0.01 | 0.005, 0.02 | 0.97, 0.98 |
| Correlation cutoff | 0.85 | 0.80, 0.90 | 0.96, 0.99 |

## 3.5 XAI Results

### 3.5.1 SHAP Feature Importance
- Top 5 features: Boil-Water, Max_Prob, Wash-By-Hand, Longitude, Garden-Water
- **[Figure 4: SHAP Importance]**

### 3.5.2 Decision Tree Rules
- C1 identification: Boil-Water > 35/week AND Showers > 10/week
- C2 identification: Boil-Water < 10/week AND HH_Size < 2.5
- **[Table 4: Decision Rules with Coverage]**

### 3.5.3 Interaction Effects (NEW)
- Boil-Water × Showers interaction for C1 separation
- **[Figure S6: Interaction Effects]**

## 3.6 Counterfactual Results (NEW)
- Transition success rate: 64%
- Average behavioral reduction required: 84%
- Infrastructure contribution: Minimal (leaks not primary driver)
- Payback period: 0.5-1.1 years (with administrative costs)

---

# 4. DISCUSSION (2,000-2,500 words)

## 4.1 Principal Findings
- Three-cluster solution with high stability
- Survey-informed features enhance traditional meter-only approaches
- XAI enables actionable intervention targeting

## 4.2 Methodological Contributions
- MAD-Bootstrap for robust feature selection
- NMF provides interpretable latent representation
- GMM + XAI integration novel for water sector

## 4.3 Comparison with Prior Work (NEW)

### 4.3.1 Quantitative Benchmarking
| Method | Stability (ARI) | Interpretability |
|--------|-----------------|------------------|
| Volumetric quartiles | N/A | High |
| K-means (raw) | 0.72 | Low |
| K-means + PCA | 0.81 | Medium |
| **This study** | **0.98** | **High (XAI)** |

### 4.3.2 Positioning in Field Evolution
- Comparison with Cominola (2019), Heydari (2024), Pelekanos (2025)
- Unique contribution: Survey + stability + XAI integration

## 4.4 Practical Implications
- Utility deployment roadmap
- Intervention prioritization for C1 (11.8%)
- Cost savings projection: 61% vs. universal campaigns
- **ROI caveat**: Estimates illustrative; utility-specific validation required

## 4.5 Limitations and Future Work

### 4.5.1 Data Limitations
- Single-region study (Yorkshire Water)
- → Future: Multi-utility replication

### 4.5.2 Methodological Limitations
- Cross-sectional design
- → Future: Longitudinal behavioral tracking

### 4.5.3 Ethical Considerations (NEW)
- **Privacy**: GDPR compliance for household profiling
- **Algorithmic fairness**: Not tested for disparate impact across demographics
- **Labeling bias**: "Profligate" may introduce value judgments; recommend neutral labels
- → Future: Fairness audits before operational deployment

### 4.5.4 Technical Limitations
- Minority cluster stability marginally lower
- → Future: Oversampling or ensemble approaches

## 4.6 Generalizability and Transferability (NEW)
- Data requirements: Survey + meter + infrastructure indicators
- Cultural adaptations: Garden/outdoor behaviors vary by climate
- Recommended: UK multi-utility validation before international transfer

---

# 5. CONCLUSIONS (300-400 words)

- Summary of key contributions
- Practical deployment recommendations
- Call for multi-utility validation
- Vision for ML-enabled water demand management

---

# ACKNOWLEDGMENTS
- Yorkshire Water for data access
- Funding sources

---

# DATA AVAILABILITY
- Anonymized data available upon request
- Code available at: [GitHub Repository]
- DOI: [Zenodo archive]

---

# AUTHOR CONTRIBUTIONS (CRediT)
- Conceptualization:
- Methodology:
- Software:
- Validation:
- Formal Analysis:
- Data Curation:
- Writing - Original Draft:
- Writing - Review & Editing:
- Visualization:
- Supervision:

---

# DECLARATION OF INTERESTS
- No competing interests to declare

---

# REFERENCES (56 citations)
[See LITERATURE_REVIEW_EXPANSION.md for full list organized by topic]

Key additions:
- Meinshausen & Bühlmann (2010) - Stability Selection
- Cohen (1988) - Effect size interpretation
- Kass & Raftery (1995) - BIC justification
- Heydari & Stillwell (2024) - Recent ML comparison
- Pradeep & Bakeev (2024) - XAI in water demand
- Benjamini & Hochberg (1995) - FDR correction
- Wasserstein & Lazar (2016) - ASA statement on p-values
- Dormann et al. (2013) - Collinearity
- Tukey (1977) - EDA/outlier detection

---

# SUPPLEMENTARY MATERIAL

## Tables
- Table S1: Full feature list (97 → 18)
- Table S2: Shapiro-Wilk and Levene's test results
- Table S3: Full Tukey HSD pairwise comparisons
- Table S4: FDR-corrected p-values (74 tests)
- Table S5: Summary statistics by cluster

## Figures
- Figure S1: Normality diagnostics (Q-Q plots)
- Figure S2: Correlation heatmap
- Figure S3: GMM BIC curve (K=1-10)
- Figure S4: Cluster size distribution
- Figure S5: Feature distributions by cluster
- Figure S6: Interaction effects
- Figure S7: Box plots by cluster
- Figure S8: NMF vs PCA interpretability

## Code
- GitHub repository with:
  - requirements.txt
  - environment.yml
  - Full pipeline scripts
  - README with reproduction instructions

---

# REVISION NOTES FOR SUPERVISORS

## Changes from Original Outline

1. **Abstract**: Corrected cluster percentages (62.8%/25.4%/11.8%)
2. **Section 1.3.4**: Added Recent Advances (2020-2024)
3. **Section 2.3.1**: Added Categorical KNN protocol
4. **Section 2.5.3**: Added NMF interpretability rationale
5. **Section 2.7**: Power analysis acknowledgment
6. **Section 2.8.1**: SHAP surrogate model clarification
7. **Section 2.9**: NEW Counterfactual methodology
8. **Section 3.4.3**: Sensitivity analyses added
9. **Section 4.3**: Quantitative benchmarking table
10. **Section 4.5.3**: Ethical considerations (privacy, fairness, labeling)
11. **Section 4.6**: Generalizability section
12. **ROI**: Revised from 0.1 to 0.5-1.1 years with administrative costs

## Figures Added
- 14 publication-quality figures (6 main + 8 supplementary)

## References
- Expanded from 11 to 56 citations
- Added 2020-2024 recent work
- Added foundational methodological references

---

**STATUS: Ready for Supervisor Review**
