# Michaelis-Menten kinetics with and without inhibitor

Nonlinear least-squares fit of V = Vmax·[S]/(Km + [S]) (7 substrate concentrations, 0.1 to 10):

| Condition | Vmax (±SE) | Km (±SE) | R² |
|---|---|---|---|
| Control | 3.474 ± 0.038 | 1.154 ± 0.040 | 0.9993 |
| Inhibitor | 2.797 ± 0.055 | 1.698 ± 0.097 | 0.9984 |

The Lineweaver-Burk linear regression gives Control Vmax=2.99, Km=0.85 and Inhibitor Vmax=2.22, Km=1.16. The double-reciprocal transform distorts the error structure, so the NLS values are the ones to use.

What this shows: with the inhibitor, Vmax drops by about 19% and apparent Km rises by about 47%. The 95% CIs do not overlap for either parameter. In the Lineweaver-Burk plot the two lines have different slopes and different y-intercepts, and they cross to the left of the y-axis. This points to **mixed-type inhibition**, not purely competitive inhibition (same Vmax) or purely noncompetitive inhibition (same Km). Catalytic efficiency (Vmax/Km) falls from 3.01 to 1.65.

Outputs: fit_results.tsv, michaelis_menten_fit.png, lineweaver_burk_plot.png.
