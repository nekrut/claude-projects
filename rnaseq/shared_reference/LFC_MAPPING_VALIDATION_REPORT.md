# LFC Mapping Validation Report

## Summary
- **LFC-matched pairs**: 203
- **Correct matches (vs NCBI old_locus_tag)**: 2 (1.0%)

## Correlation Analysis
| Method | R² |
|--------|-----|
| LFC matching | 0.9996 |
| NCBI official mapping | 0.9397 |
| NCBI official (sign flipped) | 0.9397 |

## Conclusion
The LFC-based matching achieved high R² (0.9996) but matched **wrong genes**. 
Only 2/203 pairs (1.0%) match the official NCBI gene ID correspondence.

The official NCBI mapping (via old_locus_tag in v3 GTF) achieves R² = 0.9397 when 
accounting for the reversed comparison direction.

**The LFC matching method found genes with coincidentally similar fold changes, not the actual 
corresponding genes between annotation versions.**

## Recommendation
Use the official NCBI old_locus_tag mapping from GCA_002759435.3 GTF for gene ID conversion 
between v2 (6-digit) and v3 (5-digit) annotations.
