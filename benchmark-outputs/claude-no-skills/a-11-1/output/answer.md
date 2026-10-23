# STRING PPI network for the 14 DEGs

**Method.** Gene symbols were mapped to human STRING identifiers (taxon 9606) using the STRING v12.5 REST API. The network was retrieved with the `/network` endpoint: functional network, combined score >= 0.4 (medium confidence), plus 10 first-shell interacting partners. It was then drawn with networkx: query genes are red, interacting partners are light blue, and edge width scales with the combined score.

**Result.** The network has 207 unique interactions among 23 connected proteins (13 query genes and 10 partners). 112 edges have score >= 0.7 and 55 have score >= 0.9.
- The 10 added partners are ARID1A, CCNE1, CDKN2B, MDM4, MLH1, NF2, PMS2, RET, ROS1 and TCHP.
- The 13 mapped query genes are almost fully interconnected: 72 query-query edges.
- The most connected proteins are TP53, KRAS, PIK3CA, PTEN and EGFR (degree 22), followed by BRCA1, CDKN2A and AKT1 (21).

**Caveat (VEGFA).** STRING v12.x has no VEGFA protein entry, and its resolver silently maps "VEGFA" to COL18A1. That mapping was rejected, so VEGFA appears as an isolated red node in the figure. A supplementary run on STRING v11.5, where VEGFA is present, is in `tmp/supp_v11.5/`.

Files: `ppi_network.csv` (edge list with preferredName_A, preferredName_B, score and the channel sub-scores) and `ppi_network.png`.
