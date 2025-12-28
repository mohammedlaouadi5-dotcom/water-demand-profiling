"""
Deep Behavioral Analysis - Multi-Dimensional Cluster Profiling
Extends XClustering results with behavioral adjustments and composite scores
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
DATA_PATH = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\clustered_data_enhanced.csv'
OUTPUT_DIR = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling'

def load_data():
    """Load clustered data"""
    print("Loading clustered data...")
    df = pd.read_csv(DATA_PATH)
    print(f"Shape: {df.shape}")
    print(f"Clusters: {df['Cluster'].nunique()}")
    return df

def calculate_per_capita_metrics(df):
    """Calculate per-capita normalized metrics"""
    print("\n=== Calculating Per-Capita Metrics ===")
    
    # Avoid division by zero
    people = df['Number-Of-People'].replace(0, 1)
    
    # Per-capita consumption
    if 'Household-Water-Use-Litres-Yearly' in df.columns:
        df['Water_Per_Capita_Yearly'] = df['Household-Water-Use-Litres-Yearly'] / people
        df['Water_Per_Capita_Daily'] = df['Water_Per_Capita_Yearly'] / 365
    
    # Per-capita behaviors
    if 'Showers-Per-Week' in df.columns:
        df['Showers_Per_Person_Weekly'] = df['Showers-Per-Week'] / people
    
    if 'Bath-Frequency-Per-Week' in df.columns:
        df['Baths_Per_Person_Weekly'] = df['Bath-Frequency-Per-Week'] / people
    
    print(f"  Created per-capita metrics")
    return df

def calculate_eco_score(df):
    """Calculate composite eco-behavior score (0-5)"""
    print("\n=== Calculating Eco-Behavior Score ===")
    
    eco_score = pd.Series(0, index=df.index, dtype=float)
    max_score = 0
    
    # Shower turn-off (yes = +1)
    if 'Shower-Turn-Off-Temporarily' in df.columns:
        eco_score += (df['Shower-Turn-Off-Temporarily'].str.lower() == 'yes').astype(int)
        max_score += 1
        
    # Toilet small flush (yes = +1)
    if 'Toilet-Use-Small-Flush' in df.columns:
        eco_score += (df['Toilet-Use-Small-Flush'].str.lower() == 'yes').astype(int)
        max_score += 1
        
    # Basin tap NOT running while brushing (no = +1, means eco-conscious)
    if 'Basin-Tap-Running-Brushing-Teeth' in df.columns:
        eco_score += (df['Basin-Tap-Running-Brushing-Teeth'].str.lower() == 'no').astype(int)
        max_score += 1
    
    # Normalize to 0-5 scale
    if max_score > 0:
        df['Eco_Score'] = (eco_score / max_score) * 5
    else:
        df['Eco_Score'] = 0
    
    print(f"  Eco-score components: {max_score}")
    print(f"  Mean Eco-Score: {df['Eco_Score'].mean():.2f}/5")
    return df

def calculate_leak_impact(df):
    """Quantify leak impact on consumption"""
    print("\n=== Calculating Leak Impact ===")
    
    # Estimated annual loss per leak rate (L/year)
    leak_loss_map = {
        'slowly': 5000,      # ~14 L/day
        'moderately': 15000, # ~41 L/day
        'fast': 30000        # ~82 L/day
    }
    
    leak_fixtures = ['Shower', 'Toilet', 'Basin-Tap', 'Bath-Tap', 'Kitchen-Tap']
    total_leak_loss = pd.Series(0, index=df.index, dtype=float)
    leak_count = pd.Series(0, index=df.index, dtype=int)
    
    for fixture in leak_fixtures:
        leak_col = f"{fixture}-Leak"
        rate_col = f"{fixture}-Leak-Rate"
        
        if leak_col in df.columns and rate_col in df.columns:
            # Count leaks
            has_leak = df[leak_col].str.lower() == 'yes'
            leak_count += has_leak.astype(int)
            
            # Estimate loss
            for rate, loss in leak_loss_map.items():
                mask = has_leak & (df[rate_col].str.lower() == rate)
                total_leak_loss += mask.astype(int) * loss
    
    df['Total_Leak_Count'] = leak_count
    df['Estimated_Leak_Loss_Yearly'] = total_leak_loss
    
    # Consumption without leaks
    if 'Household-Water-Use-Litres-Yearly' in df.columns:
        df['Consumption_Without_Leaks'] = df['Household-Water-Use-Litres-Yearly'] - total_leak_loss
        df['Leak_Percentage'] = (total_leak_loss / df['Household-Water-Use-Litres-Yearly']) * 100
    
    print(f"  Mean leak count: {df['Total_Leak_Count'].mean():.2f}")
    print(f"  Mean estimated leak loss: {df['Estimated_Leak_Loss_Yearly'].mean():.0f} L/year")
    return df

def calculate_infrastructure_score(df):
    """Calculate infrastructure efficiency score"""
    print("\n=== Calculating Infrastructure Efficiency Score ===")
    
    infra_score = pd.Series(0, index=df.index, dtype=float)
    max_score = 0
    
    # Water meter (yes = +1)
    if 'Have-Water-Meter' in df.columns:
        infra_score += (df['Have-Water-Meter'].str.lower() == 'yes').astype(int)
        max_score += 1
    
    # Dual-flush toilet (yes = +1)
    if 'Toilet-Type' in df.columns:
        infra_score += df['Toilet-Type'].str.contains('dual', case=False, na=False).astype(int)
        max_score += 1
    
    # Normalize to 0-5 scale
    if max_score > 0:
        df['Infrastructure_Score'] = (infra_score / max_score) * 5
    else:
        df['Infrastructure_Score'] = 0
    
    print(f"  Mean Infrastructure Score: {df['Infrastructure_Score'].mean():.2f}/5")
    return df

def generate_cluster_profiles(df):
    """Generate detailed multi-dimensional cluster profiles"""
    print("\n" + "="*60)
    print("MULTI-DIMENSIONAL CLUSTER PROFILES")
    print("="*60)
    
    profiles = {}
    
    for cluster in sorted(df['Cluster'].unique()):
        cluster_df = df[df['Cluster'] == cluster]
        n = len(cluster_df)
        pct = (n / len(df)) * 100
        
        profile = {
            'Size': n,
            'Percentage': pct,
        }
        
        # Dimension 1: Household Context
        profile['Avg_People'] = cluster_df['Number-Of-People'].mean()
        
        # Dimension 2: Consumption
        if 'Household-Water-Use-Litres-Yearly' in df.columns:
            profile['Consumption_Yearly'] = cluster_df['Household-Water-Use-Litres-Yearly'].mean()
        if 'Water_Per_Capita_Daily' in df.columns:
            profile['Per_Capita_Daily'] = cluster_df['Water_Per_Capita_Daily'].mean()
        
        # Dimension 3: Eco-Behavior
        if 'Eco_Score' in df.columns:
            profile['Eco_Score'] = cluster_df['Eco_Score'].mean()
        
        # Dimension 4: Leak Status
        if 'Total_Leak_Count' in df.columns:
            profile['Avg_Leaks'] = cluster_df['Total_Leak_Count'].mean()
            profile['Leak_Rate_Pct'] = (cluster_df['Total_Leak_Count'] > 0).mean() * 100
        if 'Estimated_Leak_Loss_Yearly' in df.columns:
            profile['Leak_Loss_Yearly'] = cluster_df['Estimated_Leak_Loss_Yearly'].mean()
        
        # Dimension 5: Infrastructure
        if 'Infrastructure_Score' in df.columns:
            profile['Infrastructure_Score'] = cluster_df['Infrastructure_Score'].mean()
        
        # Dimension 6: Behavioral Frequencies
        if 'Showers-Per-Week' in df.columns:
            profile['Showers_Weekly'] = cluster_df['Showers-Per-Week'].mean()
        if 'Bath-Frequency-Per-Week' in df.columns:
            profile['Baths_Weekly'] = cluster_df['Bath-Frequency-Per-Week'].mean()
        
        profiles[cluster] = profile
        
        # Print profile
        print(f"\n--- CLUSTER {cluster}: {get_cluster_name(cluster)} ---")
        print(f"  Size: {n:,} households ({pct:.1f}%)")
        print(f"  Avg People: {profile['Avg_People']:.1f}")
        if 'Consumption_Yearly' in profile:
            print(f"  Consumption: {profile['Consumption_Yearly']:,.0f} L/year")
        if 'Per_Capita_Daily' in profile:
            print(f"  Per-Capita: {profile['Per_Capita_Daily']:.0f} L/day")
        if 'Eco_Score' in profile:
            print(f"  Eco-Score: {profile['Eco_Score']:.2f}/5")
        if 'Leak_Rate_Pct' in profile:
            print(f"  Leak Rate: {profile['Leak_Rate_Pct']:.1f}% of households")
        if 'Leak_Loss_Yearly' in profile:
            print(f"  Leak Loss: {profile['Leak_Loss_Yearly']:,.0f} L/year")
        if 'Infrastructure_Score' in profile:
            print(f"  Infrastructure: {profile['Infrastructure_Score']:.2f}/5")
        if 'Showers_Weekly' in profile:
            print(f"  Showers/week: {profile['Showers_Weekly']:.1f}")
        if 'Baths_Weekly' in profile:
            print(f"  Baths/week: {profile['Baths_Weekly']:.1f}")
    
    return profiles

def get_cluster_name(cluster_id):
    """Return cluster name based on ID"""
    names = {
        0: "Low-Intensity Conservers",
        1: "Moderate Standard Users", 
        2: "High-Intensity Profligate"
    }
    return names.get(cluster_id, f"Cluster {cluster_id}")

def calculate_transition_potential(df, profiles):
    """Calculate potential savings for cluster transitions"""
    print("\n" + "="*60)
    print("CLUSTER TRANSITION ANALYSIS")
    print("="*60)
    
    # Calculate potential savings from C2 → C1 → C0
    if 2 in profiles and 1 in profiles and 0 in profiles:
        # C2 → C1 transition
        c2_to_c1_savings = profiles[2].get('Consumption_Yearly', 0) - profiles[1].get('Consumption_Yearly', 0)
        
        # C1 → C0 transition
        c1_to_c0_savings = profiles[1].get('Consumption_Yearly', 0) - profiles[0].get('Consumption_Yearly', 0)
        
        # C2 → C0 direct
        c2_to_c0_savings = profiles[2].get('Consumption_Yearly', 0) - profiles[0].get('Consumption_Yearly', 0)
        
        print(f"\n--- Potential Annual Water Savings ---")
        print(f"  Cluster 2 → Cluster 1: {c2_to_c1_savings:,.0f} L/year per household")
        print(f"  Cluster 1 → Cluster 0: {c1_to_c0_savings:,.0f} L/year per household")
        print(f"  Cluster 2 → Cluster 0: {c2_to_c0_savings:,.0f} L/year per household")
        
        # Key behavior differences
        print(f"\n--- Key Behavioral Changes Required (C2 → C0) ---")
        
        if 'Eco_Score' in profiles[2] and 'Eco_Score' in profiles[0]:
            eco_diff = profiles[0]['Eco_Score'] - profiles[2]['Eco_Score']
            print(f"  Eco-Score: {profiles[2]['Eco_Score']:.2f} → {profiles[0]['Eco_Score']:.2f} (+{eco_diff:.2f})")
        
        if 'Showers_Weekly' in profiles[2] and 'Showers_Weekly' in profiles[0]:
            shower_diff = profiles[2]['Showers_Weekly'] - profiles[0]['Showers_Weekly']
            print(f"  Showers/week: {profiles[2]['Showers_Weekly']:.1f} → {profiles[0]['Showers_Weekly']:.1f} (-{shower_diff:.1f})")
        
        if 'Leak_Rate_Pct' in profiles[2] and 'Leak_Rate_Pct' in profiles[0]:
            leak_diff = profiles[2]['Leak_Rate_Pct'] - profiles[0]['Leak_Rate_Pct']
            print(f"  Leak Rate: {profiles[2]['Leak_Rate_Pct']:.1f}% → {profiles[0]['Leak_Rate_Pct']:.1f}% (-{leak_diff:.1f}%)")
        
        return {
            'C2_to_C1': c2_to_c1_savings,
            'C1_to_C0': c1_to_c0_savings,
            'C2_to_C0': c2_to_c0_savings
        }
    
    return {}

def plot_multi_dimensional_profiles(df, profiles):
    """Create visualization of multi-dimensional profiles"""
    print("\n=== Generating Multi-Dimensional Profile Visualization ===")
    
    # Prepare data for radar chart
    dimensions = ['Eco_Score', 'Per_Capita_Daily', 'Leak_Rate_Pct', 'Infrastructure_Score']
    available_dims = [d for d in dimensions if all(d in profiles[c] for c in profiles)]
    
    if len(available_dims) < 3:
        print("  Not enough dimensions for radar chart, creating bar chart instead")
        # Create comparison bar chart
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        clusters = sorted(profiles.keys())
        cluster_names = [get_cluster_name(c) for c in clusters]
        
        # Per-capita consumption
        if all('Per_Capita_Daily' in profiles[c] for c in clusters):
            values = [profiles[c]['Per_Capita_Daily'] for c in clusters]
            axes[0,0].bar(cluster_names, values, color=['green', 'orange', 'red'])
            axes[0,0].set_title('Per-Capita Daily Consumption (L/day)')
            axes[0,0].set_ylabel('Liters')
        
        # Eco-Score
        if all('Eco_Score' in profiles[c] for c in clusters):
            values = [profiles[c]['Eco_Score'] for c in clusters]
            axes[0,1].bar(cluster_names, values, color=['green', 'orange', 'red'])
            axes[0,1].set_title('Eco-Behavior Score (0-5)')
            axes[0,1].set_ylabel('Score')
        
        # Leak Rate
        if all('Leak_Rate_Pct' in profiles[c] for c in clusters):
            values = [profiles[c]['Leak_Rate_Pct'] for c in clusters]
            axes[1,0].bar(cluster_names, values, color=['green', 'orange', 'red'])
            axes[1,0].set_title('Leak Rate (%)')
            axes[1,0].set_ylabel('Percentage')
        
        # Infrastructure Score
        if all('Infrastructure_Score' in profiles[c] for c in clusters):
            values = [profiles[c]['Infrastructure_Score'] for c in clusters]
            axes[1,1].bar(cluster_names, values, color=['green', 'orange', 'red'])
            axes[1,1].set_title('Infrastructure Efficiency Score (0-5)')
            axes[1,1].set_ylabel('Score')
        
        plt.suptitle('Multi-Dimensional Cluster Comparison', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, 'multi_dimensional_profiles.png'), dpi=150)
        print(f"  Saved: multi_dimensional_profiles.png")
    
    plt.close()

def save_enhanced_data(df):
    """Save enhanced dataset with new metrics"""
    output_path = os.path.join(OUTPUT_DIR, 'clustered_data_behavioral_deep.csv')
    df.to_csv(output_path, index=False)
    print(f"\n✓ Enhanced data saved to: {output_path}")
    return output_path

def save_profile_summary(profiles, transitions):
    """Save profile summary to CSV"""
    # Convert profiles to DataFrame
    profile_df = pd.DataFrame(profiles).T
    profile_df.index.name = 'Cluster'
    
    output_path = os.path.join(OUTPUT_DIR, 'cluster_behavioral_profiles.csv')
    profile_df.to_csv(output_path)
    print(f"✓ Profile summary saved to: {output_path}")
    
    return output_path

def main():
    print("="*60)
    print("DEEP BEHAVIORAL ANALYSIS - MULTI-DIMENSIONAL PROFILING")
    print("="*60)
    
    # Load data
    df = load_data()
    
    # Calculate behavioral adjustments
    df = calculate_per_capita_metrics(df)
    df = calculate_eco_score(df)
    df = calculate_leak_impact(df)
    df = calculate_infrastructure_score(df)
    
    # Generate cluster profiles
    profiles = generate_cluster_profiles(df)
    
    # Calculate transition potential
    transitions = calculate_transition_potential(df, profiles)
    
    # Generate visualizations
    plot_multi_dimensional_profiles(df, profiles)
    
    # Save outputs
    save_enhanced_data(df)
    save_profile_summary(profiles, transitions)
    
    print("\n" + "="*60)
    print("DEEP BEHAVIORAL ANALYSIS COMPLETE")
    print("="*60)
    
    return df, profiles, transitions

if __name__ == "__main__":
    df, profiles, transitions = main()
