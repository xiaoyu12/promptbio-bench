# Cox LASSO feature selection (b-9-4)
LASSO-penalized Cox (glmnet, 5-fold CV on partial-likelihood deviance, seed 42) chose lambda.min = 0.0339, giving 31 features with non-zero coefficients. An unpenalized multivariable Cox model (survival::coxph) was then refit on those 31 features. Full results are in cox_lasso_results.tsv.

Strongest effects in the refit:
- Gene_1: HR 14.23 (8.94 to 22.67), p = 4.8e-29
- Gene_2: HR 0.101 (0.064 to 0.158), p = 1.1e-23
- Gene_3: HR 7.46 (5.03 to 11.05), p = 1.4e-23
- Gene_5: HR 6.78 (4.56 to 10.07), p = 2.8e-21
- Gene_4: HR 0.188 (0.124 to 0.284), p = 3.2e-15

Gene_48, Gene_7, Gene_34, Gene_39, Gene_6, Gene_41, Gene_8, Gene_30, Gene_27, Gene_23, Gene_42 and Gene_49 also had p < 0.05, but their effects were much smaller (HR between 0.57 and 1.51). With the more conservative lambda.1se (0.1135), only Gene_1 to Gene_5 are kept.
