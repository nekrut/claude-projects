# Critical Gene ID Mapping Issue - RESOLVED

## Problem Discovery

While preparing protein sequence FASTA files for DEG comparison, I discovered a **critical mapping error** in how gene IDs were being converted between C. auris B8441 annotation versions v2 and v3.

## The Bug

### What I Initially Did (WRONG ❌)
I assumed that gene IDs were simply reformatted between versions by removing leading zeros:
- `B9J08_001458` (v2) → `B9J08_01458` (v3)
- `B9J08_004451` (v2) → `B9J08_04451` (v3)
- `B9J08_000592` (v2) → `B9J08_00592` (v3)

### What Actually Happened
**Genes were completely renumbered** between v2 and v3 annotations! The actual NCBI mappings are:
- `B9J08_001458` (v2) → `B9J08_03708` (v3) ✓
- `B9J08_004451` (v2) → `B9J08_05205` (v3) ✓
- `B9J08_000592` (v2) → `B9J08_02550` (v3) ✓

## Evidence

### Protein Sequence Comparison
When I compared protein sequences extracted using my incorrect mapping:
- **Only 2-5% sequence overlap** between v2 and v3 FASTA files
- Different protein lengths (e.g., B9J08_001458: 765 aa in v2 vs 247 aa in "v3")
- This proved I was mapping **completely different genes together**

### With Correct NCBI Mapping
After extracting the official mapping from NCBI's feature table:
- **100% sequence overlap** for paper's DEGs ✓
- **99%+ sequence overlap** for our DEGs ✓
- Identical protein sequences confirm correct mapping

## Root Cause

The v3 annotation (GCA_002759435.3) was a major update:
1. Scaffolds were joined into complete chromosomes
2. All genes were renumbered in their new genomic context
3. Chromosome names changed (PEKT02000007.1 → CM076438.1)
4. Assembly level upgraded from "Scaffold" to "Chromosome"

**NCBI's v3 assembly report explicitly states**: "Reference guided assembly: GCA_002759435.2"

## Solution

Extracted official gene ID mapping from NCBI's v3 feature table using the `old_locus_tag` attribute:

```python
# From v3_feature_table.txt
attributes: "old_locus_tag=B9J08_001530"
# This tells us: B9J08_00001 (v3) = B9J08_001530 (v2)
```

Created mapping files:
- `official_mapping_v2_to_v3.tsv` (5,563 mappings)
- `official_mapping_v3_to_v2.tsv` (5,563 mappings)

## Impact

### Original (Incorrect) Files
- Datasets #675-682 in Galaxy history
- **These FASTA files contain WRONG proteins** ⚠️
- Mapped different genes together

### Corrected Files
- Datasets #683-690 in Galaxy history ✓
- Protein sequences verified to match 100% between versions
- Ready for comparative analysis

### Affected DEG Lists
Created corrected DEG lists:
- `paper_vitro_degs_corrected.tsv` (76 DEGs, 100% mapped)
- `paper_vivo_degs_corrected.tsv` (259 DEGs, 100% mapped)
- `our_vitro_degs_corrected.tsv` (109 DEGs, 98% mapped)
- `our_vivo_degs_corrected.tsv` (920 DEGs, 99% mapped)

## Files Created

### Mapping Files
1. `official_mapping_v2_to_v3.tsv` - Official NCBI gene ID mappings
2. `official_mapping_v3_to_v2.tsv` - Reverse mapping
3. `v3_feature_table.txt` - Source of official mappings

### Corrected DEG Lists
4. `paper_vitro_degs_corrected.tsv`
5. `paper_vivo_degs_corrected.tsv`
6. `our_vitro_degs_corrected.tsv`
7. `our_vivo_degs_corrected.tsv`

### Corrected Protein FASTA Files (in Galaxy #683-690)
8. `paper_vitro_degs_v2.fasta` (76 sequences)
9. `paper_vitro_degs_v3.fasta` (76 sequences)
10. `our_vitro_degs_v2.fasta` (107 sequences)
11. `our_vitro_degs_v3.fasta` (109 sequences)
12. `paper_vivo_degs_v2.fasta` (259 sequences)
13. `paper_vivo_degs_v3.fasta` (259 sequences)
14. `our_vivo_degs_v2.fasta` (913 sequences)
15. `our_vivo_degs_v3.fasta` (919 sequences)

### Analysis Scripts
16. `extract_official_mapping.py` - Extract mappings from NCBI feature table
17. `rebuild_deg_lists_correct.py` - Rebuild DEG lists with correct mappings
18. `extract_deg_proteins_fixed.py` - Extract proteins (updated to use corrected lists)
19. `compare_protein_sequences.py` - Verify sequence overlap
20. `investigate_mapping.py` - Investigation that revealed the bug

## Verification

### Paper's DEGs
- ✓ 100% of v2 genes successfully mapped to v3
- ✓ 100% protein sequence overlap between versions
- ✓ Identical sequences confirm same genes

### Our DEGs
- ✓ 98-99% mapped successfully
- ✓ 99%+ protein sequence overlap
- Missing genes are likely new in v3 or removed in v2

## Lesson Learned

**Never assume gene ID formats across annotation versions!**

Even when gene IDs look similar, major assembly updates can completely renumber genes. Always check:
1. NCBI assembly reports for version changes
2. Feature tables for official mappings
3. Protein sequences to verify correctness

## Next Steps

Use the corrected FASTA files (Galaxy datasets #683-690) for:
1. BLAST searches
2. Functional annotation comparison
3. Sequence alignment
4. GO term enrichment

The corrected files now contain the **actual proteins** for each DEG, making meaningful biological comparisons possible.
