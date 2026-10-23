# DIA-NN label-free quantification (a-7-8)
DIA-NN 1.8.1 library-free workflow: in-silico predicted library from REF_EColi_K12_UPS1_combined.fasta (Trypsin/P, 1 missed cleavage, CAM fixed, M-ox variable, pep length 15-30, charge 2-3, precursor m/z 350-950, fragment m/z 500-1500), searched against RD139_Narrow_UPS1_0_1fmol_inj1.mzML at 1% precursor FDR (MS2/MS1 mass accuracy 10/5 ppm, since automatic calibration was impossible with so few IDs).

The mzML covers only 10.0-16.7 min of the gradient, so very few peptides are present: 3 precursors (2 peptides) from 2 E. coli proteins (gltX/P04805, rplB/P60422) passed 1% FDR; no UPS1 proteins were identified at 0.1 fmol. The precursor-level report is in report.tsv.
