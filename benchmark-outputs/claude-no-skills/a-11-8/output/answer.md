# Cross-layer hub genes

I merged the STRING PPI network (14 genes, 75 edges) and the miRNA–target network (8 miRNAs, 16 edges) into one undirected two-layer network with 23 nodes (15 genes and 8 miRNAs) and 91 edges. I then computed degree centrality, defined as degree divided by (N−1).

The 90th-percentile threshold is 0.636 (14/22). Six genes are tied at this maximum value, so a strict ">" would select no genes. I therefore counted genes at the threshold as hubs (DC ≥ P90).

**Cross-layer hub genes (DC = 0.636 each):** KRAS, MYC, AKT1, EGFR, PIK3CA and TP53. All six have both PPI and miRNA-target edges. KRAS, PIK3CA and TP53 are each targeted by two miRNAs.
