# Cox PH model: PFS ~ gene_score (ref = low) + age + sex
n = 500, 332 progression events; R survival::coxph, Efron ties, Wald 95% CI and p-values.

| Contrast | HR | 95% CI | p |
|---|---|---|---|
| medium vs low | 1.367 | 1.059 - 1.763 | 0.0162 |
| high vs low | 2.532 | 1.912 - 3.352 | 8.7e-11 |
| age (per year) | 1.030 | 1.021 - 1.038 | 2.7e-12 |
| sex (1 vs 0) | 0.797 | 0.642 - 0.990 | 0.040 |

After adjusting for age and sex, higher gene signature scores go with worse PFS, and the risk rises with each level. The medium-score group has about 37% higher hazard than the low-score group, and the high-score group has about 2.5 times the hazard. The overall gene_score likelihood-ratio test is p = 6.5e-9. The proportional hazards assumption holds (cox.zph global p = 0.99).
