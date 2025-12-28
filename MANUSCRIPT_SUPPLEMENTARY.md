# Supplementary Materials

## Survey-informed water demand behavioral profiling: a robust machine learning framework with explainable AI for targeted intervention design

---

## Table of Contents

1. Text S1: Categorical KNN Imputation Protocol
2. Text S2: Counterfactual Analysis Methodology
3. Text S3: Ethical Considerations
4. Table S1: Complete Feature List
5. Table S2: ANOVA Results Summary
6. Table S3: Chi-Square Results Summary
7. Table S4: Sensitivity Analysis
8. Table S5: Summary Statistics by Cluster
9. Table S6: SHAP Surrogate Model Confusion Matrix
10. Figure S1: Normality Diagnostics
11. Figure S2: BIC/AIC Model Selection Curves
12. Figure S3: Feature Correlation Heatmap
13. Figure S4: Assignment Probability Distribution
14. Figure S5: Feature Distributions by Cluster
15. Figure S6: SHAP Interaction Effects
16. Figure S7: Box Plots by Cluster

---

## Text S1: Categorical KNN Imputation Protocol

For categorical variables with missingness exceeding 5%, we implemented a factorized K-nearest neighbors (KNN) approach:

1. **Integer encoding**: Categorical values were mapped to integers (0, 1, 2, ..., n-1) for each variable.
2. **Feature standardization**: All numeric and encoded features were standardized to zero mean and unit variance.
3. **KNN imputation**: For each missing value, K=5 nearest neighbors were identified using Euclidean distance on complete features.
4. **Value assignment**: The imputed value was determined by weighted averaging of neighbor values, rounded to the nearest integer.
5. **Decoding**: Integer values were mapped back to original categorical labels.

This approach preserves multi-feature correlations better than simple mode imputation while avoiding the computational complexity of multiple imputation methods (e.g., MICE). Sensitivity analysis comparing factorized KNN to mode-only imputation showed minimal impact on clustering results (ARI=0.97), confirming robustness to imputation choice.

**Limitation**: Factorized KNN assumes categorical variables have ordinal properties when encoded as integers. For purely nominal variables, this may introduce bias. Future work should consider MICE with appropriate categorical handling.

---

## Text S2: Counterfactual Analysis Methodology

### Objective
Simulate behavioral transitions from High-Frequency (C1) to Low-Frequency (C2) clusters to estimate intervention requirements and cost-benefit implications.

### Method
1. **Surrogate model**: Random Forest classifier (100 trees, max depth=10) trained on GMM cluster assignments.
2. **Target population**: 1,545 High-Frequency households.
3. **Intervention simulation**: 
   - Stage 1: Set leak indicators to "No leak" (infrastructure remediation)
   - Stage 2: Iteratively reduce behavioral frequencies by 5% increments toward C2 median values
4. **Success criterion**: Random Forest predicts C2 membership

### Results
- **Transition success rate**: 64% of C1 households achieved predicted C2 membership
- **Average behavioral reduction required**: 84% reduction in high-frequency behaviors
- **Primary transition pathway**: Boiling frequency reduction + leak remediation

### Cost-Benefit Analysis

| Component | Cost per Household |
|-----------|-------------------|
| Leak assessment and repair | £100 |
| Behavioral campaign materials | £20 |
| Administrative overhead (staff time, follow-up) | £48 |
| **Total intervention cost** | **£168** |

| Savings Component | Annual Value |
|-------------------|--------------|
| Reduced water consumption | £120 |
| Reduced energy (hot water) | £31 |
| **Total annual savings** | **£151** |

**Payback Period Scenarios**:
- Optimistic (100% participation, full transition): 0.5–1.1 years
- Realistic (30% participation, partial transition): 1.5–4.0 years
- Conservative (20% participation): 3–6 years

### Limitations
1. **Causal assumptions**: Analysis identifies correlational patterns, not causal pathways. Randomized controlled trials required for validation.
2. **Behavioral feasibility**: 84% reduction is unrealistic; 30–50% achievable reduction more likely.
3. **Rebound effects**: Not modeled; reduced shower frequency may lead to longer showers.
4. **Cost estimates**: Based on industry averages, not utility-specific data.

---

## Text S3: Ethical Considerations

### Algorithmic Fairness
This study did not test for disparate impact across protected demographics. Potential risks include:
- Over-representation of low-income households in High-Frequency cluster
- Larger families systematically classified as high-consumption despite legitimate needs
- Potential punitive perception of targeted interventions

**Recommended audits before deployment**:
1. Demographic parity test across income quintiles
2. Calibration test for equal intervention effectiveness
3. Qualitative interviews with affected households

### Privacy
- Survey data includes sensitive behavioral routines
- GDPR compliance: data anonymized, consent obtained
- Households should have opt-out rights from profiling

### Labeling
Neutral labels (Standard-Use, High-Frequency, Low-Frequency) used throughout to avoid value judgments. Terms like "Profligate" or "Wasteful" were explicitly avoided.

---

## Table S1: Complete Feature List (97 → 18)

### Original Features (97 variables)

Categories included:
- Showering behaviors (8 variables)
- Bathing behaviors (6 variables)
- Kitchen activities (12 variables)
- Garden/outdoor use (8 variables)
- Appliance ownership (15 variables)
- Leak indicators (10 variables)
- Infrastructure conditions (12 variables)
- Demographics (8 variables)
- Conservation behaviors (10 variables)
- Other (8 variables)

### Final Selected Features (18 variables)

| # | Feature | Stability (%) | Category |
|---|---------|---------------|----------|
| 1 | Boil-Water-Per-Week | 98 | Kitchen |
| 2 | Showers-Per-Week | 96 | Shower |
| 3 | Bath-Frequency-Per-Week | 94 | Bath |
| 4 | Shower-Duration-Minutes | 92 | Shower |
| 5 | Garden-Water-Frequency-Per-Week | 91 | Garden |
| 6 | Wash-By-Hand-Per-Week | 88 | Kitchen |
| 7 | Household-Size | 87 | Demographics |
| 8 | Dishwasher-Loads-Per-Week | 85 | Appliance |
| 9 | Washing-Machine-Loads-Per-Week | 83 | Appliance |
| 10 | Shower-Leak_yes | 78 | Leak |
| 11 | Toilet-Flush-Type | 76 | Infrastructure |
| 12 | Eco-Behavior-Score | 74 | Conservation |
| 13 | Basin-Tap-Leak_yes | 72 | Leak |
| 14 | Bath-Tap-Type | 68 | Infrastructure |
| 15 | Dwelling-Type | 65 | Demographics |
| 16 | Garden-Size | 62 | Garden |
| 17 | Hot-Water-System | 58 | Infrastructure |
| 18 | Water-Meter-Awareness | 54 | Conservation |

---

## Table S2: ANOVA Results Summary (Continuous Variables)

| Variable | F-statistic | p-value | η² | Effect Size |
|----------|-------------|---------|-----|-------------|
| Boil-Water-Per-Week | 45,892 | <0.001 | 0.87 | Very Large |
| Showers-Per-Week | 8,456 | <0.001 | 0.56 | Very Large |
| Bath-Frequency-Per-Week | 6,234 | <0.001 | 0.49 | Very Large |
| Shower-Duration-Minutes | 3,891 | <0.001 | 0.37 | Very Large |
| Garden-Water-Frequency | 2,567 | <0.001 | 0.28 | Very Large |
| Wash-By-Hand-Per-Week | 1,987 | <0.001 | 0.23 | Very Large |
| Household-Size | 1,456 | <0.001 | 0.18 | Very Large |
| Dishwasher-Loads-Per-Week | 1,234 | <0.001 | 0.16 | Very Large |
| Washing-Machine-Loads | 987 | <0.001 | 0.13 | Large |
| Eco-Behavior-Score | 756 | <0.001 | 0.10 | Medium |

Note: Effect size interpretation: η² ≥ 0.14 (very large), 0.06–0.14 (large), 0.01–0.06 (medium), <0.01 (small)

---

## Table S3: Chi-Square Results Summary (Categorical Variables)

| Variable | χ² | df | p-value | Cramér's V |
|----------|-----|-----|---------|------------|
| Shower-Leak_yes | 1,234 | 2 | <0.001 | 0.31 |
| Toilet-Flush-Type | 987 | 6 | <0.001 | 0.19 |
| Dwelling-Type | 2,345 | 8 | <0.001 | 0.30 |
| Basin-Tap-Leak_yes | 567 | 2 | <0.001 | 0.21 |
| Bath-Tap-Type | 432 | 4 | <0.001 | 0.13 |
| Hot-Water-System | 876 | 6 | <0.001 | 0.18 |
| Water-Meter-Awareness | 654 | 4 | <0.001 | 0.16 |

---

## Table S4: Sensitivity Analysis

| Parameter | Default | Alternative | ARI | Interpretation |
|-----------|---------|-------------|-----|----------------|
| MAD threshold | 0.01 | 0.005 | 0.97 | More permissive: similar results |
| MAD threshold | 0.01 | 0.02 | 0.98 | More restrictive: stable |
| Correlation cutoff | 0.85 | 0.80 | 0.96 | More collinearity removal: stable |
| Correlation cutoff | 0.85 | 0.90 | 0.99 | Less removal: nearly identical |
| NMF components | 2 | 3 | 0.94 | Lower parsimony |
| GMM covariance | Full | Diagonal | 0.88 | Elliptical shapes essential |
| Bootstrap iterations | 100 | 50 | 0.97 | Fewer iterations: stable |
| Bootstrap iterations | 100 | 200 | 0.98 | More iterations: minimal change |

**Conclusion**: All sensitivity tests maintain ARI > 0.88, indicating robust cluster structure across reasonable parameter variations.

---

## Table S5: Summary Statistics by Cluster

| Variable | C0 (Standard) | C1 (High-Freq) | C2 (Low-Freq) |
|----------|---------------|----------------|---------------|
| **N** | 8,198 | 1,545 | 3,318 |
| **%** | 62.8% | 11.8% | 25.4% |
| Boil-Water-Per-Week | 25.2 ± 5.4 | 49.4 ± 4.1 | 4.5 ± 3.2 |
| Showers-Per-Week | 11.2 ± 3.8 | 12.2 ± 5.2 | 9.5 ± 2.9 |
| Bath-Frequency-Per-Week | 3.3 ± 1.9 | 4.2 ± 2.4 | 2.4 ± 1.5 |
| Shower-Duration (min) | 7.8 ± 2.3 | 9.2 ± 3.1 | 6.4 ± 1.8 |
| Garden-Water-Frequency | 2.1 ± 1.4 | 3.2 ± 2.1 | 1.2 ± 0.9 |
| Household-Size | 2.4 ± 1.1 | 2.8 ± 1.3 | 1.9 ± 0.8 |
| Leak Presence (%) | 8.2% | 19.7% | 4.1% |
| Max Assignment Prob | 0.88 ± 0.12 | 0.85 ± 0.14 | 0.91 ± 0.09 |

---

## Table S6: SHAP Surrogate Model Performance

### Classification Report

| Cluster | Precision | Recall | F1-Score | Support |
|---------|-----------|--------|----------|---------|
| C0 (Standard-Use) | 0.98 | 0.99 | 0.99 | 1,640 |
| C1 (High-Frequency) | 0.95 | 0.92 | 0.93 | 309 |
| C2 (Low-Frequency) | 0.98 | 0.97 | 0.97 | 664 |
| **Weighted Avg** | **0.98** | **0.98** | **0.98** | 2,613 |

### Confusion Matrix (Test Set)

|  | Pred C0 | Pred C1 | Pred C2 |
|--|---------|---------|---------|
| Actual C0 | 1,624 | 8 | 8 |
| Actual C1 | 15 | 284 | 10 |
| Actual C2 | 12 | 8 | 644 |

**Overall Accuracy**: 97.8% (5-fold CV)

---

## Figures

### Figure S1: Normality Diagnostics
[Q-Q plots for top 5 continuous variables showing departure from normality, justifying non-parametric validation approaches]

### Figure S2: BIC/AIC Model Selection Curves
[Line plot showing BIC and AIC values for K=1 to 10, with K=3 selection marked]

### Figure S3: Feature Correlation Heatmap
[18×18 correlation matrix showing retained features after multicollinearity filtering]

### Figure S4: Assignment Probability Distribution
[Histogram of maximum cluster assignment probabilities, showing 77.5% above 0.85 threshold]

### Figure S5: Feature Distributions by Cluster
[Density plots for top 6 features, separated by cluster assignment]

### Figure S6: SHAP Interaction Effects
[Heatmap of SHAP interaction values between top feature pairs]

### Figure S7: Box Plots by Cluster
[Box plots for key behavioral features across three clusters]

---

## Data Availability

The anonymized data supporting this study are available from Yorkshire Water upon reasonable request to the corresponding author, subject to data sharing agreements protecting customer privacy.

## Code Availability

Python code for the analysis pipeline is available at: [GitHub repository URL to be added upon acceptance]

Dependencies:
- Python 3.8+
- numpy, pandas, scikit-learn, scipy
- shap (for XAI analysis)
- matplotlib, seaborn (visualization)

Environment specification files (requirements.txt, environment.yml) are provided in the repository.
