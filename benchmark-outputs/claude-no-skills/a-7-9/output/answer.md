# a-7-9 answer
I ran a chi-square test of independence on m6A status (Hyper, Hypo, no sig) against DEG status (Up, Down, no-DEGs). It used all 12,754 rows of the MeRIP-seq table.
- Result: chi-square = 901.45, df = 4, **p = 8.10e-194**.
- m6A modification status and differential expression are strongly associated.
  - Hyper-methylated transcripts are enriched among up-regulated genes: 106 Up vs 12 Down.
  - Hypo-methylated transcripts are enriched among down-regulated genes: 119 Down vs 9 Up.

Figures: p_value_distribution.png and effect_size_distribution.png. Each is a 2x2 grid with panels for proteomic, m6A methylation, gene expression and all three combined.
