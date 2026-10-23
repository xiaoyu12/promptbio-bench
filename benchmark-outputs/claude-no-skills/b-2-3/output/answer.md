# KNN imputation (k=5, Euclidean) – b-2-3
Method: scikit-learn KNNImputer (k=5, nan-Euclidean distance, uniform weights) on the 19 numeric clinical/genomic/demographic features, z-score standardised before distance computation and back-transformed to original units. Categorical/ID columns had no missing values and were kept as-is.

**Total imputed values: 440 of 14,000 data cells (500 patients x 28 columns) = 3.14%** (4.63% of the 9,500 numeric cells). 293 of 500 patients had at least one imputed value.

| Column | Missing/imputed | % |
|---|---|---|
| BMI | 44 | 8.8 |
| BloodPressure_Systolic | 43 | 8.6 |
| BloodPressure_Diastolic | 42 | 8.4 |
| Cholesterol | 56 | 11.2 |
| Glucose | 53 | 10.6 |
| HeartRate | 46 | 9.2 |
| BRCA1_expression | 55 | 11.0 |
| TP53_expression | 55 | 11.0 |
| EGFR_expression | 46 | 9.2 |
All other columns: 0 missing.
