# Clustered heatmap (b-3-1)
`clustered_heatmap.png` shows the 100 genes as rows and the 20 samples as columns. Each cell is colored by the gene's row-wise Z-score: (value - gene mean) / gene SD.
Rows and columns were both clustered hierarchically with the default settings (average linkage, Euclidean distance; seaborn clustermap). All gene and sample names are labelled.
The samples split into two main clusters: Sample_1-10 and Sample_11-20. Most genes have higher relative expression in Sample_11-20.
