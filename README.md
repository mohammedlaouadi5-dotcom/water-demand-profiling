# Water Demand Behavioral Profiling Framework

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.xxxx%2Fxxxxx-blue)](https://doi.org/10.xxxx/xxxxx)

A robust machine learning framework for survey-informed water demand behavioral profiling with explainable AI (XAI) for targeted intervention design.

## 📖 Overview

This repository contains the code for the paper:

> **Survey-informed water demand behavioral profiling: a robust machine learning framework with explainable AI for targeted intervention design**
> 
> Laouadi, M., Kissi, M., & El Beggar, O. (2024)
> 
> *Water Science and Engineering* (under review)

## 🎯 Key Features

- **MAD-Bootstrap Feature Selection**: Robust stability-based feature selection (97→18 features)
- **NMF Dimensionality Reduction**: Interpretable latent components (K=2)
- **GMM Clustering**: Probabilistic behavioral profiling (K=3 clusters)
- **SHAP Explainability**: Feature importance and decision rules
- **Monte Carlo Validation**: Cluster stability analysis (ARI=0.981)

## 📊 Results Summary

| Cluster | N | % | Description |
|---------|---|---|-------------|
| Standard-Use (C0) | 8,198 | 62.8% | Moderate consumption patterns |
| Low-Frequency (C2) | 3,318 | 25.4% | Eco-conscious, smaller households |
| High-Frequency (C1) | 1,545 | 11.8% | Elevated consumption, intervention targets |

## 🗂️ Repository Structure

```
water-demand-profiling/
├── README.md
├── LICENSE
├── requirements.txt
├── environment.yml
├── .gitignore
│
├── src/                          # Source code
│   ├── __init__.py
│   ├── pipeline/                 # Main analysis pipeline
│   │   ├── xclustering_pipeline.py
│   │   └── xclustering_pipeline_enhanced.py
│   │
│   ├── preprocessing/            # Data preprocessing
│   │   ├── analyze_csv.py
│   │   └── analyze_csv_native.py
│   │
│   ├── feature_selection/        # Feature selection methods
│   │   └── compare_feature_selection.py
│   │
│   ├── validation/               # Statistical validation
│   │   ├── statistical_validation.py
│   │   ├── statistical_enhancement.py
│   │   ├── verify_cluster_sizes.py
│   │   └── validate_methodological_assumptions.py
│   │
│   ├── xai/                      # Explainable AI
│   │   ├── xai_shap_analysis.py
│   │   ├── xai_shap_enhanced.py
│   │   ├── xai_rule_extraction.py
│   │   ├── xai_rules_enhanced.py
│   │   └── xai_counterfactuals.py
│   │
│   └── visualization/            # Plotting utilities
│       ├── visualization_utils.py
│       ├── generate_manuscript_figures.py
│       ├── generate_supplementary_figures.py
│       ├── generate_pipeline_figure.py
│       ├── generate_shap_dependence_plots.py
│       └── generate_nmf_interpretability_diagram.py
│
├── data/                         # Data directory (not tracked)
│   ├── raw/                      # Original survey data
│   └── processed/                # Processed outputs
│
├── figures/                      # Generated figures
│   ├── main/                     # Main manuscript figures
│   └── supplementary/            # Supplementary figures
│
├── results/                      # Analysis outputs
│   ├── clusters/
│   ├── validation/
│   └── xai/
│
└── notebooks/                    # Jupyter notebooks (optional)
    └── exploratory_analysis.ipynb
```

## ⚙️ Installation

### Option 1: Conda (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/water-demand-profiling.git
cd water-demand-profiling

# Create conda environment
conda env create -f environment.yml
conda activate water-profiling
```

### Option 2: pip

```bash
# Clone the repository
git clone https://github.com/yourusername/water-demand-profiling.git
cd water-demand-profiling

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Quick Start

```python
from src.pipeline.xclustering_pipeline_enhanced import XClusteringPipeline

# Initialize pipeline
pipeline = XClusteringPipeline(
    data_path="data/raw/survey_data.csv",
    n_clusters=3,
    n_components=2
)

# Run full analysis
results = pipeline.run()

# Access results
clusters = results['cluster_labels']
shap_values = results['shap_importance']
```

### Step-by-Step Analysis

```python
# 1. Data Preprocessing
from src.preprocessing.analyze_csv import preprocess_data
data = preprocess_data("data/raw/survey_data.csv")

# 2. Feature Selection (MAD-Bootstrap)
from src.feature_selection.compare_feature_selection import mad_bootstrap_selection
selected_features = mad_bootstrap_selection(data, threshold=0.01, n_iterations=100)

# 3. Clustering
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3, covariance_type='full')
clusters = gmm.fit_predict(data[selected_features])

# 4. SHAP Analysis
from src.xai.xai_shap_enhanced import run_shap_analysis
shap_results = run_shap_analysis(data, clusters)
```

### Generate Figures

```bash
# Generate all manuscript figures
python src/visualization/generate_manuscript_figures.py

# Generate supplementary figures
python src/visualization/generate_supplementary_figures.py
```

## 📊 Data Requirements

The framework expects survey data with the following structure:

| Column Type | Examples |
|-------------|----------|
| Behavioral frequencies | `showers_per_week`, `baths_per_week`, `boil_water_per_week` |
| Appliance ownership | `has_dishwasher`, `has_washing_machine` |
| Infrastructure | `leak_presence`, `tap_type` |
| Demographics | `household_size`, `dwelling_type` |

**Note**: Original survey data is not included due to privacy restrictions. Contact the corresponding author for data access requests.

## 📈 Reproducibility

To reproduce the results from the paper:

```bash
# Run the complete pipeline
python src/pipeline/xclustering_pipeline_enhanced.py \
    --input data/processed/survey_data_cleaned.csv \
    --output results/ \
    --n_clusters 3 \
    --n_components 2 \
    --bootstrap_iterations 100
```

Expected outputs:
- Cluster assignments: `results/clusters/cluster_labels.csv`
- Validation metrics: `results/validation/metrics.json`
- SHAP importance: `results/xai/shap_importance.csv`
- Figures: `figures/main/` and `figures/supplementary/`

## 🧪 Testing

```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 📝 Citation

If you use this code, please cite:

```bibtex
@article{laouadi2024water,
  title={Survey-informed water demand behavioral profiling: a robust machine learning framework with explainable AI for targeted intervention design},
  author={Laouadi, Mohammed and Kissi, Mohamed and El Beggar, Omar},
  journal={Water Science and Engineering},
  year={2024},
  publisher={Elsevier}
}
```

## 📧 Contact

- **Mohammed Laouadi** (Corresponding Author)
  - Email: [mohammedlaouadi5@gmail.com](mailto:mohammedlaouadi5@gmail.com)
  - ORCID: [0009-0009-5504-3167](https://orcid.org/0009-0009-5504-3167)

- **Mohamed Kissi**
  - Email: [mohamed.kissi@fstm.ac.ma](mailto:mohamed.kissi@fstm.ac.ma)
  - ORCID: [0000-0003-4099-6992](https://orcid.org/0000-0003-4099-6992)

- **Omar El Beggar**
  - Email: [omar.elbeggar@fstm.ac.ma](mailto:omar.elbeggar@fstm.ac.ma)
  - ORCID: [0000-0002-5122-3322](https://orcid.org/0000-0002-5122-3322)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Yorkshire Water for providing access to household survey data
- Laboratory LIM FSTM, University Hassan II Mohammedia, Morocco
