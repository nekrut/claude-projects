# Session Summary: Gene ID Mapping Investigation & Fix

## Starting Point

You suspected there was an issue with gene IDs based on the observation that:
- Number of DEGs was very similar between paper and our analysis
- BUT the actual genes and fold changes didn't match well

You requested: *"Can you pull protein sequences for in_vivo and vitro degs for paper and my annotations and put them into four separate datasets in my galaxy history: (1) my DEGs v2, (2) my DEGs v3, (3) their DEGs v2, (3) their DEGs v3?"*

## What We Discovered

### Initial Analysis
1. Created 8 FASTA files (split by in_vitro/in_vivo as well)
2. Uploaded to Galaxy as datasets #675-682
3. Compared protein sequences between v2 and v3 annotations

### Critical Finding
**Only 2-5% of protein sequences matched between v2 and v3!**

This revealed that my gene ID mapping was completely wrong.

### The Root Cause
I had assumed gene IDs were simply reformatted:
- B9J08_001458 (v2) → B9J08_01458 (v3) by removing leading zeros

**But genes were actually completely renumbered:**
- B9J08_001458 (v2) → B9J08_03708 (v3) (actual mapping!)

### The Fix
1. Downloaded NCBI v3 feature table
2. Extracted official mappings from `old_locus_tag` attributes
3. Created 5,563 gene ID mappings (v2 ↔ v3)
4. Rebuilt all DEG lists with correct mappings
5. Re-extracted protein sequences
6. Verified 100% sequence overlap (for paper's DEGs)

## Results

### Corrected Files in Galaxy
**New datasets #683-690** (replace the incorrect #675-682):

#### In Vitro DEGs
- #683: Paper in_vitro DEGs (v2 annotation) - 76 sequences ✓
- #684: Paper in_vitro DEGs (v3 annotation) - 76 sequences ✓
- #685: Our in_vitro DEGs (v2 annotation) - 107 sequences ✓
- #686: Our in_vitro DEGs (v3 annotation) - 109 sequences ✓

#### In Vivo DEGs
- #687: Paper in_vivo DEGs (v2 annotation) - 259 sequences ✓
- #688: Paper in_vivo DEGs (v3 annotation) - 259 sequences ✓
- #689: Our in_vivo DEGs (v2 annotation) - 913 sequences ✓
- #690: Our in_vivo DEGs (v3 annotation) - 919 sequences ✓

### Verification Results
- Paper's DEGs: **100% sequence overlap** between v2 and v3 ✓
- Our DEGs: **99%+ sequence overlap** between v2 and v3 ✓

This confirms the corrected mappings are accurate.

### Key Files Created
1. **official_mapping_v2_to_v3.tsv** - Official NCBI gene mappings (5,563 genes)
2. **official_mapping_v3_to_v2.tsv** - Reverse mappings
3. **paper_vitro_degs_corrected.tsv** - Corrected DEG list
4. **paper_vivo_degs_corrected.tsv** - Corrected DEG list
5. **our_vitro_degs_corrected.tsv** - Corrected DEG list
6. **our_vivo_degs_corrected.tsv** - Corrected DEG list
7. **CRITICAL_GENE_ID_MAPPING_FIX.md** - Detailed documentation

## Why This Matters

The original FASTA files contained **the wrong proteins**! Using them for:
- BLAST searches → Would search wrong sequences
- Functional analysis → Would analyze wrong genes
- Sequence comparisons → Would compare different genes

The corrected files now contain the **actual proteins** corresponding to each DEG, enabling:
- Accurate sequence-based comparisons
- Proper functional annotation
- Valid BLAST searches
- Meaningful biological interpretation

## Your Intuition Was Correct!

You suspected there was a gene ID issue based on the similar DEG counts but different results. This investigation confirmed and fixed that exact problem.

## Next Steps

You can now use the corrected FASTA files (datasets #683-690) for:
1. LexicMap analysis in Galaxy
2. BLAST searches against databases
3. Functional domain identification
4. Sequence-based clustering
5. GO term enrichment

The corrected mappings also enable proper comparison of your DESeq2 results with the paper's results, since we now know which v3 genes correspond to which v2 genes.
