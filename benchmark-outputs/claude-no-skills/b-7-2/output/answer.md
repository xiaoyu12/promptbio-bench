# SVM classification of Outcome (b-7-2)
Stratified 70/30 split (350/150, seed 42); standardized numeric + one-hot categorical features; SVC tuned by 5-fold CV ROC-AUC on the training set (best: RBF kernel, C=100, gamma=0.001; CV AUC 0.968).

| Set | Accuracy | Precision | Recall | Specificity | F1 | AUC |
|---|---|---|---|---|---|---|
| Train | 0.923 | 0.935 | 0.909 | 0.937 | 0.922 | 0.977 |
| Test | 0.867 | 0.867 | 0.867 | 0.867 | 0.867 | 0.949 |

Modest train-test gap; the model generalizes well (test AUC 0.949). See roc_curves.png, classification_report.csv, svm_performance_metrics.csv.
