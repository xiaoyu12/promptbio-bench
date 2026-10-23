# Random Forest: default vs balanced class weights (AUPRC on 30% test set)
| Configuration | AUPRC |
|---|---|
| Default (class_weight=None) | 0.8821 |
| Balanced (class_weight='balanced') | 0.8844 |

Stratified 70/30 split (random_state=42), RF with 100 trees. Outcome prevalence about 33%, so baseline AUPRC is about 0.34. Balanced weighting changed AUPRC only slightly (+0.002), and ROC AUC was the same (0.949). Across 20 random splits, the mean AUPRC was 0.861 for default and 0.849 for balanced, so neither setting is clearly better.
