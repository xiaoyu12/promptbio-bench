# T-cell sub-clustering (pbmc3k, SingleR T_cells, n = 1411)
Re-normalized subset, 2000 HVGs, PCA (10 PCs), Louvain res 0.8, UMAP; markers via Seurat FindAllMarkers (Wilcoxon).

| Subcluster | n | Annotation | Top markers |
|---|---|---|---|
| 0 | 346 | CD4 memory | USP10, TIMP1, PLP2, CD40LG, S100A4, S100A11, VIM |
| 1 | 274 | CD8 naive | CCR7, LEF1, CD8B, FHIT, AIF1, PIK3IP1 |
| 2 | 202 | CD4 memory, IFN-stimulated (weak Treg signal: FOXP3/IL2RA/CTLA4 slightly higher) | ISG15, IFI6, MX1, STAT1, TNFSF10 |
| 3 | 193 | CD4 naive | CCR7, JUNB, NPM1, ribosomal genes |
| 4 | 159 | Low-quality / MALAT1-high T cells | MALAT1, RPL13, RPL32 |
| 5 | 134 | CD8 effector (cytotoxic) | GZMH, FGFBP2, GZMB, CCL4, NKG7, FCGR3A |
| 6 | 94 | CD8 GZMK+ / MAIT-like | NCR3, GZMK, KLRB1, HOPX, KLRG1 |
| 7 | 9 | T/B doublets | CD79A, MS4A1, TCL1A, FCER2 |

Regulatory T cells did not form a separate cluster (only 10 FOXP3+ cells in this dataset).
Files: tcell_subclusters_umap.png, tcell_top_markers_per_cluster.csv (top 10 per cluster, p_val_adj<0.05).
