# a-6-5 summary
- Alpha diversity (AlphaDiversity_results.csv): CF samples have lower diversity than Healthy: Shannon median 4.80 vs 5.22 (Wilcoxon p=0.014), Gini-Simpson 0.982 vs 0.991 (p=0.026); Chao1 richness 455 vs 518.5 (p=0.077, n.s.). Chao1 equals observed richness because the table has no singletons.
- Differential abundance (differential_ASVs.csv): DESeq2 (~group, CF vs Healthy, poscounts size factors, Wald test, BH). 259 ASVs have padj < 0.05: 97 are enriched in CF and 162 are depleted in CF.
