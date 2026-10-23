# b-5-1: Hierarchical clustering (Ward, Euclidean) on standardized data

- Data: 120 samples x 10 features, each feature z-scored (mean 0, SD 1) with StandardScaler.
- Ward linkage on Euclidean distance (scipy). The dendrogram is in `hierarchical_dendrogram.png`: samples on the x axis, linkage distance on the y axis.
- Structure: there are three well-separated main clusters. The largest merge heights are 31.5 and 26.2, then a big drop to 14.0. Cutting at k=3 gives sizes 42 / 36 / 42:
  - samples S36-S71 plus a small subgroup S108-S113
  - S72-S107
  - S0-S35 plus a small outlying subgroup S114-S119
- The cophenetic correlation is 0.73.
