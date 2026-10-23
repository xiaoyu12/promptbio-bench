# ACMG classification (a-10-3)
| ID | Gene | Consequence | Criteria met | CLASS |
|---|---|---|---|---|
| rsTest1 | BRCA1 | stop_gained, AF=0, ClinVar Pathogenic | PVS1, PM2, PP5 | Pathogenic |
| rsTest2 | GENE1 | synonymous, AF=0.05, ClinVar Benign, SIFT tolerated/PolyPhen benign | BA1, BP4, BP6, BP7 | Benign |
| rsTest3 | GENE2 | missense, AF=1e-5, no ClinVar, SIFT deleterious/PolyPhen probably damaging | PM2, PP3 | VUS |

PM2 + PP3 alone (1 moderate + 1 supporting) is not enough for Likely Pathogenic, so rsTest3 remains a VUS. Full table: acmg_classification.tsv.
