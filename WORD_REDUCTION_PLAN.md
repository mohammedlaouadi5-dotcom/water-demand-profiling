# PLAN DE RÉDUCTION - Water Science and Engineering
## Limite: ≤6,000 mots

---

# RÉSUMÉ DE LA RÉDUCTION

| Section | Mots Actuels | Mots Cibles | Réduction | % |
|---------|--------------|-------------|-----------|---|
| Abstract | 280 | 180 | -100 | -36% |
| Introduction | 2,000 | 900 | -1,100 | -55% |
| Methods | 3,500 | 1,800 | -1,700 | -49% |
| Results | 2,500 | 1,500 | -1,000 | -40% |
| Discussion | 2,000 | 600 | -1,400 | -70% |
| Conclusions | 350 | 250 | -100 | -29% |
| Acknowledgements | 50 | 50 | 0 | 0% |
| **TOTAL** | **10,680** | **5,280** | **-5,400** | **-51%** |

**Buffer restant**: ~720 mots pour ajustements

---

# DÉTAIL PAR SECTION

---

## 1. ABSTRACT (280 → 180 mots)

### Contenu Actuel à Conserver:
- ✅ Objectif de recherche
- ✅ Méthodologie (MAD-Bootstrap, NMF, GMM)
- ✅ Résultats principaux (3 clusters, %)
- ✅ Conclusion principale

### Contenu à Supprimer:
- ❌ Détails SHAP
- ❌ Counterfactual analysis (mentionner en 1 phrase)
- ❌ Effet sizes détaillés

### Texte Proposé (~180 mots):

> Effective water demand management requires understanding heterogeneous household behaviors. This study develops a machine learning framework integrating survey-informed features, robust feature selection, and explainable AI to profile residential water demand. Using data from 13,061 UK households with 97 behavioral variables, MAD-Bootstrap stability selection retained 18 robust features. Non-negative Matrix Factorization reduced dimensionality to two interpretable components, and Gaussian Mixture Models identified three distinct behavioral profiles: Standard-Use (62.8%), Low-Frequency (25.4%), and High-Frequency (11.8%). Monte Carlo validation confirmed high cluster stability (ARI = 0.981). All differences achieved statistical significance with very large effect sizes. SHAP analysis identified boiling frequency, shower habits, and garden watering as primary differentiators, enabling targeted intervention design. The framework provides water utilities with interpretable household segmentation for demand-side management, with potential for improved resource allocation efficiency.

---

## 2. INTRODUCTION (2,000 → 900 mots)

### Structure Proposée:

| Sous-section | Mots | Contenu |
|--------------|------|---------|
| 1.1 Background | 200 | Contexte global eau, UK challenges |
| 1.2 Literature Review | 400 | Bref (pas de sous-sections détaillées) |
| 1.3 Research Gap | 150 | Gap clairement identifié |
| 1.4 Objectives | 150 | 3-4 objectifs |
| **Total** | **900** | |

### Contenu à Supprimer:
- ❌ Section 1.3.4 (Recent Advances 2020-2024) → Fusionner en 2-3 phrases
- ❌ Section 1.3.5 (Methodological Synthesis) → Intégrer dans Gap
- ❌ Section 1.6 (Paper Structure) → Pas nécessaire
- ❌ Sous-sections numérotées dans Lit Review → Paragraphes continus

### Structure Révisée:

```
1. Introduction (900 mots)
   1.1 Background and problem statement (200 mots)
   1.2 Literature review (400 mots)
       - Traditional approaches (1 paragraphe)
       - ML approaches and limitations (1 paragraphe)
       - Research gap (1 paragraphe)
   1.3 Objectives (150 mots)
       - 4 objectifs numérotés
```

---

## 3. METHODS (3,500 → 1,800 mots)

### Structure Proposée:

| Sous-section | Mots | Contenu |
|--------------|------|---------|
| 2.1 Data | 200 | Study area, sample, variables |
| 2.2 Preprocessing | 250 | Imputation, outliers (bref) |
| 2.3 Feature Selection | 300 | MAD-Bootstrap algorithm |
| 2.4 NMF | 200 | Formulation, K=2 justification |
| 2.5 GMM Clustering | 250 | BIC selection, configuration |
| 2.6 Validation | 250 | Internal metrics + Monte Carlo |
| 2.7 XAI | 200 | SHAP surrogate approach |
| 2.8 Counterfactual | 150 | Bref résumé (détails en Suppl.) |
| **Total** | **1,800** | |

### Contenu à Déplacer vers Supplementary:
- → Section 2.3.1 (Categorical KNN details)
- → Section 2.3.3 (Consistency corrections details)
- → Section 2.5.3 (NMF interpretability diagram)
- → Section 2.6.3 (Assignment confidence distribution)
- → Section 2.7.4 (Power analysis details)
- → Section 2.9.4 (Counterfactual limitations - garder 2 phrases)

### Contenu à Supprimer Complètement:
- ❌ Pseudocode détaillé
- ❌ BIC vs AIC table complète (garder: "K=3 optimal, BIC=-55,450")
- ❌ Confusion matrix détaillée (garder: "surrogate accuracy 97.8%")

---

## 4. RESULTS (2,500 → 1,500 mots)

### Structure Proposée:

| Sous-section | Mots | Contenu |
|--------------|------|---------|
| 3.1 Feature Selection | 200 | 18 features, top 5 |
| 3.2 Cluster Characterization | 500 | 3 clusters, profiles, Table |
| 3.3 Statistical Validation | 300 | ANOVA/Chi², effect sizes |
| 3.4 Stability Analysis | 200 | ARI, sensitivity (brief) |
| 3.5 XAI Results | 300 | SHAP top features, 2 rules |
| **Total** | **1,500** | |

### Contenu à Déplacer vers Supplementary:
- → Table S1: Full feature list
- → Table S2: Complete ANOVA results
- → Table S3: Chi-square results
- → Table S4: Sensitivity analysis details
- → Figure S5-S7: Detailed plots

### Contenu à Supprimer:
- ❌ Section 3.5.3 (Interaction Effects) → 1 phrase seulement
- ❌ Section 3.6 (Counterfactual Results) → Fusionner avec Discussion

---

## 5. DISCUSSION (2,000 → 600 mots)

### Structure Proposée:

| Sous-section | Mots | Contenu |
|--------------|------|---------|
| 4.1 Key Findings | 150 | Résumé 3 points principaux |
| 4.2 Practical Implications | 200 | Utility deployment, intervention |
| 4.3 Limitations | 150 | 4-5 limitations courtes |
| 4.4 Future Work | 100 | 2-3 directions |
| **Total** | **600** | |

### Contenu à Supprimer:
- ❌ Section 4.2 (Methodological Contributions) → Intégrer en 2 phrases
- ❌ Section 4.3 (Comparison with Prior Work) → 1 phrase
- ❌ Section 4.5.3 (Ethical Considerations) → 2 phrases dans Limitations
- ❌ Section 4.6 (Generalizability) → 1 phrase dans Limitations
- ❌ Benchmarking table → Supplementary

### Style:
- Paragraphes continus sans sous-titres
- Maximum 2-3 paragraphes

---

## 6. CONCLUSIONS (350 → 250 mots)

### Contenu:
- ✅ Résumé contribution principale
- ✅ 3 key findings
- ✅ Practical recommendation
- ✅ Call for future validation

### Style:
- Un seul paragraphe fluide
- Pas de listes numérotées

---

# SUPPLEMENTARY MATERIALS

## Contenu Déplacé:

| Item | Type | À Déplacer de |
|------|------|---------------|
| Table S1 | Feature list (97→18) | Methods 2.3 |
| Table S2 | Complete ANOVA results | Results 3.3 |
| Table S3 | Chi-square results | Results 3.3 |
| Table S4 | Sensitivity analysis | Results 3.4 |
| Table S5 | Summary statistics | Results 3.2 |
| Table S6 | SHAP surrogate confusion matrix | Methods 2.7 |
| Figure S1-S8 | All supplementary figures | Various |
| Text S1 | Categorical KNN protocol | Methods 2.2 |
| Text S2 | Counterfactual methodology details | Methods 2.8 |
| Text S3 | Ethical considerations | Discussion |

---

# FIGURES DANS LE MANUSCRIT PRINCIPAL

## Garder (4-5 figures max recommandé):

| Figure | Contenu | Justification |
|--------|---------|---------------|
| Fig. 1 | Analytical Pipeline | Vue d'ensemble méthodologie |
| Fig. 2 | Cluster Visualization | Résultat principal |
| Fig. 3 | Behavioral Profiles Radar | Caractérisation clusters |
| Fig. 4 | SHAP Feature Importance | XAI résultat |

## Déplacer vers Supplementary:

- Figure 5 (Validation Metrics) → Figure S1
- Figure 6 (NMF Selection) → Figure S2
- All S1-S8 → Supplementary

---

# TABLES DANS LE MANUSCRIT PRINCIPAL

## Garder (2-3 tables max):

| Table | Contenu | Mots estimés |
|-------|---------|--------------|
| Table 1 | Cluster Overview (3 rows) | ~100 |
| Table 2 | Top 5 SHAP Features | ~80 |

## Déplacer vers Supplementary:

- Table complète ANOVA → Table S2
- Table Chi-square → Table S3
- Table Sensitivity → Table S4

---

# CHECKLIST DE VALIDATION

## Avant Génération:

- [ ] Abstract ≤200 mots
- [ ] Introduction ≤1,000 mots (pas de sous-sous-sections)
- [ ] Methods ≤2,000 mots
- [ ] Results ≤1,500 mots
- [ ] Discussion ≤700 mots
- [ ] Conclusions ≤300 mots
- [ ] Total ≤6,000 mots
- [ ] ≤5 figures main text
- [ ] ≤3 tables main text
- [ ] Supplementary Materials préparés

---

# QUESTION POUR VOUS

Avant de générer le manuscrit condensé, confirmez:

1. ✅ **Abstract 180 mots** - OK?
2. ✅ **Introduction sans sous-sous-sections** - OK?
3. ✅ **Counterfactual en Supplementary** - OK?
4. ✅ **4 figures principales** - OK?
5. ✅ **Ethical considerations en 2 phrases** - OK?

---

**Dès votre confirmation, je génère le manuscrit complet format WSE.**
