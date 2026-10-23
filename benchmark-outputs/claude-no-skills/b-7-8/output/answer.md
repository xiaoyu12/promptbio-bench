# SVM: Alzheimer's vs control (50 genes, stratified 70/30 split, seed 42, standardized features)

| Model | Test Accuracy | AUC |
|---|---|---|
| SVM (Linear kernel, C=1) | 0.7083 | 0.8203 |
| SVM (RBF kernel, C=1, gamma='scale') | 0.7583 | 0.8644 |

The RBF kernel did a little better on the held-out test set (n=120). The gap is small and within sampling noise: 5-fold CV AUC on the training set was 0.893 for the linear model and 0.870 for RBF.
