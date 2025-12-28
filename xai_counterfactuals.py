"""
Option C: Counterfactual Analysis (What-If Scenarios)
- Train Classifier (Random Forest)
- Simulate transitions from Profligate (C1) to Conservers (C2)
- Identify minimal behavioral changes required
- Cost-Benefit Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

# Paths
DATA_PATH = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling\clustered_data_enhanced.csv'
OUTPUT_DIR = r'c:\Users\moham\Desktop\New folder\profiling\data_science_profiling'

def load_data():
    """Load and prepare data"""
    print("="*60)
    print("OPTION C: COUNTERFACTUAL ANALYSIS (WHAT-IF)")
    print("="*60)
    
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df)} households")
    
    exclude_cols = ['Cluster', 'Max_Prob', 'Month', 'Year', 'Date', 'Postal outcode', 
                    'Functional area', 'County', 'Latitude', 'Longitude']
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    feature_cols = [c for c in numeric_cols if c not in exclude_cols]
    
    X = df[feature_cols].fillna(0)
    y = df['Cluster']
    
    return df, X, y, feature_cols

def train_model(X, y):
    """Train Random Forest for prediction"""
    print("\n--- Training Transition Model ---")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    rf.fit(X_train, y_train)
    
    acc = rf.score(X_test, y_test)
    print(f"Model Accuracy: {acc:.2%}")
    
    return rf

def simulate_transitions(model, df, X, feature_names):
    """Simulate transitions from C1 (Profligate) to C2 (Conservers)"""
    print("\n--- Simulating Transitions (C1 -> C2) ---")
    
    # Target: Move C1 (Cluster 1) -> C2 (Cluster 2)
    c1_households = X[df['Cluster'] == 1]
    c2_households = X[df['Cluster'] == 2]
    
    # Calculate target profile (C2 medians)
    target_profile = c2_households.median()
    
    # Key actionable features to perturb
    actionable_features = [
        'Showers-Per-Week', 
        'Bath-Frequency-Per-Week',
        'Shower-Duration-Minutes',
        'Boil-Water-Per-Week',
        'Wash-Dishes-By-Hand'
    ]
    
    # Leak features (binary/categorical handled as numeric here for simplicity if encoded)
    # Assuming leaks are encoded or we check specific columns
    leak_features = [c for c in feature_names if 'Leak' in c and 'Rate' not in c]
    
    print(f"Actionable features: {len(actionable_features)}")
    print(f"Leak features: {len(leak_features)}")
    
    # Select a sample of C1 households
    sample_size = 50
    c1_sample = c1_households.sample(n=sample_size, random_state=42)
    
    successful_transitions = 0
    changes_required = []
    
    for idx, household in c1_sample.iterrows():
        current_state = household.copy()
        original_pred = model.predict([current_state])[0]
        
        if original_pred != 1:
            continue # Skip if model doesn't predict C1 initially
            
        # Strategy 1: Fix Leaks first
        leaks_fixed = 0
        for leak_feat in leak_features:
            # Assuming 1 = Yes, 0 = No (if OHE or binary)
            # Check if feature exists and is high
            if leak_feat in current_state and current_state[leak_feat] > 0.5:
                current_state[leak_feat] = 0 # Fix leak
                leaks_fixed += 1
        
        pred_after_leaks = model.predict([current_state])[0]
        
        # Strategy 2: Reduce Consumption Behaviors iteratively
        behavior_reduction = 0
        steps = 20 # 5% reduction per step
        
        transitioned = False
        final_reduction_pct = 0
        
        if pred_after_leaks == 2:
            transitioned = True
        else:
            for step in range(1, steps + 1):
                reduction_factor = 1.0 - (step * 0.05) # Reduce by 5%, 10%, ...
                
                for feat in actionable_features:
                    if feat in current_state:
                        # Move towards target (C2 median) but don't go below it if already lower
                        target_val = target_profile[feat]
                        current_val = household[feat]
                        
                        if current_val > target_val:
                            new_val = current_val * reduction_factor
                            current_state[feat] = max(new_val, target_val)
                
                new_pred = model.predict([current_state])[0]
                if new_pred == 2:
                    transitioned = True
                    final_reduction_pct = step * 5
                    break
        
        if transitioned:
            successful_transitions += 1
            changes_required.append({
                'Household_ID': idx,
                'Leaks_Fixed': leaks_fixed,
                'Behavior_Reduction_Pct': final_reduction_pct
            })
    
    return changes_required, sample_size

def analyze_results(changes, sample_size):
    """Analyze and save counterfactual results"""
    print("\n--- Analyzing Counterfactual Results ---")
    
    if not changes:
        print("No successful transitions found.")
        return
    
    df_results = pd.DataFrame(changes)
    
    success_rate = (len(df_results) / sample_size) * 100
    avg_reduction = df_results['Behavior_Reduction_Pct'].mean()
    avg_leaks = df_results['Leaks_Fixed'].mean()
    
    # Cost-Benefit Estimation
    # Assumptions:
    # - Leak fix cost: £100
    # - Behavior change cost (campaign): £20
    # - Water savings: 50,000 L/year (~£150/year)
    
    avg_cost = (avg_leaks * 100) + (20 if avg_reduction > 0 else 0)
    avg_savings = 150 # Estimated
    roi_years = avg_cost / avg_savings if avg_savings > 0 else 0
    
    print(f"Success Rate: {success_rate:.1f}%")
    print(f"Average Behavior Reduction Needed: {avg_reduction:.1f}%")
    print(f"Average Leaks Fixed: {avg_leaks:.1f}")
    print(f"Estimated ROI Period: {roi_years:.1f} years")
    
    # Save report
    report_path = os.path.join(OUTPUT_DIR, 'counterfactual_analysis.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Counterfactual Analysis: Transitioning Profligates (C1) to Conservers (C2)\n\n")
        f.write("## Methodology\n")
        f.write("- **Model**: Random Forest Classifier\n")
        f.write("- **Strategy**: Fix leaks first, then iteratively reduce behavioral frequencies (Showers, Baths, etc.)\n")
        f.write("- **Target**: Cluster 2 (Conservers)\n\n")
        
        f.write("## Key Findings\n")
        f.write(f"- **Transition Success Rate**: {success_rate:.1f}%\n")
        f.write(f"- **Average Behavior Reduction Required**: {avg_reduction:.1f}%\n")
        f.write(f"- **Average Leaks Fixed per Household**: {avg_leaks:.1f}\n\n")
        
        f.write("## Cost-Benefit Analysis (Estimates)\n")
        f.write(f"- **Intervention Cost**: £{avg_cost:.2f} (Leak repairs + Behavioral nudges)\n")
        f.write(f"- **Annual Savings**: £{avg_savings:.2f} (Water bill reduction)\n")
        f.write(f"- **Payback Period**: {roi_years:.1f} years\n\n")
        
        f.write("## Recommendation\n")
        if avg_leaks > 0.5:
            f.write("- **Priority**: Leak repair programs are essential for this transition.\n")
        else:
            f.write("- **Priority**: Behavioral change (reducing frequency) is the main driver.\n")
            
    print(f"  Saved: counterfactual_analysis.md")

def main():
    df, X, y, feature_names = load_data()
    model = train_model(X, y)
    changes, sample_size = simulate_transitions(model, df, X, feature_names)
    analyze_results(changes, sample_size)
    
    print("\n" + "="*60)
    print("OPTION C: COUNTERFACTUAL ANALYSIS - COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
