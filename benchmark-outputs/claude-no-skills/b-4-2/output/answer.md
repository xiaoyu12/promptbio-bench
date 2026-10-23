# TP53 expression across tumor grades

One-way ANOVA: F(3, 96) = 37.50, p = 3.96e-16, eta^2 = 0.54. TP53 expression differs significantly across tumor grades. Mean expression rises with grade: I 4.82, II 6.49, III 7.89, IV 9.27.
The model assumptions hold (Shapiro-Wilk on residuals p = 0.92; Levene p = 0.45). The result is the same under Welch ANOVA (p = 2.7e-13) and Kruskal-Wallis (p = 1.2e-11).

Tukey HSD (adjusted p-values): every pairwise comparison is significant.

| Comparison | Mean diff | 95% CI | p-adj |
|---|---|---|---|
| Grade I vs II | 1.66 | 0.47 to 2.86 | 0.0024 |
| Grade I vs III | 3.06 | 1.85 to 4.28 | <0.0001 |
| Grade I vs IV | 4.45 | 3.29 to 5.61 | <0.0001 |
| Grade II vs III | 1.40 | 0.26 to 2.53 | 0.0093 |
| Grade II vs IV | 2.79 | 1.71 to 3.86 | <0.0001 |
| Grade III vs IV | 1.39 | 0.29 to 2.49 | 0.0072 |

Figure: tp53_boxplot_with_pvalues.png (boxplot with jittered points; brackets show the Tukey p-values). Full table: tukey_hsd_results.csv.
