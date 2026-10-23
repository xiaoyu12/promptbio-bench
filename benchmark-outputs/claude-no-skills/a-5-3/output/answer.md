# Trajectory inference (a-5-3)
Mouse retina scRNA-seq (3,806 cells, 2 samples). I used Scanpy for preprocessing and Harmony to integrate the two samples, then clustered the cells with Leiden into 12 clusters. Trajectories were inferred with Slingshot on 30 Harmony PCs, rooted in the Muller glia cluster, using a Euclidean cluster-centroid MST. Microglia were left out of the trajectory. The principal curves were projected onto the UMAP (output/trajectory.png).

Lineages (cluster IDs):
1. 8 Muller glia -> 3 reactive MG/progenitor-like -> 0 -> 5 -> 7 -> 6 (neurons; cluster 6 is low-UMI, so this end point may be a quality artifact)
2. 8 -> 3 -> 0 -> 5 -> 2 Bipolar-like
3. 8 -> 3 -> 0 -> 1 -> 4 Photoreceptor-like
4. 8 -> 3 -> 0 -> 5 -> 10 Amacrine-like
5. 8 -> 3 -> 0 -> 11 Gap43+ RGC-like

Cluster labels come from marker genes and are provisional.
