# GO ORA: ASXL1 vs Control (blood)

DESeq2 (~ sex + condition) found 2,099 DE genes (padj < 0.05; 1,144 up, 955 down in ASXL1). I ran an ORA with clusterProfiler enrichGO (GO BP, BH correction). The universe was the 22,961 tested genes. 186 terms were significant (padj < 0.05).

Top 10 GO terms by adjusted p-value:

| Rank | GO ID | Term | GeneRatio | p.adjust |
|---|---|---|---|---|
| 1 | GO:0042110 | T cell activation | 87/1349 | 1.78e-04 |
| 2 | GO:0006935 | chemotaxis | 64/1349 | 1.78e-04 |
| 3 | GO:0042330 | taxis | 64/1349 | 1.78e-04 |
| 4 | GO:0061564 | axon development | 66/1349 | 2.21e-04 |
| 5 | GO:0007409 | axonogenesis | 59/1349 | 4.96e-04 |
| 6 | GO:0098742 | cell-cell adhesion via plasma-membrane adhesion molecules | 35/1349 | 4.96e-04 |
| 7 | GO:0048667 | cell morphogenesis involved in neuron differentiation | 72/1349 | 4.96e-04 |
| 8 | GO:0002694 | regulation of leukocyte activation | 86/1349 | 4.96e-04 |
| 9 | GO:0009952 | anterior/posterior pattern specification | 30/1349 | 4.96e-04 |
| 10 | GO:0007411 | axon guidance | 34/1349 | 4.96e-04 |

Plot: GO_BarPlot_Issy_ASXL1_blood.png
