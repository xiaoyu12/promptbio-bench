# GRAVY-based solubility prediction and solubility-improving mutations

**Original sequence (76 aa, ubiquitin):**
`MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG`

- Original GRAVY (Kyte-Doolittle mean): **-0.489474**
- Original solubility = 1/(1+exp(2*GRAVY)) = **0.726899**

## Top 3 single-point mutations (hydrophobic -> hydrophilic)

| rank | mutation | position | original | mutant | mutant GRAVY | mutant solubility | solubility gain |
|---|---|---|---|---|---|---|---|
| 1 | I3R  | 3  | I | R | -0.607895 | 0.771322 | +0.044422 |
| 2 | I13R | 13 | I | R | -0.607895 | 0.771322 | +0.044422 |
| 3 | I23R | 23 | I | R | -0.607895 | 0.771322 | +0.044422 |

All 91 hydrophobic→hydrophilic single substitutions were evaluated. Since GRAVY is the mean hydropathy, the gain depends only on the change in Kyte-Doolittle value, so the maximum improvement comes from Ile (+4.5) → Arg (-4.5), a change of -9.0 / 76 = -0.118421 in GRAVY. All seven isoleucine positions (3, 13, 23, 30, 36, 44, 61) give exactly this same, maximal gain; ties were broken by ascending position.

## Best mutant

- Best mutation: **I3R**
- Best mutant sequence: `MQRFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG`
- Best mutant GRAVY: **-0.607895**
- Best mutant solubility: **0.771322** (gain +0.044422 over the wild type)
