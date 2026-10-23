# ML phylogeny of HOXA1 orthologs (a-12-1)
- Alignment: MAFFT L-INS-i (4 seqs, 1011 aligned columns).
- ML inference: IQ-TREE 3 with ModelFinder (best BIC model HKY+F+I), 1000 ultrafast bootstraps + 1000 SH-aLRT.
- Tree (Newick, `aligned.fasta.treefile`): `(HOXA1_1:0.0054823021,(HOXA1_3:0.0550300813,HOXA1_4:0.7494944279)86.6/88:0.0611261660,HOXA1_2:0.0023372788);`
- HOXA1_1 and HOXA1_2 are nearly identical sisters; HOXA1_3 is closer to them; HOXA1_4 is highly divergent (~0.75 subs/site). Split {HOXA1_1,HOXA1_2}|{HOXA1_3,HOXA1_4} support: SH-aLRT 86.6%, UFBoot 88%.
- Figure `phylo_tree.png`: midpoint-rooted, branch lengths in substitutions/site, leaves labeled by sequence ID.
