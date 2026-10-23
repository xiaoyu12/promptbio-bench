LSTM (21-day window -> 7-day horizon, 64/32 ReLU LSTM + Dropout 0.2, Dense16, Dense7; Adam/MSE, batch 32, early stopping patience 10 on 20% validation split).
Test RMSE (original ICU-occupancy units, all 7 horizons pooled, 68 test sequences): **10.31** (seed 42; across 5 seeds 10.21 +/- 0.17).
