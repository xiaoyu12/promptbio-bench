# Factor analysis of survey_data.csv
Parallel analysis (100 iterations, 95th percentile, random_state=42) supports **3 factors**. The observed eigenvalues of the first three factors (6.40, 3.35, 2.57) exceed the random 95th percentiles (1.56, 1.45, 1.37). The 4th does not (1.02 vs 1.31).

The model was fit with MINRES extraction and varimax rotation. The three factors explain 55.9% of the variance.
- Factor_1: Item_01-Item_06 (loadings 0.73-0.84)
- Factor_2: Item_07-Item_12 (loadings 0.70-0.79)
- Factor_3: Item_13-Item_18 (loadings 0.66-0.82)
- Item_19 and Item_20 have near-zero loadings (communality <0.02) and belong to no factor.

The full loadings are in factor_loadings.csv.
