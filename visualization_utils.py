import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUTPUT_DIR = r'profiling'

def plot_optimization_results(results_path):
    """Plots stability and silhouette scores from the grid search."""
    df = pd.read_csv(results_path)
    
    # Pivot for Heatmap
    stability_pivot = df.pivot(index='n_nmf', columns='n_gmm', values='stability')
    silhouette_pivot = df.pivot(index='n_nmf', columns='n_gmm', values='silhouette')
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    sns.heatmap(stability_pivot, annot=True, cmap='viridis', ax=axes[0])
    axes[0].set_title('Stability Score (Target > 0.75)')
    
    sns.heatmap(silhouette_pivot, annot=True, cmap='magma', ax=axes[1])
    axes[1].set_title('Silhouette Score')
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'optimization_heatmap.png'))
    print("Saved optimization_heatmap.png")

def plot_cluster_profiles(df, cluster_col='Cluster'):
    """Plots the mean values of features for each cluster (Heatmap)."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [c for c in numeric_cols if c not in [cluster_col, 'Max_Prob']]
    
    # Calculate means
    means = df.groupby(cluster_col)[numeric_cols].mean()
    
    # Normalize for visualization (Z-score per feature)
    means_norm = (means - means.mean()) / means.std()
    
    plt.figure(figsize=(14, 10))
    sns.heatmap(means_norm.T, cmap='RdBu_r', center=0, annot=False)
    plt.title('Cluster Profiles (Normalized Feature Means)')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'cluster_profiles_heatmap.png'))
    print("Saved cluster_profiles_heatmap.png")

def plot_stability_distribution(stability_scores):
    """Plots the histogram of household stability scores."""
    plt.figure(figsize=(10, 6))
    sns.histplot(stability_scores, bins=20, kde=True)
    plt.axvline(x=0.75, color='r', linestyle='--', label='Target Threshold')
    plt.title('Distribution of Household Stability Scores')
    plt.xlabel('Stability Score')
    plt.legend()
    plt.savefig(os.path.join(OUTPUT_DIR, 'stability_distribution.png'))
    print("Saved stability_distribution.png")

if __name__ == "__main__":
    # Test run
    results_path = os.path.join(OUTPUT_DIR, 'optimization_results_enhanced.csv')
    if os.path.exists(results_path):
        plot_optimization_results(results_path)
        
    data_path = os.path.join(OUTPUT_DIR, 'clustered_data_enhanced.csv')
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        plot_cluster_profiles(df)
