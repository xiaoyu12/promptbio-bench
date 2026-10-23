# a-4-7: ChIP-seq count profiles (full read vs read end)

`aligned_reads_summary.csv` has one row per genomic window. It contains two count profiles:
- **bases.counted = "each"** counts the full read length. Each unique aligned read is a window `[chromStart, chromEnd)` with count = 1. Duplicate reads, shown by the input `count` column, are not counted.
- **bases.counted = "end"** counts only the base where each read ends. Reads are grouped by end position, giving the window `[chromEnd-1, chromEnd)` with count = the number of unique reads that end there.

| bases.counted | experiment | chrom | windows | median width |
|---|---|---|---|---|
| each | H3K36me3 | chr9 | 28,368 | 100 |
| each | H3K4me3 | chr2 | 12,028 | 99 |
| end | H3K36me3 | chr9 | 25,606 | 1 |
| end | H3K4me3 | chr2 | 8,843 | 1 |

`count_profiles.csv` holds the per-base coverage built from these windows, compressed into runs of equal count (bedGraph style). The highest per-base coverage is 44 for H3K36me3 and 203 for H3K4me3 when full reads are counted, and 6 and 9 when only read ends are counted.
