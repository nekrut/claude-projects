# Summary: DESeq2 Analysis for PRJNA1086003

## What Was Accomplished

Successfully set up and ran DESeq2 differential expression analysis in Galaxy to replicate the experiments from:
**Wang et al. (2024) "Functional redundancy in Candida auris cell surface adhesins crucial for cell-cell interaction and aggregation"**

## Data Organization

### 1. Sample Files Created
- `samples_in_vitro.tsv` - 6 samples from in vitro biofilm experiment
- `samples_in_vivo.tsv` - 7 samples from in vivo catheter experiment
- Both files include group tags for Galaxy (format: `group:sample_name`)

### 2. Galaxy Collections Created

**Original:**
- Collection #601: Counts Table (all 13 samples)

**Experiment-specific:**
- Collection #621: PRJNA1086003_in_vitro (6 samples)
- Collection #629: PRJNA1086003_in_vivo (7 samples)

**Strain-specific sub-collections:**
- Collection #641: PRJNA1086003_in_vitro_AR0382 (3 samples, aggregative strain)
- Collection #645: PRJNA1086003_in_vitro_AR0387 (3 samples, non-aggregative strain)
- Collection #651: PRJNA1086003_in_vivo_AR0382 (3 samples, aggregative strain)
- Collection #656: PRJNA1086003_in_vivo_AR0387 (4 samples, non-aggregative strain)

### 3. Group Tags Added
All 13 datasets tagged with their sample names (e.g., `group:82_Bio_1`, `group:87-1`)

## DESeq2 Analysis Setup

### Correct Methodology
**Each factor level (strain) receives its own collection**

**In vitro experiment:**
```
Factor: strain
  - Level "87" (AR0387, non-aggregative): Collection #645 (n=3)
  - Level "82" (AR0382, aggregative): Collection #641 (n=3)
```

**In vivo experiment:**
```
Factor: strain
  - Level "87" (AR0387, non-aggregative): Collection #656 (n=4)
  - Level "82" (AR0382, aggregative): Collection #651 (n=3)
```

### Analysis Parameters
- Tool: DESeq2 v2.11.40.8+galaxy0
- FDR threshold: 0.01 (α = 0.01)
- LFC threshold: 0 (post-filter for |LFC| ≥ 1)
- Beta priors: False
- Comparison: Strain 82 (aggregative) vs Strain 87 (non-aggregative)

## Expected Results

Based on the paper:
- **In vitro:** ~76 differentially expressed genes
- **In vivo:** ~259 differentially expressed genes

### Key genes to verify:
The top upregulated genes in AR0382 should include:
- **SCF1** (B9J08_001458) - Cell surface adhesin with Flo11 domain
- **ALS4112** (B9J08_004112) - Als-family adhesin
- **IFF4109** (B9J08_004109) - IFF/HYR1 family adhesin
- Additional IFF/HYR1 family members

## Files Created

### Analysis Scripts
1. `split_collection.py` - Split original collection by experiment
2. `add_tags_to_collections.py` - Added group tags to datasets
3. `run_deseq2_proper.py` - **Final correct DESeq2 submission** ✓

### Documentation
1. `samples_in_vitro.tsv` - In vitro sample metadata
2. `samples_in_vivo.tsv` - In vivo sample metadata
3. `gxy.md` - Galaxy artifacts and collection tracking
4. `DESEQ2_ANALYSIS.md` - Detailed analysis documentation
5. `SUMMARY.md` - This file

## How to Check Results

1. Visit: https://usegalaxy.org/u/cartman/h/prjna1086003
2. Look for the most recent DESeq2 outputs:
   - DESeq2 result file (tabular file with gene statistics)
   - DESeq2 plots (diagnostic plots)
3. Download the result files
4. Filter for genes with:
   - |log2FoldChange| ≥ 1
   - padj (adjusted p-value) < 0.01
5. Compare with Supplementary Data from the paper

## Key Learning

**DESeq2 in Galaxy requires separate collections for each experimental condition when using the "collections" mode.**

Incorrect approach:
- ✗ Single collection with all samples + factor file
- ✗ Splitting within DESeq2 using sample names

Correct approach:
- ✓ Pre-split samples into strain-specific collections
- ✓ Feed each collection as a separate factor level to DESeq2
