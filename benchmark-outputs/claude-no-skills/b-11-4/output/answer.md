# Bayesian vs frequentist linear regression: Drug_Response ~ Age + Genetic_Variant_Count (n = 150)

Priors: beta_j ~ N(0, 100) for each coefficient, sigma^2 ~ InvGamma(1, 1). Posterior from a Gibbs sampler (4 chains, 60,000 post-burn-in draws, R-hat ~ 1.000). Credible intervals are 95% equal-tailed.

| Parameter | Posterior mean [95% CrI] | OLS estimate [95% CI] | p-value |
|---|---|---|---|
| Intercept | 8.290 [6.487, 10.104] | 8.352 [6.521, 10.184] | 9.9e-16 |
| Age | -0.1165 [-0.1471, -0.0858] | -0.1174 [-0.1483, -0.0865] | 5.5e-12 |
| Genetic_Variant_Count | 1.208 [1.015, 1.402] | 1.205 [1.010, 1.400] | 4.5e-24 |
| sigma^2 | 6.99 [5.56, 8.77] | 6.97 [5.62, 8.89] | NA |

How to read it: each additional year of age lowers the expected drug response by about 0.12 units. Each additional genetic variant raises it by about 1.2 units. Both effects are clearly non-zero: P(beta_Age < 0) and P(beta_GVC > 0) are about 1, and the OLS p-values are below 1e-11. R^2 = 0.58. With 150 observations, the weakly informative priors have little effect, so the Bayesian and frequentist estimates and intervals almost match. The Bayesian intercept is pulled slightly toward 0, by about 0.06.
