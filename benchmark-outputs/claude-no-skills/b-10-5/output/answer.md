# Soft-voting ensemble vs individual models (test set, n=150; 70/30 stratified split, random_state=42; positive class = Tumor)

| Model | Accuracy | AUC |
|---|---|---|
| Random Forest | 0.860 | 0.947 |
| SVM | 0.913 | 0.958 |
| Logistic Regression | 0.833 | 0.925 |
| Soft Voting Ensemble | 0.860 | 0.951 |

The soft-voting ensemble (AUC 0.951, accuracy 0.860) beats Random Forest and Logistic Regression on AUC and matches or beats them on accuracy. It does not beat the best single model: the SVM was highest on both accuracy (0.913) and AUC (0.958).
