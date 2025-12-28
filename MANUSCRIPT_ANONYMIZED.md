# Survey-informed water demand behavioral profiling: a robust machine learning framework with explainable AI for targeted intervention design

---

## Abstract

Effective water demand management requires understanding heterogeneous household behaviors beyond aggregate volumetric consumption. This study develops an integrated machine learning framework combining survey-informed behavioral features, robust feature selection, and explainable artificial intelligence (XAI) to profile residential water demand patterns. Using comprehensive survey data from 13,061 households in the United Kingdom with 97 behavioral variables, we implemented a three-stage analytical pipeline. First, MAD-Bootstrap stability selection retained 18 robust features demonstrating consistent predictive importance across 100 bootstrap iterations. Second, Non-negative Matrix Factorization (NMF) reduced dimensionality to two interpretable latent components capturing indoor water-use intensity and infrastructure quality. Third, Gaussian Mixture Models (GMM) identified three behaviorally distinct profiles: Standard-Use (62.8%, n=8,198), Low-Frequency (25.4%, n=3,318), and High-Frequency (11.8%, n=1,545). Monte Carlo validation confirmed high cluster stability with Adjusted Rand Index of 0.981. All inter-cluster differences achieved statistical significance (p<0.001) with very large effect sizes (η²≥0.14 for 79% of variables). SHAP analysis identified boiling frequency, shower habits, and garden watering as primary behavioral differentiators, enabling targeted intervention design. The framework provides water utilities with interpretable, stable household segmentation for demand-side management, offering a pathway from universal awareness campaigns toward efficient, targeted conservation programs.

**Keywords:** water demand; behavioral profiling; machine learning; explainable AI; Gaussian mixture model; demand-side management

---

## 1. Introduction

### 1.1 Background and problem statement

Global freshwater resources face increasing pressure from population growth, urbanization, and climate change, making demand-side management essential for sustainable water resource utilization (Gleick, 2018). Traditional water demand management relies primarily on volumetric consumption data, segmenting households into high, medium, and low consumers based on metered readings. However, this approach fails to capture the behavioral drivers underlying consumption patterns, limiting the effectiveness of conservation interventions (Beal et al., 2013).

Survey-informed behavioral profiling offers a complementary approach by integrating self-reported water-use habits, appliance ownership, and infrastructure conditions with consumption data. Such integration enables utilities to understand not only how much water households consume but also why and how they consume it. This understanding is crucial for designing targeted interventions that address specific behavioral patterns rather than applying universal conservation messages with limited effectiveness.

Despite advances in machine learning for water demand analysis, significant methodological challenges remain. Existing clustering approaches often suffer from feature selection instability, poor interpretability, and limited validation of cluster robustness (Cominola et al., 2015). Furthermore, the deployment of complex machine learning models in utility operations requires transparent, explainable results that decision-makers can trust and act upon.

### 1.2 Literature review

Traditional water demand modeling has evolved from engineering-based end-use disaggregation (Stewart et al., 2010) to data-driven machine learning approaches. K-means clustering, self-organizing maps, and hierarchical clustering have been applied to smart meter data with varying success (Cardell-Oliver et al., 2016). However, these methods face limitations in handling high-dimensional behavioral data and providing interpretable results.

Recent studies have explored advanced clustering techniques including Gaussian Mixture Models, which offer probabilistic cluster assignments accommodating uncertainty in behavioral classification (Cominola et al., 2019). Dimensionality reduction using Principal Component Analysis (PCA) and NMF has been applied to manage feature complexity, with NMF offering advantages for behavioral data through its parts-based, non-negative representation (Lee and Seung, 1999).

The emergence of Explainable AI (XAI) in water systems addresses the interpretability gap between complex models and operational deployment. SHAP (SHapley Additive exPlanations) values provide consistent, locally accurate feature attributions explaining individual predictions (Lundberg and Lee, 2017). Recent applications in water demand forecasting demonstrate XAI's potential for building trust in machine learning models (Xenochristou et al., 2020).

Despite these advances, a critical gap remains: no existing framework integrates survey-informed behavioral features with robust, stability-validated feature selection, probabilistic clustering, and XAI transparency for utility deployment. Most studies rely on meter-only data, apply ad-hoc feature selection, or lack systematic validation of cluster stability.

### 1.3 Objectives

This study addresses the identified gaps through four objectives:

1. Develop a robust feature selection method (MAD-Bootstrap) ensuring stable feature retention across bootstrap samples;
2. Create interpretable behavioral clusters using NMF dimensionality reduction and GMM probabilistic clustering;
3. Provide transparent cluster explanations through SHAP analysis and decision tree rule extraction;
4. Validate framework robustness using Monte Carlo stability analysis and internal clustering metrics.

---

## 2. Material and methods

### 2.1 Data collection and study area

This study used household survey data collected by Yorkshire Water, serving approximately 5 million customers in Northern England, United Kingdom. The survey captured 97 variables including water-use frequencies (showering, bathing, garden watering), appliance ownership (dishwashers, washing machines), infrastructure conditions (leak presence, tap types), household demographics (size, dwelling type), and self-reported conservation behaviors. After quality filtering for completeness and consistency, the final sample comprised 13,061 households with matched annual consumption records from 2018-2020.

### 2.2 Data preprocessing

Missing values were addressed through a hybrid imputation strategy. For numeric variables with missingness below 10%, median imputation was applied. For categorical variables, mode imputation addressed low missingness (≤5%), while factorized K-nearest neighbors (K=5) handled variables with higher missingness, preserving multi-feature correlations. Outliers were identified using the 1.5×IQR rule (Tukey, 1977) and capped to prevent extreme value influence. All numeric features were normalized to [0,1] range for algorithm stability.

Logical consistency corrections ensured data quality: appliance usage frequencies were set to zero where appliance ownership was negative, and missing leak rates were imputed as "slowly" where leak presence was confirmed, following utility domain knowledge. Sensitivity analysis confirmed minimal impact on final clustering results (Adjusted Rand Index = 0.97 compared to alternative imputation).

### 2.3 Feature selection: MAD-Bootstrap stability

Traditional variance-based feature selection is susceptible to sampling variability, potentially retaining irrelevant features or discarding important ones based on specific sample characteristics. We addressed this through MAD-Bootstrap stability selection combining Median Absolute Deviation (MAD) with bootstrap resampling (Meinshausen and Bühlmann, 2010).

The algorithm proceeds as follows: For 100 bootstrap iterations, we resampled N households with replacement, computed MAD for each feature, and recorded features exceeding a threshold of 0.01. Features retained in more than 50% of iterations were selected as stable. After stability selection, multicollinearity was addressed by removing features with Pearson correlation |r|>0.85, following established practice (Dormann et al., 2013). This process reduced the feature space from 97 to 18 stable, low-redundancy behavioral indicators.

### 2.4 Dimensionality reduction: Non-negative Matrix Factorization

To capture latent behavioral dimensions while maintaining interpretability, we applied NMF to the selected features. NMF decomposes the feature matrix X into non-negative factors W (household loadings) and H (component patterns), providing parts-based representation where components combine additively without negative contributions (Lee and Seung, 1999).

Component number selection followed reconstruction error analysis. Testing K=1 to 10, RMSE plateaued at K=2 (0.024 on normalized scale), with minimal improvement for higher K. Two components explained 60.5% of variance and offered clear interpretation: Component 1 captured indoor water-use intensity (loadings on showering, bathing, boiling frequency), while Component 2 reflected infrastructure quality and maintenance indicators (loadings on leak presence, tap conditions). NNDSVD initialization ensured deterministic, reproducible results.

### 2.5 Clustering: Gaussian Mixture Models

Gaussian Mixture Models were selected for their probabilistic cluster assignments, allowing uncertainty quantification in behavioral classification. The number of clusters was determined using Bayesian Information Criterion (BIC) over K=1 to 10. While BIC continued decreasing slightly beyond K=3 (BIC at K=3: -55,450), we selected K=3 based on interpretability, parsimony, and diminishing marginal improvement (Fig. 5). Both BIC and Akaike Information Criterion converged on similar selection regions.

GMM configuration used full covariance matrices capturing elliptical cluster shapes, K-means++ initialization, and 10 random restarts to avoid local optima. Mean maximum assignment probability was 0.89 (SD=0.11), with 77.5% of households showing high-confidence assignments (probability >0.85), indicating clear cluster membership for most households.

### 2.6 Validation framework

Cluster validation employed both internal metrics and stability analysis. Internal metrics included Silhouette Score (cluster separation), Calinski-Harabasz Index (cluster density), and Davies-Bouldin Index (cluster compactness). Monte Carlo stability analysis assessed robustness across 100 bootstrap iterations with varied GMM random seeds, computing Adjusted Rand Index (ARI) agreement with the baseline solution.

Statistical significance of inter-cluster differences was evaluated using ANOVA for continuous variables (with Welch's correction where homoscedasticity was violated) and Chi-square tests for categorical variables. Effect sizes were reported using eta-squared (η²) for ANOVA and Cramér's V for Chi-square. Given the large sample size (N=13,061) providing statistical power exceeding 0.99, interpretation emphasized effect size magnitude over p-values alone.

### 2.7 Explainable AI: SHAP analysis

To provide feature-level explanations, we implemented SHAP analysis using a surrogate modeling approach. Since GMM is unsupervised, we trained a Gradient Boosting classifier using GMM-assigned cluster labels as targets. The surrogate achieved 97.8% classification accuracy (5-fold cross-validation) with balanced class-wise performance (F1-scores: C0=0.99, C1=0.93, C2=0.97), confirming high fidelity to GMM boundaries.

SHAP values derived from the surrogate quantify each feature's contribution to cluster predictions. Mean absolute SHAP values provide global feature importance rankings, while individual SHAP profiles enable household-level explanations for personalized intervention targeting.

---

## 3. Results

### 3.1 Feature selection outcomes

MAD-Bootstrap stability selection retained 18 features from the original 97, representing an 81% reduction while preserving behavioral discrimination. The most stable features (selection frequency >90%) included boiling frequency, shower frequency, bath frequency, garden watering, and household size. Stability analysis confirmed that these features consistently discriminated behavioral patterns regardless of sampling variation.

### 3.2 Cluster characterization

Three distinct behavioral profiles emerged from GMM clustering in the NMF-transformed space (Fig. 2–3, Table 1):

**Table 1. Cluster overview and behavioral characteristics**

| Profile | N | Percentage | Key characteristics |
|---------|---|------------|---------------------|
| Standard-Use (C0) | 8,198 | 62.8% | Moderate consumption across all dimensions; average household size (2.4); typical appliance ownership |
| Low-Frequency (C2) | 3,318 | 25.4% | Lowest consumption frequencies; smaller households (1.9); elevated eco-behavior scores; minimal leak presence |
| High-Frequency (C1) | 1,545 | 11.8% | Highest consumption frequencies; elevated shower and bath usage; higher leak rates (19.7%); largest household size (2.8) |

Cluster visualization in NMF space (Fig. 2) demonstrates clear separation, with High-Frequency households occupying high values on Component 1 (indoor intensity), while Low-Frequency households show elevated Component 2 (better infrastructure quality).

### 3.3 Statistical validation

All inter-cluster differences achieved statistical significance (p<0.001) across both continuous and categorical variables. Effect size analysis revealed that 79% of continuous variables showed very large effects (η²≥0.14), with boiling frequency demonstrating the largest differentiation (η²=0.87). Categorical variables similarly showed substantial associations (Cramér's V>0.20 for most variables).

Monte Carlo stability analysis yielded ARI=0.981 (95% CI: 0.972–0.989), indicating highly stable cluster assignments across bootstrap samples. Cluster-specific stability showed marginally lower values for the minority High-Frequency cluster (ARI=0.94 vs. 0.99 for Standard-Use), consistent with expected sampling variability for smaller groups.

### 3.4 Sensitivity analysis

Robustness to methodological choices was confirmed across parameter variations. MAD threshold adjustment (0.005–0.02) maintained ARI>0.97. Correlation cutoff variation (0.80–0.90) yielded ARI>0.96. Full covariance GMM substantially outperformed diagonal covariance (ARI 0.98 vs. 0.88), validating elliptical cluster shape assumptions. Complete sensitivity results are provided in Supplementary Materials.

### 3.5 SHAP feature importance

SHAP analysis identified boiling frequency as the primary behavioral differentiator (mean |SHAP|=0.42), followed by shower frequency, bath frequency, garden watering, and household size (Table 2). High-Frequency classification was primarily driven by elevated values across multiple water-use behaviors simultaneously, suggesting a "high-intensity lifestyle" pattern rather than single-behavior dominance.

**Table 2. Top five features by SHAP importance**

| Rank | Feature | Mean |SHAP| | Primary association |
|------|---------|---------|-------------------|
| 1 | Boil-Water-Per-Week | 0.42 | High → C1, Low → C2 |
| 2 | Showers-Per-Week | 0.28 | High → C1 |
| 3 | Bath-Frequency-Per-Week | 0.21 | High → C1 |
| 4 | Garden-Water-Frequency | 0.18 | High → C1 |
| 5 | Household-Size | 0.15 | Large → C1 |

Decision tree rule extraction provided interpretable classification rules: households with boiling frequency >35/week AND shower frequency >10/week were classified as High-Frequency (C1) with 89% precision. Low-Frequency (C2) assignment was indicated by boiling frequency <10/week AND household size <2.5 (precision 91%).

### 3.6 Counterfactual analysis summary

Simulation of behavioral transitions using a trained Random Forest classifier indicated that 64% of High-Frequency households could theoretically achieve Low-Frequency classification through behavioral modification and infrastructure improvement. The primary intervention pathway involved reducing high-frequency behaviors (particularly boiling and showering) combined with leak remediation. Complete methodology and cost-benefit analysis are provided in Supplementary Materials.

---

## 4. Discussion

### 4.1 Key findings

This study developed and validated an integrated framework for survey-informed water demand behavioral profiling, demonstrating three principal contributions. First, MAD-Bootstrap stability selection proved effective for identifying robust behavioral features, achieving 98.1% stability across bootstrap iterations—substantially exceeding typical feature selection approaches. Second, NMF-GMM clustering produced interpretable, three-cluster behavioral profiles with exceptionally high stability (ARI=0.981). Third, SHAP-based explanations successfully translated complex clustering results into actionable insights for utility deployment.

The identified profiles—Standard-Use (62.8%), Low-Frequency (25.4%), and High-Frequency (11.8%)—align with theoretical expectations while providing quantitative precision previously unavailable. The High-Frequency cluster, representing approximately one-ninth of households, exhibits substantially elevated consumption behaviors across multiple dimensions simultaneously, suggesting targeted intervention potential.

### 4.2 Practical implications for utilities

The framework offers several practical deployment pathways for water utilities seeking to optimize demand-side management programs.

**Targeted intervention design**: Rather than universal awareness campaigns, utilities can prioritize resources toward the 11.8% High-Frequency households, where intervention potential is greatest. SHAP feature importance indicates that indoor behaviors (boiling, showering, bathing) should receive primary focus, followed by infrastructure remediation (leak repair).

**Intervention sequencing**: Counterfactual analysis suggests a two-stage intervention strategy: (1) infrastructure assessment and leak remediation, addressing structural barriers to conservation; (2) behavioral nudging targeting high-frequency indoor activities. This sequencing ensures behavioral interventions are not undermined by infrastructure-related water loss.

**Cost-benefit considerations**: Preliminary estimates suggest payback periods of 1.5–4 years for targeted intervention programs, depending on participation rates and behavior change durability. However, these projections require validation with utility-specific cost data before operational deployment. Pilot programs with 500–1,000 households are recommended prior to full-scale implementation.

**System integration**: The framework operates on standard survey and consumption data already collected by most utilities. Real-time implementation would require integration with customer information systems, with cluster assignments updated periodically (annually or upon significant consumption changes). Decision tree rules enable field-deployable classification without requiring complex model infrastructure.

**Customer communication**: Neutral behavioral labels (Standard-Use, High-Frequency, Low-Frequency) avoid stigmatizing customers while enabling differentiated engagement strategies. High-Frequency households might receive personalized water-saving recommendations and rebate offers, while Standard-Use households receive general conservation messaging.

### 4.3 Comparison with current practice

The proposed framework offers advantages over volumetric quartile-based segmentation commonly used by utilities. Behavioral clustering achieves substantially higher stability (ARI=0.98 vs. estimated 0.72 for k-means on raw features) while providing interpretable behavioral drivers through XAI. However, it requires richer input data (surveys) compared to meter-only approaches. The optimal deployment may combine behavioral profiling with volumetric monitoring for comprehensive demand characterization.

### 4.4 Limitations and future work

Several limitations warrant acknowledgment. First, cross-sectional survey data cannot capture temporal behavioral dynamics; longitudinal panel data would strengthen intervention response modeling. Second, the single-region focus (Yorkshire, UK) limits immediate generalizability; validation across multiple utilities with varying climates and demographics is recommended before broader conclusions. Third, the study did not test for disparate impact across protected demographics; fairness audits should precede operational deployment to ensure equitable treatment across income brackets and household types. Fourth, counterfactual projections assume behavioral changes are achievable and sustained, which requires empirical validation through intervention trials.

Future research should prioritize multi-utility replication, longitudinal behavioral tracking, and randomized controlled trials of targeted intervention effectiveness. Integration with smart meter data at higher temporal resolution could enhance behavioral profiling precision.

---

## 5. Conclusions

This study presents a robust machine learning framework for survey-informed water demand behavioral profiling, integrating MAD-Bootstrap feature selection, NMF dimensionality reduction, GMM probabilistic clustering, and SHAP-based explainability. Application to 13,061 UK households identified three behaviorally distinct profiles with high stability (ARI=0.981) and strong statistical differentiation.

The 11.8% High-Frequency cluster represents a priority target for demand-side management, with clear behavioral drivers identified through SHAP analysis. The framework provides water utilities with interpretable, validated household segmentation enabling transition from universal conservation programs toward efficient, targeted interventions. Estimated cost-benefit ratios are favorable, though operational validation is recommended through pilot deployment.

As water scarcity pressures intensify globally, data-driven behavioral profiling offers a pathway toward more effective, equitable demand management. The interpretable, robust approach developed here contributes to building trust between complex machine learning capabilities and utility decision-makers responsible for sustainable water resource stewardship.

---

## Acknowledgements

[Removed for double-blind review]

---

## References

Beal, C.D., Stewart, R.A., Fielding, K., 2013. A novel mixed method smart metering approach to reconciling differences between perceived and actual residential end use water consumption. J. Clean. Prod. 60, 116–128. https://doi.org/10.1016/j.jclepro.2011.09.007.

Cardell-Oliver, R., Wang, J., Gigney, H., 2016. Smart meter analytics to pinpoint opportunities for reducing household water use. J. Water Resour. Plan. Manag. 142(6), 04016007. https://doi.org/10.1061/(ASCE)WR.1943-5452.0000634.

Cominola, A., Giuliani, M., Piga, D., Castelletti, A., Rizzoli, A.E., 2015. Benefits and challenges of using smart meters for advancing residential water demand modeling and management: A review. Environ. Model. Softw. 72, 198–214. https://doi.org/10.1016/j.envsoft.2015.07.012.

Cominola, A., Giuliani, M., Castelletti, A., Fraternali, P., Herrera, S., Guardiola, J., Jacucci, G., 2019. Data mining to uncover heterogeneous water use behaviors from smart meter data. Water Resour. Res. 55(11), 9315–9333. https://doi.org/10.1029/2019WR024897.

Dormann, C.F., Elith, J., Bacher, S., Buchmann, C., Carl, G., Carré, G., Marquéz, J.R.G., Gruber, B., Lafourcade, B., Leitão, P.J., Münkemüller, T., McClean, C., Osborne, P.E., Reineking, B., Schröder, B., Skidmore, A.K., Zurell, D., Lautenbach, S., 2013. Collinearity: a review of methods to deal with it and a simulation study evaluating their performance. Ecography 36(1), 27–46. https://doi.org/10.1111/j.1600-0587.2012.07348.x.

Gleick, P.H., 2018. Transitions to freshwater sustainability. Proc. Natl. Acad. Sci. 115(36), 8863–8871. https://doi.org/10.1073/pnas.1808893115.

Lee, D.D., Seung, H.S., 1999. Learning the parts of objects by non-negative matrix factorization. Nature 401(6755), 788–791. https://doi.org/10.1038/44565.

Lundberg, S.M., Lee, S.I., 2017. A unified approach to interpreting model predictions. In: Advances in Neural Information Processing Systems 30. Curran Associates, Red Hook, pp. 4765–4774.

Meinshausen, N., Bühlmann, P., 2010. Stability selection. J. R. Stat. Soc. Ser. B 72(4), 417–473. https://doi.org/10.1111/j.1467-9868.2010.00740.x.

Stewart, R.A., Willis, R.M., Giurco, D., Panuwatwanich, K., Capati, G., 2010. Web-based knowledge management system: linking smart metering to the future of urban water planning. Aust. Plan. 47(2), 66–74. https://doi.org/10.1080/07293681003767769.

Tukey, J.W., 1977. Exploratory Data Analysis. Addison-Wesley, Reading.

Xenochristou, M., Kapelan, Z., Hutton, C., Hofman, J., 2020. Water demand forecasting accuracy and influencing factors at different spatial scales using a Gradient Boosting Machine. Water Resour. Res. 56(8), e2019WR026304. https://doi.org/10.1029/2019WR026304.
