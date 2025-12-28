# =============================================================================
# Water Demand Behavioral Profiling
# Source Package Initialization
# =============================================================================
"""
Water Demand Behavioral Profiling Framework

A robust machine learning framework for survey-informed water demand 
behavioral profiling with explainable AI (XAI).

Modules:
    - pipeline: Main analysis pipeline (xclustering)
    - preprocessing: Data cleaning and preprocessing
    - feature_selection: MAD-Bootstrap feature selection
    - validation: Statistical validation and sensitivity analysis
    - xai: Explainable AI (SHAP, decision rules, counterfactuals)
    - visualization: Figure generation utilities

Usage:
    from src.pipeline.xclustering_pipeline_enhanced import XClusteringPipeline
    
    pipeline = XClusteringPipeline(data_path="data/survey.csv")
    results = pipeline.run()

Authors:
    Mohammed Laouadi, Mohamed Kissi, Omar El Beggar
    Laboratory LIM FSTM, University Hassan II Mohammedia, Morocco

License:
    MIT License
"""

__version__ = "1.0.0"
__author__ = "Mohammed Laouadi, Mohamed Kissi, Omar El Beggar"
__email__ = "mohammedlaouadi5@gmail.com"

# Package-level imports for convenience
# Uncomment when modules are properly organized
# from .pipeline import XClusteringPipeline
# from .xai import run_shap_analysis
