# TMB across 10 cancer types (ridge plot: tmb_ridge_plot.png)

The ridge plot has one KDE ridge per cancer type (n=200 each), ordered by median TMB:

| Cancer type | Median TMB (mut/Mb) | IQR | % ≥10 mut/Mb |
|---|---|---|---|
| Melanoma | 11.4 | 8.7–14.7 | 65.5 |
| Lung adenocarcinoma | 7.5 | 5.8–9.0 | 17.5 |
| Bladder | 6.6 | 5.3–8.3 | 10.0 |
| Colorectal | 6.0 | 4.4–7.4 | 8.0 |
| Head & Neck | 5.8 | 4.7–7.1 | 2.0 |
| Stomach | 4.5 | 3.4–5.9 | 1.5 |
| Breast | 2.6 | 1.9–3.5 | 0.5 |
| Pancreatic | 2.4 | 1.7–3.3 | 0.5 |
| Ovarian | 1.8 | 1.5–2.5 | 0.0 |
| Prostate | 1.4 | 1.0–1.8 | 0.0 |

- Melanoma has the highest TMB and the widest, most right-skewed distribution. Most melanoma samples are TMB-high (≥10 mut/Mb).
- Lung adenocarcinoma and bladder come next. Prostate, ovarian, pancreatic and breast form a narrow low-TMB group.
- All distributions are right-skewed with long upper tails.
- TMB differs strongly across cancer types (Kruskal-Wallis H=1457, p<1e-300).
