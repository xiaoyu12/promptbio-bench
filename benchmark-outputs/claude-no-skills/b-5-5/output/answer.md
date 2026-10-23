# K-means consensus (k=3, 50 runs, master seed 42)
I z-scored the features, then ran K-means 50 times (k=3, n_init=1, k-means++). Each run's seed was drawn from np.random.RandomState(42). Consensus[i,j] is the fraction of runs in which samples i and j were in the same cluster.
- consensus_matrix.csv: a 120x120 symmetric matrix with values in [0,1] and a diagonal of 1.
- consensus_matrix_heatmap.png: a heatmap with samples ordered by average-linkage clustering of 1 - consensus.

The matrix has three clean blocks of 42, 36 and 42 samples. Every pairwise value is either 0.14 or less, or 0.86 or more, so the 3-cluster solution is very stable across random starts.
