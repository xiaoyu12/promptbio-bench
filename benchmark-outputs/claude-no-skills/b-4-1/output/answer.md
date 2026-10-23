# b-4-1: Wilcoxon rank-sum DE, Treated (n=50) vs Control (n=50)
I tested 201 genes (TP53 + GENE_001..GENE_200) with a two-sided Wilcoxon rank-sum (Mann-Whitney U) test and applied Benjamini-Hochberg correction. **19 genes have FDR < 0.05**. 18 are higher in Treated and 1 (GENE_026) is lower in Treated:
GENE_095, GENE_129, GENE_055, GENE_122, GENE_037, GENE_126, GENE_012, GENE_072, GENE_141, GENE_014, GENE_021, GENE_083, GENE_076, GENE_102, GENE_003, GENE_026, GENE_168, GENE_127, GENE_173.
See significant_genes_fdr.csv for the Gene, FDR, raw p-value, U statistic, group medians and means, and direction of each gene.
