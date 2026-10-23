# K562 candidate fusion junctions (STAR chimeric detection)

STAR 2.7.11b (two-pass, STAR-Fusion chimeric parameters, `--chimOutJunctionFormat 1`) was run on hg38 with Ensembl 116 junctions.
601 read pairs were aligned, and 551 of them (91.7%) were chimeric, giving 757 chimeric alignments in `K562_Chimeric.out.junction`.
`K562_candidate_fusions.csv` contains every junction line, annotated with genes and support counts.
`is_candidate=True` marks the 145 rows that remain after removing mitochondrial, multimapping and same-gene chimeras.

Top candidate fusions (split reads / spanning pairs):

| Fusion | Split reads | Spanning pairs |
|---|---|---|
| BAG6--SLC44A4 | 30 | 9 |
| BCR--ABL1 | 28 | 19 |
| NUP214--XKR3 | 17 | 9 |
| ARMH3 (C10orf76)--KCNIP2 | 11 | 4 |
| C16orf87--ORC6 | 4 | 0 |
| RCC1--UBE2D2 | 3 | 0 |
| RNF157--ZNF79 | 3 | 0 |
| IMMP2L--DOCK4 | 2 | 1 |
| XACT--LRCH2 | 1 | 2 |

The BCR--ABL1 breakpoint (the Philadelphia chromosome fusion that defines K562) is chr22:23,290,414 (BCR, +) -> chr9:130,854,063 (ABL1, +) in hg38 (12 split reads in this orientation; the remaining split reads support the same junction from the reverse strand).
