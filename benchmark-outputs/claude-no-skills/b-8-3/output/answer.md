# XGBoost grid search (b-8-3)
Outcome: `Target`; features Feature_1..Feature_100 (PatientID and LengthOfStay excluded). 80/20 split (random_state=42); GridSearchCV with KFold(5, shuffle=True, random_state=42), scoring = R².

- Best parameters: n_estimators = 200, max_depth = 3
- Best 5-fold CV R²: 0.8203
- Test set: R² = 0.8378, RMSE = 5.500, MAE = 4.568
