# PCA of RNA-seq counts (log2(x+1), per-gene z-score)

Plot: `pca_rnaseq_plot.png`. It shows PC1 on the x-axis and PC2 on the y-axis. Samples are coloured by tumor/normal group.

- PC1 explains 43.8% of the variance and PC2 explains 39.3%. Together they explain 83.1%; every later PC explains less than 1.5%.
- The 30 normal samples form one tight cluster on the negative side of PC1.
- The 60 tumor samples separate from the normals and split into two distinct sub-clusters of 30 samples each, which may be two tumor subtypes.
