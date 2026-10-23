# a-8-3: Hierarchical clustering heatmap of tissue metabolomes

Output: `clustermap.png`

Method: 60 samples (30 tumor, 30 matched normal) × 570 metabolites. I removed 15 metabolites that had the same value in every sample (mostly drugs/xenobiotics, where a z-score is undefined), leaving 555. Intensities were log2-transformed and z-scored per metabolite across samples. Samples and metabolites were then clustered with Ward linkage on Euclidean distance (seaborn.clustermap), with a RdBu_r colour scale centred at 0 and clipped at ±3. The column sidebar shows TISSUE_TYPE from sample_meta.txt (NORMAL = green, TUMOR = orange).

Result: the first split of the sample dendrogram almost exactly matches tissue type. One cluster has 28 NORMAL samples and no TUMOR samples; the other has all 30 TUMOR samples plus 2 NORMAL samples (58/60 concordant). One large block of metabolites is consistently higher in normal tissue and lower in tumors. Other blocks are higher in tumors, mainly in one tumor subcluster, which suggests metabolic differences among the tumors themselves.
