# Notes (a-4-8)
- Input rows are aligned read intervals (~100 bp, overlapping, sorted); `count` = number of identical reads. They were converted to a run-length coverage profile (sum of counts over overlapping reads; zero-coverage gaps kept), then adjacent runs with equal coverage were merged.
- Model: PeakSeg = Poisson segmentation with up-down constraint (alternating background/peak), solved exactly with PeakSegOptimal::PeakSegPDPAchrom (CRAN; weights = run lengths), max.peaks=2; selected the 2-peak (5-segment) model.
- H3K36me3 (chr9): peaks 111629703-111693572 (mean 15.7) and 111781275-111869506 (mean 13.5); Poisson loss -3170882.
- H3K4me3 (chr2): peaks 175458034-175463035 (mean 125.0) and 175496130-175499598 (mean 129.0); Poisson loss -4544522.
- Files: tmp/segment.R, tmp/segments_2peaks.tsv, tmp/loss_2peaks.tsv, tmp/coverage.bedGraph.tsv.
