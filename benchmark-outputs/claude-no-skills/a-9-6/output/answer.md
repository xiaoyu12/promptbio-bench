# Clonotype distribution across clusters (a-9-6)

Method: the 10x Cell Ranger VDJ contigs were collapsed to one clonotype per cell (`raw_clonotype_id`). They were then joined to the cluster labels by barcode, giving 29 cells, 10 clonotypes and 5 clusters. Cells were then counted per clonotype and cluster. Note: the contigs are immunoglobulin chains (IGH/IGK/IGL), so these are BCR clonotypes, even though the question says TCR.

| clonotype | c1 | c2 | c3 | c4 | c5 | total |
|---|---|---|---|---|---|---|
| clonotype1 | 4 | 0 | 0 | 0 | 0 | 4 |
| clonotype2 | 1 | 2 | 0 | 0 | 0 | 3 |
| clonotype3 | 2 | 1 | 0 | 0 | 0 | 3 |
| clonotype4 | 0 | 1 | 2 | 0 | 0 | 3 |
| clonotype5 | 1 | 0 | 1 | 1 | 0 | 3 |
| clonotype6 | 2 | 0 | 0 | 0 | 1 | 3 |
| clonotype7 | 1 | 1 | 1 | 0 | 0 | 3 |
| clonotype8 | 1 | 1 | 1 | 0 | 0 | 3 |
| clonotype9 | 0 | 1 | 0 | 0 | 1 | 2 |
| clonotype10 | 0 | 0 | 0 | 2 | 0 | 2 |

Key observations: clonotype1, the largest clone, is found only in cluster 1 (4 cells). clonotype10 is found only in cluster 4. Every other clonotype is spread over 2 or 3 clusters. Cluster 1 holds the most clonally expanded cells (12 of 29).

Heatmap: `clonotype_cluster_heatmap.png`. The full table, including CDR3 sequences, is at `tmp/clonotype_cluster_counts.csv`.
