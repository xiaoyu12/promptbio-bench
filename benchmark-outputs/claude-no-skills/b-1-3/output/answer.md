# Coefficient of variation (CV%) per numeric feature

CV% = sample SD (ddof=1) / |mean| x 100. The table covers the 20 numeric columns of bio_dataset.csv (n=300), sorted from highest to lowest CV. The full table is in coefficient_of_variation.csv.

- Highest relative variability: Troponin_level (255.4%), IL6_concentration (86.6%), CRP_level (86.4%), IFNgamma_concentration (78.9%), Neutrophil_count (76.7%).
- Lowest: RBC_count (1.96%), Sodium_concentration (2.12%), Glucose_level (12.8%), HistoneH3_abundance (14.5%), GeneA_expression (14.8%).

Inflammatory and injury markers (troponin, IL-6, CRP, IFN-gamma) vary the most. Tightly regulated quantities (sodium, RBC count, glucose) vary the least.
Caveat: some columns contain zero or negative values, such as IFN-gamma with 100 zeros and Tcell_activation_stage. CV is less meaningful for those columns.
