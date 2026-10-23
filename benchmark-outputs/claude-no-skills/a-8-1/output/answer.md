# a-8-1: LC-MS peak annotation against HMDB (+/-0.01 Da)

How it was done: each HMDB neutral monoisotopic mass was converted to a positive-mode [M+H]+ m/z (adds 1.007276 Da). Candidates within +/-0.01 Da of each query were kept. They were ranked by |ppm error| and the top 3 were reported. The full table is in annotations.csv.

| query_mz | top candidates (HMDB) | formula | ppm_error | candidates within tol |
|---|---|---|---|---|
| 132.1012 | L-Isoleucine (HMDB00172), L-Alloisoleucine (HMDB00557), L-Leucine (HMDB00687) | C6H13NO2 | -5.33 | 7 (all C6H13NO2 isomers) |
| 287.2389 | Vitamin A / retinol (HMDB00305), 11-cis-Retinol (HMDB06216), 9-cis-Retinol (HMDB06217) | C20H30O | +6.82 | 5 |
| 556.2771 | Enkephalin L (HMDB01045) | C28H37N5O7 | +0.94 | 1 |

Isomers that share a formula have the same ppm error, so their order (by HMDB ID) is arbitrary. MS1 mass alone cannot tell them apart.
If the m/z values are instead matched straight to neutral masses with no adduct, the hits are only 1-Nitrohexane for 132.1012 and Quinidine barbiturate for 556.2771, and nothing matches 287.2389. That table is in tmp/annotations_neutral_mass.csv.
