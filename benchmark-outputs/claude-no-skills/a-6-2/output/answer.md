# Answer a-6-2: 78 ASVs inferred; all 78 predicted as rRNA (16S) by barrnap
- Session resumed after usage-limit interruption (old start time kept in .start_time.interrupted_usage_limit).
- Primers 515F/806R removed with cutadapt (-O 15, -e 0.1, discard untrimmed): 1812/2500 pairs kept.
- DADA2: truncLen 220/180, maxEE 2/2, truncQ 2; pooled single sample; consensus chimera removal -> 78 ASVs (252-255 bp), 1138 reads.
- ASV IDs = md5 of sequence (nf-core/ampliseq convention).
- Taxonomy: DADA2 assignTaxonomy (minBoot 50) with GTDB R07-RS207 DADA2 training set + addSpecies exact match. 69 Bacteria, 9 Archaea.
- rRNA: barrnap 1.10.5 (supports kingdoms bac/arc/fun only; euk/mito options unavailable in this version) run on all ASVs, default e-value 1e-3.
  is_rRNA = TRUE if any kingdom gives an rRNA hit. All 78 ASVs hit 16S_rRNA (bac & arc models) -> is_rRNA TRUE for all.
