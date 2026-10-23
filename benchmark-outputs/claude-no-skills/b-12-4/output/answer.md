# b-12-4 answer
Median EarlyShrinkage = 1.3943; ShrinkageGroup = 1 if above median (50 patients) else 0 (50 patients).
Cox PH (Efron ties): coef = -0.963, HR = 0.382 (95% CI 0.243-0.599), p = 2.8e-5 (LRT p = 2e-5); PH assumption holds (cox.zph p = 0.67).
Predicted survival at t = 52 weeks: ShrinkageGroup 0 = 0.0393; ShrinkageGroup 1 = 0.2906.
Per-patient predictions: survival_predictions.csv.
