# Moran's I for primate traits (a-12-4)
Method: ape::Moran.I, with weights = 1 / cophenetic (patristic) distance from the tree and diagonal = 0; the p-value is two-sided (normal approximation). Expected I = -0.25.

| Trait | Moran's I | P (two-sided) |
|---|---|---|
| body | -0.0731 | 0.0471 |
| longevity | -0.1838 | 0.4675 |

Body mass shows significant phylogenetic autocorrelation (observed I is greater than expected, p < 0.05). Longevity does not (p = 0.47).
