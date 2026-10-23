# TCR clonotype diversity (a-9-5)
Shannon H = -sum p ln p, Gini-Simpson = 1 - sum p^2; p = clonotype count / total (';'-separated counts summed per CDR3nt row).

| sample | shannon | gini (Gini-Simpson) | clonotypes |
|---|---|---|---|
| sample1_1 | 2.142 | 0.820 | 187 |
| sample1_2 | 2.340 | 0.829 | 2218 |
| sample2_1 | 6.027 | 0.990 | 2484 |
| sample3_1 | 1.806 | 0.790 | 134 |

The files are dominated by IGK clonotypes. If only TR chains are counted: Shannon 4.07 / 4.22 / 4.32 / 3.88 and Gini-Simpson 0.980 / 0.983 / 0.985 / 0.977. These values are in the extra columns of the CSV.
