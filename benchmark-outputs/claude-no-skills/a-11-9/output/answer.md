# Louvain community detection on the STRING PPI network

- Network: 14 proteins, 75 edges (density 0.82); edges weighted by the STRING combined score.
- Louvain (networkx, resolution 1.0, best of 100 seeds) found **2 communities**:
  1. AKT1, APC, COL18A1, EGFR, KRAS, NF1, PIK3CA, PTEN (RTK/RAS/PI3K signalling)
  2. BRCA1, CDKN2A, MYC, RB1, TERT, TP53 (cell cycle / genome maintenance)
- **Modularity Q = 0.0047** (weighted). Without weights, the best Louvain Q is 0.027.
- What this means: Q is close to 0, far below the ~0.3 usually taken as clear community structure. The network is close to a clique of cancer driver genes, so the split is weak and changes between runs (4 different partitions over 100 seeds).
