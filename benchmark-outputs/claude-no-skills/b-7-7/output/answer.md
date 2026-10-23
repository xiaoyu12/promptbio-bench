# Decision tree: drug response prediction (b-7-7)

**Setup.** 800 patients, 65 features (clinical + pharmacogene variants + 50 SNPs). I split the data 70/30 with stratification (560 train, 240 test, random_state=42). The model is a scikit-learn DecisionTreeClassifier. Its hyperparameters were tuned by 10x repeated stratified 5-fold CV on the training set only. The selected settings were Gini, max_depth=3 and min_samples_leaf=40.

**Test accuracy: 0.7417** (majority-class baseline 0.600). Balanced accuracy 0.708, ROC AUC 0.723.

**Top 10 features (Gini importance):**
1. CYP2D6_variant 0.362
2. CYP3A4_variant 0.355
3. Disease_Stage 0.255
4. SNP_26 0.027

Ranks 5-10 (Baseline_Marker_A, Baseline_Marker_B, ABCB1_variant, SNP_44, Kidney_Function, SNP_5) have an importance of 0 in the pruned final tree. They are ordered by their mean importance across the cross-validation refits.

The pruned tree is driven by the CYP2D6 and CYP3A4 metabolizer variants and by disease stage. Patients with no CYP2D6 or CYP3A4 variant and an early stage (I-II) are predicted to respond.
