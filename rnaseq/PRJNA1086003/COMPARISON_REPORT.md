# DESeq2 Results Comparison: Our Analysis vs Wang et al. (2024)

## Summary

Comparison of DESeq2 differential expression analysis results between our replication and the original paper by Wang et al. (2024).

**Paper:** "Functional redundancy in Candida auris cell surface adhesins crucial for cell-cell interaction and aggregation"
**DOI:** https://doi.org/10.1038/s41467-024-53588-5

## Overall DEG Count Comparison

| Experiment | Our Results | Paper | Difference | Match % |
|------------|-------------|-------|------------|---------|
| **In Vitro** | 73 DEGs | 76 DEGs | -3 | 96.1% |
| **In Vivo** | 259 DEGs | 259 DEGs | 0 | 100% |

**Filtering criteria:** |log2FoldChange| ≥ 1, padj < 0.01

## ✓ Excellent Match in DEG Counts

The overall number of differentially expressed genes matches the paper almost perfectly:
- **In vitro:** 73 vs 76 expected (only 3 fewer, 96.1% match)
- **In vivo:** 259 vs 259 expected (perfect 100% match)

This suggests our DESeq2 analysis pipeline and parameters are correctly configured.

## ⚠️ Key Adhesin Genes NOT Significant

The paper identifies three key cell surface adhesin genes as highly upregulated in AR0382 (aggregative strain):
- **SCF1** (B9J08_01458) - Cell surface adhesin with Flo11 domain
- **ALS4112** (B9J08_04112) - Als-family adhesin
- **IFF4109** (B9J08_04109) - IFF/HYR1 family adhesin

However, **NONE of these genes are significantly differentially expressed in our results:**

### In Vitro Results

| Gene | LFC | padj | Status |
|------|-----|------|--------|
| SCF1 (B9J08_01458) | 0.36 | 1.00 | ✗ Not significant |
| ALS4112 (B9J08_04112) | -0.07 | 1.00 | ✗ Not significant |
| IFF4109 (B9J08_04109) | 0.79 | 0.58 | ✗ Not significant |

### In Vivo Results

| Gene | LFC | padj | Status |
|------|-----|------|--------|
| SCF1 (B9J08_01458) | 0.27 | 0.30 | ✗ Not significant |
| ALS4112 (B9J08_04112) | 0.09 | 0.80 | ✗ Not significant |
| IFF4109 (B9J08_04109) | -0.78 | 0.06 | ✗ Not significant |

## Top Differentially Expressed Genes

### In Vitro - Top 5 Upregulated

| Gene ID | LFC | padj |
|---------|-----|------|
| B9J08_03209 | 14.98 | 4.75e-32 |
| B9J08_00020 | 6.09 | 2.92e-53 |
| B9J08_05490 | 5.26 | 6.51e-12 |
| B9J08_02614 | 4.28 | 1.48e-63 |
| B9J08_01838 | 4.04 | 1.36e-19 |

### In Vivo - Top 5 Upregulated

| Gene ID | LFC | padj |
|---------|-----|------|
| B9J08_03209 | 8.68 | 2.50e-71 |
| B9J08_00017 | 3.25 | 3.92e-11 |
| B9J08_00020 | 3.15 | 4.30e-11 |
| B9J08_00019 | 2.89 | 2.77e-04 |
| B9J08_01766 | 2.74 | 1.85e-06 |

**Note:** B9J08_03209 is the most highly upregulated gene in both experiments.

## Possible Explanations for Discrepancy

### 1. Factor Level Ordering in DESeq2

The direction of log2FoldChange depends on which condition is the reference:
- Our setup: Factor level "87" (AR0387) vs "82" (AR0382)
- Positive LFC = upregulated in which strain?
- This needs verification with the DESeq2 setup

**Important:** The factor level order in DESeq2 determines the sign of LFC values:
- If AR0387 is the reference: positive LFC = upregulated in AR0387, negative LFC = upregulated in AR0382
- If AR0382 is the reference: positive LFC = upregulated in AR0382, negative LFC = upregulated in AR0387

### 2. Gene Annotation Differences

- Our IDs use format: B9J08_XXXXX (no leading zeros)
- Paper IDs use format: B9J08_00XXXX (with leading zeros)
- Could the gene IDs refer to different loci?

### 3. Assembly or Annotation Version

- Different genome assembly versions might have different gene IDs
- The paper might have used a different annotation set

## Recommendations

1. **Verify factor level ordering:** Check which strain is the reference in our DESeq2 analysis
2. **Download paper's supplementary data:** Compare our full gene lists with theirs
3. **Check gene annotations:** Verify that our gene IDs map correctly to the paper's IDs
4. **Examine top genes:** Investigate what B9J08_03209 is (the top gene in our results)
5. **Review DESeq2 parameters:** Ensure beta priors and other settings match the paper

## Files Generated

- `deseq2_in_vitro_results.tsv` - Full DESeq2 results for in vitro experiment
- `deseq2_in_vivo_results.tsv` - Full DESeq2 results for in vivo experiment
- `deseq2_in_vitro_significant.tsv` - Filtered significant DEGs (in vitro)
- `deseq2_in_vivo_significant.tsv` - Filtered significant DEGs (in vivo)

## Analysis Date

Generated: 2025-11-18
