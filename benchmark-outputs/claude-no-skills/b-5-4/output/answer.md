# GMM (3 components, full covariance, random_state=42) on bio_dataset.csv

Fit with sklearn GaussianMixture on the raw feature_1 and feature_2 values (no scaling). EM converged in 2 iterations, with mean log-likelihood -1.937 per sample and BIC 546.3.

| Component | Weight | Mean (f1, f2) | Covariance [[c00, c01],[c10, c11]] | n assigned |
|---|---|---|---|---|
| 0 | 0.3336 | (-1.3218, -0.6790) | [[0.1387, 0.0044],[0.0044, 0.1274]] | 40 |
| 1 | 0.3498 | (0.6312, 1.2529) | [[0.1111, 0.0008],[0.0008, 0.1942]] | 42 |
| 2 | 0.3166 | (0.6951, -0.6689) | [[0.1254, -0.0077],[-0.0077, 0.1421]] | 38 |

The data separates into three well-separated, roughly spherical clusters of about the same size. Each has a weight of about 1/3, a variance of about 0.11–0.19 and almost no correlation between the two features.
Files: gmm_cluster_plot.png (ellipses at 1/2/3 SD) and gmm_parameters.csv.
