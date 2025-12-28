Ce document a été élaboré pour la restructuration et la mise en œuvre de votre nouvelle équipe de Data Science (DS), chargée du projet **XClustering Comportemental** (découlant du cadre KOGAMI) pour le secteur de l'eau. Il sert de feuille de route complète et de matrice de responsabilité pour assurer un niveau de rigueur élevé (Journal Q1).

---

## DOCUMENT DE SPÉCIFICATION ORGANISATIONNELLE ET MÉTHODOLOGIQUE : PROJET XCLUSTERING COMPORTEMENTAL

| Rév. | Date | Auteur | Validé par |
| :--- | :--- | :--- | :--- |
| **V1.0** | Dec. 2025 | Relecteur Académique Senior | Client / Management DS |

### 0. Contexte et Vision du Projet (The *North Star*)

*   **Objectif Stratégique (La Cible Q1) :** Établir une méthode scientifique **robuste (Statistiquement Validée)**, **interprétable (Explicable)** et **opérationnelle (Actionnable)** pour segmenter les foyers non plus sur la base des volumes d'eau agrégés (limite de l'état de l'art), mais sur leurs **Routines Comportementales Latentes** (*End-Use Proxies*) afin de personnaliser les incitations de gestion de la demande (DSM) et modéliser l'**Inertie/Résistance au Changement ($\boldsymbol{m}$ de KOGAMI)**.
*   **Gap Technique à Combler :** La littérature a validé l'existence de routines (*Cominola 2019*), mais **échoue à fournir des Explications de Cluster basées sur des Règles (XAI/Rule-Lists)** ou une **Validation Externe Statistique rigoureuse** des profils par rapport aux croyances déclarées (*Beal 2013*). Notre projet synthétise et dépasse ces limites.
*   **Données Clés :** **Yorkshire Water Dataset** (avec ses *features* étendues de volumes/fréquence/durée) $\boldsymbol{+}$ **Données d'Enquête Comportementale/Attitudinale**.

---

### 1. Organisation de l'Équipe et Matrice des Rôles Principaux

Une approche structurée requiert des rôles spécialisés mais interdépendantes.

| Rôle | Expertise Principale | Responsabilités Générales (Accountability - Le *Boss*) |
| :--- | :--- | :--- |
| **Chef de Projet/Architecte PL** | Leadership, alignement stratégique, KOGAMI | **Propriété** de l'intégrité de la pipeline de la donnée brute à la règle XAI. **Garantit le niveau Q1** de l'Artefact final. |
| **Data Engineer (DE)** | Ingénierie des données, robustesse ML, Imputation. | **Responsable** de la préparation du Dataset, de la normalisation NMF, et de la validation de la **robustesse (Monte-Carlo)**. |
| **Data Scientist/ML Engineer (MLE)** | Modélisation non-supervisée (NMF, GMM), Performance/Tuning. | **Responsable** de la découverte des **Clusters ($P_k$)**, du choix des modèles de Clustering/Réduction de dimension (NMF/GMM), et du **support des Experts XAI/Stat.** |
| **Expert XAI/Statisticien (BSS)** | Psychologie Comportementale, Hypothèses Statistique ($p$-value), Interprétation Causalité. | **Responsable** de l'**Explicabilité des résultats (SHAP/Rules)** et de la **Signification Statistique (ANOVA)**, comblant le Gap XAI/Perception. |

---

### 2. Spécifications Détaillées des Phases de Travail (Workstreams)

Les étapes critiques sont divisées en tâches, chaque sous-tâche étant l'artefact technique minimal nécessaire pour garantir la qualité de la phase suivante.

#### Workstream I : Data Preparation et Feature Augmentation (Phase 1 du Modèle)

| Rôles Dirigeants | Tâches (R: Responsabilité Primaire / C: Consulting / I: Informé) |
| :--- | :--- |
| **R/C/I** | **Tâches et Sous-tâches Spécifiques (Must-Have Q1)** |
| DE / DA / PL | **T.1 : Fusion et Nettoyage de la Donnée** |
| | S-T 1.1 : Jointure des Données Compteur (Proxies Comportementaux EUD) et Enquête (Attitudinale/Socio-Démo) au niveau du foyer. |
| | S-T 1.2 : Traitement des valeurs manquantes : **Imputation par mode** (catégorielles), **médiane** (numériques), justifiant la méthode (car le *clusteuring* y est sensible). |
| DE / MLE / BSS | **T.2 : Ingénierie des Features XClustering (Lien d'Attribution)** |
| | S-T 2.1 : **Sélection de Features Avancée (RFE)** : Utilisation de *Recursive Feature Elimination* pour sélectionner les variables les plus discriminantes et réduire le bruit (Target: < 200 features). |
| | S-T 2.2 : Application de **MinMaxScaler** (Strictement requis pour NMF) pour garantir la non-négativité, et **One-Hot Encoding** pour les catégorielles. |
| **Artefact Clé du Workstream :** La Matrice de Feature $\boldsymbol{F_{Scaled}}$, prête pour le NMF (avec les variables d'enquête en *collab-data* non utilisées directement par NMF).

#### Workstream II : Extraction des Routines et Segmentation (*XClustering*)

| Rôles Dirigeants | Tâches (R: Responsabilité Primaire / C: Consulting / I: Informé) |
| :--- | :--- |
| MLE / DE / PL | **T.3 : Réduction de Dimension (Feature Dénominateur Commun Interprétable)** |
| | S-T 3.1 : Remplacement de l'approche PCA (*Eigenbehavior Cominola*) par la **NMF** pour extraire $\boldsymbol{K_{NMF}}$ composantes (matrices $W$ et $H$). **NMF est utilisé comme proxy de *Routine Expliquable***. |
| | S-T 3.2 : Analyse de la *novelty* du $NMF$ par les **Charges $H$** (prouver la sémantique de chaque *Eigenbehavior*). |
| MLE / BSS / PL | **T.4 : Clustering Probabiliste de Foyers (Groupes de Consommateurs)** |
| | S-T 4.1 : Exécution du Clustering par **GMM (Gaussian Mixture Model)** pour capter le *Soft Membership* des foyers. |
| | S-T 4.2 : **Optimisation de la Stabilité (Grid Search)** : Itération sur $K_{NMF}$ et $K_{GMM}$ pour maximiser le **Score de Stabilité** (> 100 itérations). Sélection de la configuration offrant le meilleur compromis Stabilité/Silhouette. |
| **Artefact Clé du Workstream :** La Matrice de **Scores d'Appartenance (Soft/Floue) W**, donnant $\boldsymbol{W_{ij} \in [0, 1]}$ : la probabilité/poids du Foyer $i$ d'appartenir à la Routine $j$.

#### Workstream III : Validation Comportementale et Robustesse

| Rôles Dirigeants | Tâches (R: Responsabilité Primaire / C: Consulting / I: Informé) |
| :--- | :--- |
| **BSS / MLE / PL** | **T.5 : Validation Statistique du Sens des Clusters** |
| | S-T 5.1 : Validation Externe Catégorielle : Test du **Chi-carré** avec calcul de la **Taille d'Effet (Cramer's V)** pour quantifier la force de l'association. |
| | S-T 5.2 : Validation Externe Numérique : **ANOVA** complète rapportant **F-ratio**, **Valeur $p$**, et **Taille d'Effet (Eta-squared $\eta^2$)**. Suivi de tests **Post-Hoc Tukey HSD** pour les différences par paire. |
| DE / MLE / BSS | **T.6 : Validation de la Robustesse et Propagation d'Incertitude** |
| | S-T 6.1 : Test de **Stabilité des Clusters (Simulations Monte-Carlo)** : Répéter le GMM $\ge 100$ fois avec des initialisations aléatoires (*random seeds*) ou du *Bootstrap* (sous-échantillonnage avec remplacement). |
| | S-T 6.2 : Calculer la **métrique de Robustesse** (Taux d'Assignation Stable par foyer, Mesure de **l'Inertie Comportementale $\boldsymbol{m}$**). |
| **Artefact Clé du Workstream :** **Matrice des $p$-values** $\boldsymbol{(\boldsymbol{\text{Validez statistiquement le lien Cluter} \leftrightarrow \text{Croyance Humaine)}}$ et un **Rapport de Robustesse** (*Mean Stable Membership Rate*) quantifiant la confiance du cluster $P_k$.

#### Workstream IV : Explicabilité et Modélisation Prescriptive (XAI Final)

| Rôles Dirigeants | Tâches (R: Responsabilité Primaire / C: Consulting / I: Informé) |
| :--- | :--- |
| **XAI / MLE / BSS** | **T.7 : Explication des Règles Globales et du Rebond (Explicabilité du Profil)** |
| | S-T 7.1 : Extraction de **Règles Logiques Globales (Rule-Lists)** via un classifieur simple (arbre de décision) entraîné pour **prédire l'appartenance au cluster** ($P_k$). Règle finale : **"IF Feature A $> X$ THEN Cluster $\approx P_{k}$"**. |
| | S-T 7.2 : Validation XAI Locale (SHAP) : Entraîner un *proxy classifier* (XGBoost) pour générer les **valeurs SHAP** (contribution locale des features à la décision de cluster) sur la matrice de features d'origine. |
| XAI / PL / BSS | **T.8 : Counterfactuals et Intégration KOGAMI (La Valeur Prédictrice)** |
| | S-T 8.1 : Dérivation de 3 à 5 scénarios de **Contre-Factuels (DiCE ou Optimisation)** : Pour le Foyer $X \in P1$, quel **changement minimal et faisable de Feature** (ex : réduire le temps de douche de $\min \Delta \text{minutes}$) lui ferait basculer vers un cluster $P_3$ plus efficient ? |
| | S-T 8.2 : Formalisation du lien **KOGAMI :** Mapping entre la **Robustesse $m$** (Output D) et l'**Inertie/Résistance Comportementale $m$** dans le modèle Lewin/Kotter (Plus la stabilité/robustesse de $P_k$ est haute, plus l'inertie $m$ est haute). |
| **Artefact Clé du Workstream :** **Explanations Set** (*Rule-Lists, SHAP Values Chart*) et le **Fichier d'Intervention Prét-à-l'Agent** (mapping Cluster $\rightarrow$ Inertie $m$ $\rightarrow$ Counterfactual Rule).

---

### 3. Conclusion et Critères d'Acceptation Q1

| Exigence | Critère d'Acceptation (PL Vetting) |
| :--- | :--- |
| **Validation du Sense** | Toutes les variables *Survey* ($\chi^2$/ANOVA) montrent une **Différence Statistique Significative** $\boldsymbol{(p < 0.05)}$ entre les clusters d'usages trouvés. |
| **Interprétabilité** | Le *Senior Data Scientist* doit pouvoir labéliser les 5 clusters majeurs avec des étiquettes sémantiques fortes (Ex: *Rebound Effect Users*, *Hyper-Conservers Overestimating*, *Tense Low Users*). |
| **Robustesse** | La mesure de **Robustesse Monte-Carlo** doit être maximisée via l'optimisation. Si < 75% (comme observé : 43.5%), cela doit être interprété comme une **Fluidité Comportementale** significative (Contribution Scientifique). |
| **Nouveauté & Implication Q1**| L'article doit intégrer les résultats de **SHAP/DiCE** et d'**ANOVA/Valeur $p$** pour former une narration causale répondant explicitement aux Gaps non résolus par *Cominola (2019)* et *Beal (2013)*. |