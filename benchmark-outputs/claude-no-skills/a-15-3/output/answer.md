# SPT5 targets: ChIP-seq and RNA-seq integration
SPT5 targets are genes with an SPT5 ChIP-seq peak, assigned by HOMER to the nearest TSS, that were also measured in the RNA-seq table. log2FC = log2((mean TPM KO + 1)/(mean TPM WT + 1)).

| Gene | log2FC (KO vs WT) | Peak annotation |
|---|---|---|
| YBL109W | -1.12 | exon |
| YDR543C | 0.00 | promoter-TSS |
| YKL225W | 0.40 | promoter-TSS |
| RDN5-1 | 0.63 | TTS / rDNA (strongest peak) |

YHL050W-B has no SPT5 peak (the nearby peak is assigned to YHL050W-A), so it is not a target. Only YBL109W changes by more than 2-fold: it goes down in the KO. Full table: SPT5_target_log2FC.csv.
