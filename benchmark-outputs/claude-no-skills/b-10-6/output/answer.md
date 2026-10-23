# Linear regression: LOOCV vs single 80-20 split

OLS linear regression (intercept + all 50 features, n = 500) was evaluated in two ways.

| Method | MSE | RMSE | MAE | R2 |
|---|---|---|---|---|
| LOOCV (500 folds, pooled predictions) | 1.0519 | 1.0256 | 0.8123 | 0.8882 |
| Train-test split 80-20 (random_state=42, 100 test samples) | 0.9442 | 0.9717 | 0.8034 | 0.9022 |

The two methods agree closely: R2 is about 0.89-0.90 and RMSE is about 1.0, compared with a Target SD of about 3.07.
The single split gives somewhat lower error (MSE 0.94 vs 1.05), but that gap comes from which samples land in the test set.
Over 100 random 80-20 splits, test MSE was 1.11 +/- 0.14 (range 0.78-1.38) and R2 was 0.879 +/- 0.021. The seed-42 split is on the optimistic side, while the LOOCV estimate falls well inside that range.
LOOCV uses every sample for testing and fits on 499 of 500 samples, so it gives a nearly unbiased, deterministic estimate.
A single 80-20 split is cheaper but has high variance, because it rests on only 100 test points.
Both estimates are above the in-sample training error (MSE 0.85), as expected for a model with 50 predictors.
