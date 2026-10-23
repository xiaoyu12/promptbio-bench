# Random Forest: b-7-1
- Setup: 500-tree Random Forest, stratified 70/30 split (random_state=42), PatientID dropped, categorical variables encoded ("None" kept as its own category).
- **Test accuracy: 0.8133** (122/150 correct; ROC AUC 0.908).
- Top 10 features by impurity-based importance: Age (0.270), BMI (0.071), Glucose (0.062), Family_History_Diabetes (0.060), Family_History_Heart_Disease (0.057), Cholesterol (0.045), Albumin (0.041), HeartRate (0.040), Hemoglobin (0.040), Platelet_Count (0.040).
- Age is by far the strongest predictor. Ranks 6-10 are close to the noise level of the other continuous lab values.
