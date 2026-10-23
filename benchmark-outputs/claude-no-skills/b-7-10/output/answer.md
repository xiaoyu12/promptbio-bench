# Self-training SVM (b-7-10)
RBF-SVM with Platt probabilities. Stratified 70/30 split; 20% of training set labeled (280 cells), 80% unlabeled (1120). Pseudo-labels with confidence >= 0.8 added each iteration, up to 10 iterations (all 10 performed; 957 cells added, pseudo-label accuracy 93.6%).

- **Initial test accuracy (before self-training): 0.8333**
- **Final test accuracy (after self-training): 0.8867**
- Fully supervised reference (all 1400 training labels): 0.9050
