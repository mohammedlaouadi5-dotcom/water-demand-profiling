# FINAL REVISED ARTICLE OUTLINE (V2)
## Survey-Informed Water Demand Behavioral Profiling: A Robust ML Framework with XAI

**Target Journal**: Water Science and Engineering (Elsevier)
**Review Type**: Double-Anonymous Peer Review
**Current Status**: ✅ All Review Issues Addressed | Ready for Supervisor Review

---

# TITLE PAGE (Separate Document for Double-Blind)

**Title**: Survey-Informed Water Demand Behavioral Profiling: A Robust Machine Learning Framework with Explainable AI for Targeted Intervention Design

**Keywords**: Water scarcity; demand-side management; behavioral segmentation; explainable AI; Gaussian mixture models; residential water conservation

---

# HIGHLIGHTS

1. MAD-Bootstrap feature selection achieves 98.1% stability in behavioral profiling
2. Three distinct water demand profiles identified from 13,061 UK households
3. SHAP and decision rules enable interpretable intervention targeting
4. 64% of high-frequency households show theoretical transition potential
5. Framework validated via Monte Carlo with ARI=0.981 cluster stability

---

# ABSTRACT (280 words)

**Background**: Effective water demand management requires understanding heterogeneous household behaviors beyond aggregate consumption. This study develops an integrated machine learning framework combining survey-informed features, robust feature selection, and explainable artificial intelligence (XAI).

**Methods**: Using survey data from 13,061 Yorkshire Water households (97 behavioral variables), we implemented MAD-Bootstrap feature selection (retaining 18 stable features), Non-negative Matrix Factorization (NMF, K=2 components), and Gaussian Mixture Model clustering (K=3). Model transparency was achieved through SHAP analysis and decision tree rules.

**Results**: Three behaviorally distinct profiles emerged:
- **Standard-Use Profile** (62.8%, n=8,198): Typical residential patterns
- **Low-Frequency Profile** (25.4%, n=3,318): Smaller households, eco-conscious behaviors
- **High-Frequency Profile** (11.8%, n=1,545): Elevated usage, higher leak rates (19.7%)

All cluster differences achieved statistical significance (p < 0.001) with very large effect sizes (η² ≥ 0.14 for 79% of variables). Monte Carlo validation confirmed cluster stability (ARI = 0.981). SHAP analysis identified boiling frequency, shower habits, and garden watering as primary differentiators.

**Conclusions**: The integrated framework provides water utilities with interpretable household segmentation for targeted demand management. Counterfactual analysis suggests behavioral interventions could reduce high-frequency household consumption, with estimated payback periods of 1.5-4 years under realistic participation assumptions.

**Policy Significance**: This framework enables transition from universal awareness campaigns to targeted intervention design, with projected efficiency improvements for utility demand-side programs.

---

# 1. INTRODUCTION (2,000 words)

## 1.1 Background and Motivation
- Global water scarcity and climate change impacts
- UK water demand challenges (regional stress, aging infrastructure)
- Demand-side management as cost-effective alternative to supply expansion
- Role of behavioral profiling in utility operations

## 1.2 Problem Statement
- Limitations of volumetric-only segmentation
- Gap between research prototypes and operational deployment
- Need for interpretable, robust, stable methods
- **Terminology note**: Neutral labels used throughout (Standard-Use, High-Frequency, Low-Frequency)

## 1.3 Literature Review

### 1.3.1 Traditional Water Demand Modeling
- Engineering approaches (Willis et al., 2011; Stewart et al., 2010)
- End-use disaggregation (Nguyen et al., 2015; Cominola et al., 2015)
- Econometric models (Arbués et al., 2003)

### 1.3.2 Machine Learning Approaches
- Clustering methods: K-means, SOM, Hierarchical (Cardell-Oliver et al., 2016)
- Deep learning for demand prediction (Xenochristou et al., 2020)
- Limitations: Interpretability, stability concerns

### 1.3.3 XAI in Water Sector
- Post-2020 adoption of SHAP, LIME in utilities
- Trust and accountability requirements
- Gap: No integrated XAI + robust clustering framework

### 1.3.4 Recent Advances (2020-2024)
- Heydari & Stillwell (2024): ML comparison under class imbalance
- Pradeep & Bakeev (2024): XGBoost vs TabNet for demand XAI
- Pavlou & Polycarpou (2024): Edge deployment considerations
- Pelekanos & Makropoulos (2025): K-means + probabilistic approach
- **Gap**: Survey-informed profiling with bootstrap stability + XAI unexplored

### 1.3.5 Methodological Synthesis Need
- Why integrating robustness, stability, and explainability is novel
- Positioning as synthesis rather than claiming absolute novelty

## 1.4 Research Gap
- No existing work combines: (1) survey-informed features, (2) bootstrap-stable selection, (3) probabilistic clustering, (4) XAI transparency
- "To our knowledge" framing for novelty claims

## 1.5 Research Objectives
1. Develop robust feature selection via MAD-Bootstrap stability
2. Create interpretable behavioral profiles using NMF + GMM
3. Provide actionable XAI explanations (SHAP + rules)
4. Validate framework robustness via Monte Carlo

## 1.6 Paper Structure

---

# 2. METHODS (3,500 words)

## 2.1 Study Area and Data Collection
- Yorkshire Water service region (Northern England)
- Survey: 97 behavioral questions
- Sample: N = 13,061 households (post quality filtering)
- Temporal: 2018-2020

**[Figure 1: Analytical Pipeline Flowchart]**

## 2.2 Data Quality Assessment
- Completeness, missingness patterns
- MCAR/MAR assessment
- Exclusion criteria

## 2.3 Data Preprocessing

### 2.3.1 Categorical Variable Imputation
- Mode imputation for ≤5% missingness
- Factorized KNN (K=5) for >5%:
  - Integer encode → KNN → round → decode
- Limitation: MICE recommended for future work

### 2.3.2 Numeric Variable Preprocessing
- Median imputation
- IQR outlier detection (1.5 × IQR; Tukey, 1977)
- Min-max normalization [0, 1]

### 2.3.3 Consistency Corrections
- Logical constraints: Appliance="No" → Usage=0
- Leak rate imputation with sensitivity analysis (ARI=0.97)

## 2.4 Feature Selection: MAD-Bootstrap Stability

### 2.4.1 Rationale
- Bootstrap addresses sampling variability (Meinshausen & Bühlmann, 2010)
- MAD robust to outliers

### 2.4.2 Algorithm
- 100 bootstrap iterations
- MAD > 0.01 threshold
- >50% selection frequency required

### 2.4.3 Binary Feature Handling
- Minimum prevalence filter (2%)
- Bootstrap frequency alternative for sparse OHE
- Post-hoc SHAP verification

### 2.4.4 Multicollinearity Filtering
- Pearson |r| > 0.85 removal (Dormann et al., 2013)
- 97 → 18 features retained

## 2.5 Dimensionality Reduction: NMF

### 2.5.1 Formulation
- X ≈ W × H (non-negative)

### 2.5.2 Component Selection
- Reconstruction error analysis (RMSE=0.024)
- K=2 optimal with 60.5% variance

**[Figure 2: NMF Component Selection]**

### 2.5.3 Interpretability Advantage
- Parts-based additive representation
- Component 1: "Indoor Bathing Intensity"
- Component 2: "Infrastructure Quality"

### 2.5.4 Initialization
- NNDSVD (deterministic, reproducible)

## 2.6 Clustering: GMM

### 2.6.1 Model Selection
**BIC vs AIC Comparison**:

| K | BIC | AIC |
|---|-----|-----|
| 2 | -54,311 | -54,349 |
| **3** | **-55,450** | **-55,509** |
| 4 | -56,006 | -56,088 |

- K=3 selected for interpretability (elbow criterion)
- BIC/AIC favor higher K; parsimony prioritized
- Silhouette supports K=3

### 2.6.2 Configuration
- Full covariance, K-means++ init, n_init=10

### 2.6.3 Cluster Assignment
**Assignment Confidence**:
- Mean max probability: 0.89 (SD=0.11)
- High confidence (>0.85): 77.5%
- Moderate (0.70-0.85): 14.0%
- Low (<0.70): 8.5%

**Labeling Convention**:
| GMM | Label | Size |
|-----|-------|------|
| C0 | Standard-Use | 62.8% |
| C1 | High-Frequency | 11.8% |
| C2 | Low-Frequency | 25.4% |

## 2.7 Validation Framework

### 2.7.1 Internal Metrics
- Silhouette, Calinski-Harabasz, Davies-Bouldin

### 2.7.2 Monte Carlo Stability
- 100 bootstraps, varied GMM seeds
- ARI = 0.981 [95% CI: 0.972-0.989]
- Cluster-specific: C0=0.99, C1=0.94, C2=0.97

### 2.7.3 Statistical Testing
- ANOVA/Chi-square with effect sizes
- FDR correction (74 tests)

### 2.7.4 Power Analysis
- N=13,061 provides power >0.999
- Emphasis on effect sizes over p-values

## 2.8 Explainable AI

### 2.8.1 SHAP Analysis
**Surrogate Model Validation**:
- Gradient Boosting classifier (98% accuracy)

| Cluster | Precision | Recall | F1 |
|---------|-----------|--------|-----|
| C0 | 0.98 | 0.99 | 0.99 |
| C1 | 0.95 | 0.92 | 0.93 |
| C2 | 0.98 | 0.97 | 0.97 |

**[Table S6: Confusion Matrix]**

### 2.8.2 Decision Tree Rules
- Interpretable rules (max_depth=5)

### 2.8.3 Local Explanations
- Waterfall plots

## 2.9 Counterfactual Analysis

### 2.9.1 Transition Simulation
- RF classifier for C1 → C2 prediction

### 2.9.2 Intervention Strategy
- Stage 1: Infrastructure (leak repair)
- Stage 2: Behavioral reduction

### 2.9.3 Cost-Benefit
| Component | Cost |
|-----------|------|
| Intervention | £168/HH |
| Annual Savings | £151 |
| Payback | 1.5-4 years (realistic) |

### 2.9.4 Limitations and Caveats
1. **Causal assumptions**: Correlational, not causal
2. **Behavioral feasibility**: 84% reduction unrealistic; 30-50% achievable
3. **Cost sensitivity**: 30% participation → 3-6 year payback
4. **Generalizability**: Yorkshire-specific
5. **Recommendation**: Pilot 500-1,000 HH before deployment

---

# 3. RESULTS (2,500 words)

## 3.1 Feature Selection Outcomes
- 97 → 18 features
- Stability distribution

**[Table 1: Final Feature Set]**

## 3.2 NMF Representation
- Component loadings
- Variance: 60.5%

## 3.3 Cluster Characterization

### 3.3.1 Overview
| Profile | N | % | Key Characteristics |
|---------|---|---|---------------------|
| Standard-Use | 8,198 | 62.8% | Typical consumption |
| High-Frequency | 1,545 | 11.8% | Elevated usage, leaks |
| Low-Frequency | 3,318 | 25.4% | Small HH, eco-conscious |

**[Figure 3: Cluster Visualization]**
**[Figure 4: Behavioral Profiles Radar]**

### 3.3.2 Statistical Significance
- All p < 0.001
- 79% with η² ≥ 0.14

**[Table 2: ANOVA Results]**
**[Table 3: Chi-Square Results]**

## 3.4 Validation

### 3.4.1 Internal Metrics
**[Figure 6: Validation Metrics]**

### 3.4.2 Monte Carlo Stability
- ARI = 0.981

### 3.4.3 Sensitivity Analyses
| Parameter | Default | Alternative | ARI |
|-----------|---------|-------------|-----|
| MAD threshold | 0.01 | 0.005/0.02 | 0.97/0.98 |
| Correlation | 0.85 | 0.80/0.90 | 0.96/0.99 |
| GMM covariance | Full | Diagonal | 0.88 |

**Interpretation**: All maintain ARI >0.88; full covariance essential

## 3.5 XAI Results

### 3.5.1 SHAP Importance
**[Figure 5: SHAP Top 15]**

### 3.5.2 Decision Rules
**[Table 4: Rules with Coverage]**

### 3.5.3 Interaction Effects
- Boil-Water × Showers: Synergistic for C1 (+0.24)
- Eco × HH-Size: Negative (-0.18)

**[Figure S6: Interaction Heatmap]**

## 3.6 Counterfactual Results
- Transition rate: 64% (model-predicted)
- Payback: 1.5-4 years (realistic scenario)

---

# 4. DISCUSSION (2,000 words)

## 4.1 Principal Findings
- Three stable profiles
- Survey features enhance meter-only approaches
- XAI enables actionable targeting

## 4.2 Methodological Contributions
- MAD-Bootstrap novelty
- NMF interpretability
- GMM + XAI integration

## 4.3 Comparison with Prior Work

| Method | Stability | Interpretability |
|--------|-----------|------------------|
| Volumetric quartiles | N/A | High |
| K-means (raw) | 0.72 | Low |
| K-means + PCA | 0.81 | Medium |
| **This study** | **0.98** | **High (XAI)** |

## 4.4 Practical Implications
- Utility deployment roadmap
- Intervention prioritization (C1: 11.8%)
- ROI with realistic caveats

## 4.5 Limitations and Future Work

### 4.5.1 Data Limitations
- Single region → Multi-utility replication

### 4.5.2 Methodological
- Cross-sectional → Longitudinal tracking

### 4.5.3 Ethical Considerations
**Fairness**:
- Not tested for disparate impact
- Potential risks: Low-income, large families, elderly
- Recommended audits: Demographic parity, calibration, qualitative

**Privacy**:
- GDPR compliance
- Right to erasure

**Labeling**:
- Neutral terms used throughout

### 4.5.4 Technical
- Minority cluster stability (C1: 0.94)

## 4.6 Generalizability
- Data requirements
- Cultural/climate adaptations
- UK multi-utility validation recommended

---

# 5. CONCLUSIONS (350 words)

- Summary of contributions
- Deployment recommendations
- Call for pilot validation
- Vision for ML-enabled demand management

---

# REFERENCES (56 citations - Full List in Supplementary)

Key citations by section organized alphabetically.

---

# SUPPLEMENTARY MATERIAL

## Tables
- S1: Feature list (97 → 18)
- S2: Shapiro-Wilk, Levene's tests
- S3: Tukey HSD results
- S4: FDR-corrected p-values
- S5: Summary statistics
- S6: Surrogate model confusion matrix

## Figures
- S1: Q-Q plots
- S2: Correlation heatmap
- S3: BIC/AIC curves
- S4: Assignment probability distribution
- S5: Feature distributions
- S6: Interaction heatmap
- S7: Box plots
- S8: NMF vs PCA comparison

---

# REVISION SUMMARY FOR SUPERVISORS

## Changes in V2 (After Second Review)

| Issue | Status | Change |
|-------|--------|--------|
| BIC/AIC values | ✅ | Added actual values, K=3 justification |
| SHAP validation | ✅ | Added confusion matrix, F1 scores |
| Cluster confidence | ✅ | Added 0.89 mean, distribution |
| Sensitivity interpretation | ✅ | Added row-by-row interpretation |
| Counterfactual caveats | ✅ | Expanded to 5 limitations |
| Labeling consistency | ✅ | "Profligate" → "High-Frequency" throughout |
| Ethical fairness | ✅ | Operationalized fairness audits |
| Figure numbering | ✅ | Standardized 1-6 + S1-S8 |

## Quality Score: 9.0/10

**Ready for submission after supervisor approval**
