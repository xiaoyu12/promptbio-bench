# TMB across four cancer types (n = 30 each)

Median TMB (mut/Mb): Breast 3.94, Colorectal 7.08, Lung 9.75, Melanoma 13.83.

**Kruskal-Wallis:** H = 68.00, df = 3, p = 1.15e-14. TMB differs significantly across cancer types (epsilon^2 = 0.57, a large effect).

**Dunn's post-hoc test** (two-sided, tie-corrected, Bonferroni-adjusted, alpha = 0.05):

| Comparison | z | adj. p | Significant |
|---|---|---|---|
| Breast vs Colorectal | -3.20 | 0.0082 | Yes |
| Breast vs Lung | -5.16 | 1.5e-06 | Yes |
| Breast vs Melanoma | -8.01 | 7.0e-15 | Yes |
| Colorectal vs Lung | -1.95 | 0.304 | No |
| Colorectal vs Melanoma | -4.80 | 9.3e-06 | Yes |
| Lung vs Melanoma | -2.85 | 0.026 | Yes |

Five of the six pairs differ significantly. Only Colorectal vs Lung does not (raw p = 0.051, which is also not significant under Holm or BH). The ordering is Melanoma > Lung ≈ Colorectal > Breast.
