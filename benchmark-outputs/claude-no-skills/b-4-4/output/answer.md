# Notes (b-4-4)
- Difference defined as BP_After - BP_Before (same sign as provided Change column); negative = decrease after treatment.
- Computed from raw BP_Before/BP_After columns; the shipped Change column differs by up to 0.1 due to rounding (mean Change = -9.483 vs -9.467 from raw values).
- Two-sided paired t-test, alpha = 0.05, scipy.stats.ttest_rel; 95% CI from t distribution with df = n-1 = 29.
- Assumption check: Shapiro-Wilk on differences p = 0.68 (normality fine). Sensitivity: Wilcoxon signed-rank p = 3.7e-9.
- Result: mean diff = -9.47 mmHg, 95% CI [-11.22, -7.72], t(29) = -11.07, p = 6.33e-12; Cohen's dz = -2.02. Significant decrease.
