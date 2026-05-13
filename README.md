# DS555 — Mini MVA Project

Multivariate analysis of the HATCO dataset exploring how firm characteristics influence customer satisfaction and corporate image perceptions.

## Dataset

**HATCO_clean.csv** (100 observations, 14 variables)

| Variable | Description | Type |
|---|---|---|
| `delivery_speed` | Delivery speed rating | Continuous |
| `price_level` | Price level | Continuous |
| `price_flexibility` | Price flexibility rating | Continuous |
| `manufacturer_image` | Manufacturer image rating | Continuous |
| `service_level` | Service level rating | Continuous |
| `salesforce_image` | Salesforce image rating | Continuous |
| `product_quality` | Product quality rating | Continuous |
| `firm_size` | Firm size (0=Small, 1=Medium, 2=Large) | Categorical |
| `usage_level` | Product usage level | Continuous |
| `satisfaction` | Overall satisfaction (0–10) | Continuous |
| `spec_buying` | Speculative buying | Binary |
| `procurement_structure` | Procurement structure type | Categorical |
| `industry_type` | Industry type | Categorical |
| `buying_situation` | Buying situation type | Categorical |

## Research Questions

### RQ1 — Firm Size vs. Satisfaction Level (One-Way ANOVA)

**Question:** Does average satisfaction differ significantly by firm size?

| | Variable | Role |
|---|---|---|
| IV | `firm_size` (3 groups) | Independent |
| DV | `satisfaction` (continuous) | Dependent |

**Hypotheses:**
- H₀: μ_Small = μ_Medium = μ_Large (no difference)
- H₁: At least one group mean differs

**Method:**
1. Shapiro-Wilk normality test per group
2. Levene's test for homogeneity of variance
3. One-Way ANOVA
4. Tukey HSD post-hoc (if ANOVA is significant)

**Result:** **Reject H₀** — firm size significantly affects satisfaction (p < 0.05).

Post-hoc (Tukey HSD):
- Small ≠ Medium (p ≈ 0.012)
- Medium ≠ Large (p ≈ 0.04)
- Small = Large (p ≈ 0.8, not significant)

---

### RQ2 — Firm Size vs. Corporate Image Perceptions (One-Way MANOVA)

**Question:** Does firm size affect the combined perceptions of delivery speed, service level, and salesforce image?

| | Variables | Role |
|---|---|---|
| IV | `firm_size` (3 groups) | Independent |
| DVs | `delivery_speed`, `service_level`, `salesforce_image` | Dependent (multivariate) |

**Hypotheses:**
- H₀: Mean vectors are equal across all firm size groups
- H₁: At least one group mean vector differs

**Method:**
1. Shapiro-Wilk normality test for each DV per group
2. Box's M test for homogeneity of covariance matrices
3. Levene's test per DV for homoscedasticity
4. MANOVA (Wilks' Lambda & Pillai's Trace)

**Result:** **Accept H₀** — no significant multivariate effect of firm size on corporate image perceptions (p > 0.05 for both Wilks' Lambda and Pillai's Trace). No post-hoc required.

## Project Structure

```
project555/
├── code/
│   └── analysis.ipynb       # Main analysis notebook
├── data/
│   ├── HATCO_clean.csv      # Cleaned dataset
│   └── HATCO_Documentation.pdf
└── DS555-Mini-final.pdf     # Final report
```

## Dependencies

- Python 3.12
- pandas, numpy
- pingouin
- plotly, matplotlib
- scikit-learn
- ydata-profiling
- statsmodels
- IPython

## Key Findings

1. Satisfaction levels differ significantly across firm sizes — the effect is between adjacent size groups (Small/Medium and Medium/Large), but small and large firms do not differ significantly.
2. Corporate image perceptions (delivery speed, service, salesforce image) do **not** vary by firm size, suggesting consistent brand perception regardless of customer scale.