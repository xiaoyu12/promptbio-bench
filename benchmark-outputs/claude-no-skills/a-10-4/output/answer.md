# IC50 from 4-parameter logistic (sigmoid) fits

| Drug | IC50 (uM) | 95% CI (uM) | Hill slope | R^2 |
|---|---|---|---|---|
| DrugA | 1.712 | 1.589-1.845 | 0.80 | 0.9999 |
| DrugB | 1.311 | 1.244-1.382 | 0.76 | 0.9999 |

Method: 4PL model V = Bottom + (Top-Bottom)/(1+(c/IC50)^Hill), all parameters free, fitted by least squares (scipy curve_fit) with log10(IC50) parameterisation. DrugB is slightly more potent (lower IC50) than DrugA. Absolute IC50s (concentration giving 50% viability) are nearly identical: 1.727 uM (A), 1.315 uM (B).
