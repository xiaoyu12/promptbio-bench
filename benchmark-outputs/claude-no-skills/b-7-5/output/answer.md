KNN (k=5, standardized features, stratified 70/30 split, random_state=42; 150 test samples):
- Euclidean: test accuracy 0.7067
- Manhattan: test accuracy 0.7400
Manhattan did slightly better on this split. Across 20 random splits the two metrics averaged about the same (~0.723), so the gap is within split-to-split noise.
