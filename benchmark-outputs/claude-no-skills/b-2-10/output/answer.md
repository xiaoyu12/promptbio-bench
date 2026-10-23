# Stratified 70/30 split on DiagnosisClass

Method: sklearn `train_test_split(test_size=0.3, stratify=DiagnosisClass, random_state=42)` on 500 patients.

Train set: 350 patients; test set: 150 patients (all 28 original columns kept, values unchanged).

Class,Original_Count,Original_Percentage,Train_Count,Train_Percentage,Test_Count,Test_Percentage
ClassA,192,38.4,134,38.29,58,38.67
ClassB,175,35.0,123,35.14,52,34.67
ClassC,133,26.6,93,26.57,40,26.67


Class proportions are preserved within rounding (max deviation from original 0.33 percentage points); chi-square test of class vs split: chi2=0.0111, p=0.9945.
