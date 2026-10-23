# WGCNA on combined RNA + protein data vs Disease

Method: R/WGCNA 1.73. RNA (100) and protein (100) features were row-bound (prefixed RNA_/Prot_) into 200 features x 20 samples. Unsigned network, soft power 4 (lowest power with scale-free R^2 >= 0.8), blockwiseModules (minModuleSize 10, mergeCutHeight 0.25). Each module eigengene was Pearson-correlated with Disease (0/1), with Student p-values (n = 20).

| Module | n features | r (Disease) | p-value |
|---|---|---|---|
| red | 15 | -0.572 | 0.0084 |
| brown | 18 | 0.255 | 0.277 |
| blue | 28 | -0.235 | 0.320 |
| pink | 13 | 0.230 | 0.330 |
| green | 16 | -0.205 | 0.386 |
| yellow | 18 | 0.126 | 0.596 |
| grey (unassigned) | 16 | -0.124 | 0.601 |
| greenyellow | 10 | -0.122 | 0.609 |
| purple | 12 | 0.102 | 0.670 |
| magenta | 13 | 0.055 | 0.819 |
| turquoise | 28 | 0.040 | 0.868 |
| black | 13 | -0.008 | 0.972 |

Only the **red module** (RNA and protein of Gene33, 38, 40, 84, 90, 95, 97 plus RNA_Gene74) is significantly associated with disease at nominal p < 0.05. It is negatively correlated (r = -0.57, p = 0.008), so its features are lower in diseased samples. It does not pass BH correction across the 12 modules (FDR = 0.10). Files: module_trait_correlations.csv, wgcna_module_trait_heatmap.png.
