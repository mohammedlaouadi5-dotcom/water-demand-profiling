# =============================================================================
# Git Commands for Repository Setup
# =============================================================================
# Run these commands in your terminal/PowerShell
# =============================================================================

# 1. Navigate to the project directory
cd "c:\Users\moham\Desktop\New folder\profiling\data_science_profiling"

# 2. Initialize Git repository
git init

# 3. Add all files (respecting .gitignore)
git add .

# 4. First commit
git commit -m "Initial commit: Water Demand Behavioral Profiling Framework

- MAD-Bootstrap feature selection
- NMF dimensionality reduction
- GMM probabilistic clustering
- SHAP explainability
- Monte Carlo validation

Paper: Survey-informed water demand behavioral profiling (WSE, 2024)"

# 5. Create main branch
git branch -M main

# 6. Add remote origin (replace with your actual GitHub repo URL)
git remote add origin https://github.com/yourusername/water-demand-profiling.git

# 7. Push to GitHub
git push -u origin main

# =============================================================================
# Additional Git Commands (Optional)
# =============================================================================

# Create a release tag
git tag -a v1.0.0 -m "Version 1.0.0 - Initial release for WSE paper"
git push origin v1.0.0

# View status
git status

# View log
git log --oneline -10
