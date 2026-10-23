# Median imputation of numeric columns (b-2-2)

Dataset: 500 patients x 28 columns, of which 19 are numeric. Each missing numeric value was replaced with the median of the observed values in its column.

- **Total missing values filled: 440**. That is 4.63% of the 9,500 numeric cells (500 x 19) and 3.14% of all 14,000 cells.
- 9 of the 19 numeric columns had missing values. All of them are clinical or gene-expression columns, each with 8.4–11.2% missing:

| column | missing_count | missing_% | median_used |
|---|---|---|---|
| Cholesterol | 56 | 11.2 | 204.90 |
| BRCA1_expression | 55 | 11.0 | 153.07 |
| TP53_expression | 55 | 11.0 | 392.65 |
| Glucose | 53 | 10.6 | 99.45 |
| HeartRate | 46 | 9.2 | 70.555 |
| EGFR_expression | 46 | 9.2 | 93.135 |
| BMI | 44 | 8.8 | 25.325 |
| BloodPressure_Systolic | 43 | 8.6 | 120.59 |
| BloodPressure_Diastolic | 42 | 8.4 | 80.83 |

- 293 of the 500 patients had at least one imputed value.
- None of the other 10 numeric columns had missing values: Age, MYC_expression, KRAS_expression, Var1–Var4, Temperature, IsSmoker and LabResult.
- After imputation, no numeric values are missing. The non-numeric columns are unchanged.

Outputs: `imputation_report.csv` (per-column counts, percentages and medians) and `imputed_data.csv` (the imputed dataset).
