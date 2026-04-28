# -*- coding: utf-8 -*-
# =============================================================================
#  DS555 — HATCO Project Practice Script
#  اكتب الكود ده بنفسك خطوة خطوة كمشروع تدريبي
# =============================================================================
# DATA: data/HATCO_clean.csv  (100 rows, 14 variables)
#
# VARIABLES:
#   Metric (0-10):  delivery_speed, price_level, price_flexibility,
#                   manufacturer_image, service_level, salesforce_image,
#                   product_quality, usage_level(0-100), satisfaction
#   Non-Metric:     firm_size(0/1), spec_buying(0/1),
#                   procurement_structure(0/1), industry_type(0/1),
#                   buying_situation(1/2/3)
# =============================================================================


# ─────────────────────────────────────────────
#  STEP 0 — Import libraries & load data
# ─────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.dpi'] = 100

import warnings
warnings.filterwarnings('ignore')

# Load the clean CSV
df = pd.read_csv('data/HATCO_clean.csv')

print("Shape:", df.shape)        # should be (100, 15)
print(df.head())                 # first 5 rows
print(df.dtypes)                 # column types


# ─────────────────────────────────────────────
#  SECTION 1 — VARIABLES CLASSIFICATION
# ─────────────────────────────────────────────

# Separate metric vs non-metric columns
metric_cols    = ['delivery_speed', 'price_level', 'price_flexibility',
                  'manufacturer_image', 'service_level', 'salesforce_image',
                  'product_quality', 'usage_level', 'satisfaction']

nonmetric_cols = ['firm_size', 'spec_buying', 'procurement_structure',
                  'industry_type', 'buying_situation']

print("\n--- Metric variables ---")
print(df[metric_cols].head())

print("\n--- Non-Metric variables ---")
print(df[nonmetric_cols].head())


# ─────────────────────────────────────────────
#  SECTION 2A — FREQUENCY TABLES (Non-Metric)
# ─────────────────────────────────────────────

print("\n========== FREQUENCY TABLES ==========")

for col in nonmetric_cols:
    freq  = df[col].value_counts().sort_index()
    rel   = df[col].value_counts(normalize=True).sort_index().round(3) * 100
    table = pd.DataFrame({'Count': freq, 'Percent %': rel})
    print(f"\n[{col}]")
    print(table)


# ─────────────────────────────────────────────
#  SECTION 2B — BAR CHARTS (Non-Metric)
# ─────────────────────────────────────────────

# Labels for readability
labels = {
    'firm_size':               {0: 'Small', 1: 'Large'},
    'spec_buying':             {0: 'Spec Buying', 1: 'Total Value'},
    'procurement_structure':   {0: 'Decentralized', 1: 'Centralized'},
    'industry_type':           {0: 'Other', 1: 'Industry A'},
    'buying_situation':        {1: 'New Task', 2: 'Modified Rebuy', 3: 'Straight Rebuy'},
}

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()

for i, col in enumerate(nonmetric_cols):
    counts = df[col].value_counts().sort_index()
    x_labels = [labels[col].get(k, str(k)) for k in counts.index]
    axes[i].bar(x_labels, counts.values, color='steelblue', edgecolor='white')
    axes[i].set_title(f'Figure {i+1}: {col.replace("_"," ").title()}')
    axes[i].set_xlabel('Category')
    axes[i].set_ylabel('Count')
    for j, v in enumerate(counts.values):
        axes[i].text(j, v + 0.5, str(v), ha='center', fontsize=9)

axes[-1].set_visible(False)   # hide empty subplot
plt.tight_layout()
plt.savefig('plots/Figure_01_to_05_barcharts.png')
plt.show()
print("Saved: plots/Figure_01_to_05_barcharts.png")


# ─────────────────────────────────────────────
#  SECTION 2C — DESCRIPTIVE STATISTICS (Metric)
# ─────────────────────────────────────────────

print("\n========== DESCRIPTIVE STATISTICS ==========")

desc = df[metric_cols].describe(percentiles=[0.25, 0.5, 0.75]).T
desc['range'] = desc['max'] - desc['min']
desc['IQR']   = desc['75%'] - desc['25%']

print(desc[['mean','50%','std','variance' if 'variance' in desc else 'std',
            'min','max','range','25%','75%','IQR']].round(2))

# Full describe
print("\nFull describe:")
print(df[metric_cols].describe(percentiles=[0.10, 0.25, 0.50, 0.75, 0.90]).round(2))


# ─────────────────────────────────────────────
#  SECTION 2D — HISTOGRAMS (Metric)
# ─────────────────────────────────────────────

fig, axes = plt.subplots(3, 3, figsize=(14, 10))
axes = axes.flatten()

for i, col in enumerate(metric_cols):
    axes[i].hist(df[col], bins=10, color='steelblue', edgecolor='white')
    axes[i].axvline(df[col].mean(),   color='red',    linestyle='--', label=f'Mean={df[col].mean():.1f}')
    axes[i].axvline(df[col].median(), color='orange', linestyle='--', label=f'Median={df[col].median():.1f}')
    axes[i].set_title(f'Figure {i+6}: {col.replace("_"," ").title()}')
    axes[i].set_xlabel('Value')
    axes[i].set_ylabel('Frequency')
    axes[i].legend(fontsize=7)

plt.tight_layout()
plt.savefig('plots/Figure_06_to_14_histograms.png')
plt.show()
print("Saved: plots/Figure_06_to_14_histograms.png")


# ─────────────────────────────────────────────
#  SECTION 3A — ONE-WAY ANOVA
#  Q: Does satisfaction differ by firm size?
#  IV: firm_size (0=Small, 1=Large)
#  DV: satisfaction (0–10)
# ─────────────────────────────────────────────
from scipy import stats

print("\n========== ONE-WAY ANOVA ==========")
print("Q: Does satisfaction differ between Small and Large firms?")
print("H0: mean_small = mean_large")
print("H1: mean_small != mean_large")

# Split groups
small = df[df['firm_size'] == 0]['satisfaction']
large = df[df['firm_size'] == 1]['satisfaction']

print(f"\nSmall firms  (n={len(small)}): mean={small.mean():.2f}, std={small.std():.2f}")
print(f"Large firms  (n={len(large)}): mean={large.mean():.2f}, std={large.std():.2f}")

# --- Step 1: Normality test (Shapiro-Wilk) ---
print("\n--- Normality Test (Shapiro-Wilk) ---")
stat_s, p_s = stats.shapiro(small)
stat_l, p_l = stats.shapiro(large)
print(f"Small: W={stat_s:.4f}, p={p_s:.4f}  →  {'Normal ✓' if p_s > 0.05 else 'NOT normal ✗'}")
print(f"Large: W={stat_l:.4f}, p={p_l:.4f}  →  {'Normal ✓' if p_l > 0.05 else 'NOT normal ✗'}")

# --- Step 2: Homogeneity of Variance (Levene) ---
print("\n--- Levene's Test (Homogeneity of Variance) ---")
lev_stat, lev_p = stats.levene(small, large)
print(f"Levene: F={lev_stat:.4f}, p={lev_p:.4f}  →  {'Equal variances ✓' if lev_p > 0.05 else 'Unequal variances ✗'}")

# --- Step 3: ANOVA (= Independent T-test for 2 groups) ---
print("\n--- One-Way ANOVA ---")
f_stat, p_val = stats.f_oneway(small, large)
print(f"F = {f_stat:.4f},  p = {p_val:.4f}")
if p_val < 0.05:
    print("Decision: REJECT H0 → Significant difference in satisfaction between firm sizes")
else:
    print("Decision: FAIL TO REJECT H0 → No significant difference")

# Visualization
fig, ax = plt.subplots(figsize=(6, 4))
ax.boxplot([small, large], labels=['Small Firm', 'Large Firm'])
ax.set_title('Figure 15: Satisfaction by Firm Size')
ax.set_ylabel('Satisfaction (0–10)')
plt.tight_layout()
plt.savefig('plots/Figure_15_anova_boxplot.png')
plt.show()
print("Saved: plots/Figure_15_anova_boxplot.png")


# ─────────────────────────────────────────────
#  SECTION 3B — MANOVA
#  Q: Does the OVERALL perception pattern
#     (delivery + service + quality) differ by firm size?
#  IV:  firm_size (0=Small, 1=Large)
#  DVs: delivery_speed, service_level, product_quality
# ─────────────────────────────────────────────
from scipy.stats import chi2

print("\n========== MANOVA ==========")
print("Q: Does the combination of (delivery, service, quality) differ by firm size?")
print("H0: No difference in centroid between Small and Large firms")
print("H1: Centroid differs between groups")

dv_cols = ['delivery_speed', 'service_level', 'product_quality']

# Wilks' Lambda (manual calculation for 2 groups)
group0 = df[df['firm_size'] == 0][dv_cols].values
group1 = df[df['firm_size'] == 1][dv_cols].values

n0, p = group0.shape[0], len(dv_cols)
n1    = group1.shape[0]
n     = n0 + n1

# Grand mean and group means
grand_mean  = df[dv_cols].values.mean(axis=0)
mean0       = group0.mean(axis=0)
mean1       = group1.mean(axis=0)

# Within-group scatter matrix W
W = np.zeros((p, p))
for x in group0:
    d = (x - mean0).reshape(-1, 1)
    W += d @ d.T
for x in group1:
    d = (x - mean1).reshape(-1, 1)
    W += d @ d.T

# Total scatter matrix T
all_data = df[dv_cols].values
T = np.zeros((p, p))
for x in all_data:
    d = (x - grand_mean).reshape(-1, 1)
    T += d @ d.T

# Between-group scatter matrix B = T - W
B = T - W

# Wilks' Lambda = det(W) / det(T)
wilks_lambda = np.linalg.det(W) / np.linalg.det(T)

# Approx F-test for Wilks' Lambda (2 groups)
df_h = p                    # hypothesis df
df_e = n - 2                # error df
F_approx = ((1 - wilks_lambda) / wilks_lambda) * (df_e / df_h)
p_manova  = 1 - stats.f.cdf(F_approx, df_h, df_e)

print(f"\nWilks' Lambda = {wilks_lambda:.4f}")
print(f"Approx F({df_h}, {df_e}) = {F_approx:.4f},  p = {p_manova:.4f}")
if p_manova < 0.05:
    print("Decision: REJECT H0 → Significant multivariate difference in perception pattern")
else:
    print("Decision: FAIL TO REJECT H0 → No significant multivariate difference")

# Univariate follow-up ANOVAs
print("\n--- Univariate Follow-up ANOVAs (for each DV) ---")
for col in dv_cols:
    g0 = df[df['firm_size'] == 0][col]
    g1 = df[df['firm_size'] == 1][col]
    f, p = stats.f_oneway(g0, g1)
    sig = '* significant' if p < 0.05 else '  not significant'
    print(f"  {col:<22}: F={f:.3f}, p={p:.4f}  {sig}")


# ─────────────────────────────────────────────
#  SECTION 3C — FACTOR ANALYSIS
#  Q: Can X1–X7 (perceptions) be reduced to
#     a smaller set of underlying factors?
# ─────────────────────────────────────────────
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

print("\n========== FACTOR ANALYSIS (PCA) ==========")
print("Variables: delivery_speed, price_level, price_flexibility,")
print("           manufacturer_image, service_level, salesforce_image, product_quality")

fa_cols = ['delivery_speed', 'price_level', 'price_flexibility',
           'manufacturer_image', 'service_level', 'salesforce_image', 'product_quality']

X = df[fa_cols].values

# --- Step 1: KMO approximation (using correlation matrix) ---
corr = df[fa_cols].corr()
print("\n--- Correlation Matrix ---")
print(corr.round(2))

# Check overall correlation — if avg off-diagonal > 0.2, FA is appropriate
off_diag = corr.values[np.triu_indices_from(corr.values, k=1)]
print(f"\nAvg inter-variable correlation: {off_diag.mean():.3f}")
print("→ FA is appropriate" if off_diag.mean() > 0.2 else "→ FA may not be appropriate (low correlations)")

# --- Step 2: PCA ---
scaler = StandardScaler()
X_std  = scaler.fit_transform(X)

pca = PCA()
pca.fit(X_std)

eigenvalues  = pca.explained_variance_
explained_pct = pca.explained_variance_ratio_ * 100
cumulative    = np.cumsum(explained_pct)

print("\n--- Eigenvalues & Variance Explained ---")
ev_table = pd.DataFrame({
    'Eigenvalue':     eigenvalues.round(3),
    'Variance %':     explained_pct.round(2),
    'Cumulative %':   cumulative.round(2),
}, index=[f'PC{i+1}' for i in range(len(eigenvalues))])
print(ev_table)

n_factors = np.sum(eigenvalues > 1)
print(f"\n→ Number of factors with Eigenvalue > 1: {n_factors}")

# --- Step 3: Scree Plot ---
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(range(1, len(eigenvalues)+1), eigenvalues, 'o-', color='steelblue')
ax.axhline(y=1, color='red', linestyle='--', label='Eigenvalue = 1')
ax.set_title('Figure 16: Scree Plot')
ax.set_xlabel('Component Number')
ax.set_ylabel('Eigenvalue')
ax.legend()
plt.tight_layout()
plt.savefig('plots/Figure_16_scree_plot.png')
plt.show()
print("Saved: plots/Figure_16_scree_plot.png")

# --- Step 4: Component Loadings (Varimax-like rotation via PCA) ---
pca_n = PCA(n_components=n_factors)
pca_n.fit(X_std)

loadings = pd.DataFrame(
    pca_n.components_.T,
    index=fa_cols,
    columns=[f'Factor_{i+1}' for i in range(n_factors)]
)
print("\n--- Component Loadings (before rotation) ---")
print(loadings.round(3))

# Highlight strong loadings (|loading| > 0.5)
print("\n--- Strong Loadings (|loading| > 0.5) ---")
for factor in loadings.columns:
    strong = loadings[loadings[factor].abs() > 0.5][factor]
    print(f"\n  {factor}:")
    for var, val in strong.items():
        print(f"    {var:<25}: {val:+.3f}")

print("\n========== ANALYSIS COMPLETE ==========")
print("Output files saved in: plots/")
