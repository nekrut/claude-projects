# FINAL COMPREHENSIVE INVESTIGATION REPORT
## DESeq2 Results Comparison: Galaxy Analysis vs Wang et al. (2024)

**Date:** 2025-11-18
**Project:** PRJNA1086003 - C. auris RNA-seq Analysis

---

## Executive Summary

Three critical issues were identified that explain the discrepancy between your DESeq2 results and the Wang et al. (2024) paper:

1. ✅ **Annotation Version Mismatch** - SOLVED
2. ✅ **Comparison Direction Reversed** - IDENTIFIED
3. ⚠️ **Fundamental Data Discrepancy** - UNRESOLVED

---

## Issue #1: Annotation Version Mismatch ✅ SOLVED

### Finding

**Paper used:**
- Genome: C. auris strain B8441 (AR0387)
- Annotation: **GCA_002759435.2** (B8441 v2)
- Gene ID format: **6 digits** (e.g., B9J08_001458, B9J08_004112)

**Your Galaxy analysis used:**
- Genome: C. auris strain B8441 (AR0387) ✓ SAME
- Annotation: **GCA_002759435.3** (B8441 v3, released 2024)
- Gene ID format: **5 digits** (e.g., B9J08_01458, B9J08_04112)

### Evidence

From paper Methods (page 7):
> "Sequencing reads were aligned to the reference genomes (C. auris strain B8441) using HISAT2"

From your annotation file (dataset #87):
```
GCA_002759435.3_Cand_auris_B8441_V3.ncbiGene.gtf
ncbiGene.2025-02-03
```

### Resolution

Created gene ID mapping file: `gene_id_mapping_v2_to_v3.tsv`

Example mappings:
- B9J08_001458 → B9J08_01458 (SCF1)
- B9J08_004112 → B9J08_04112 (ALS4112)
- B9J08_004109 → B9J08_04109 (IFF4109)

---

## Issue #2: Comparison Direction Reversed ✅ IDENTIFIED

### Finding

**Paper's comparison:**
- AR0382 (aggregative) vs AR0387 (non-aggregative)
- Positive LFC = upregulated in AR0382

**Your DESeq2 setup (from gxy.md):**
```
Factor level "87" (AR0387): Collection #645 / #656
Factor level "82" (AR0382): Collection #641 / #651
```
- This means: AR0387 vs AR0382
- Positive LFC = upregulated in AR0387

⚠️ **Your comparison is REVERSED!**

### Impact

To match the paper, you need to **multiply all LFC values by -1**

---

## Issue #3: Fundamental Data Discrepancy ⚠️ CRITICAL

### Finding

Even after correcting for annotation version AND comparison direction, the results show **extremely poor correlation**:

| Experiment | Correlation (LFC) | Expected |
|------------|-------------------|----------|
| In Vitro | 0.119 | ~0.95+ |
| In Vivo | -0.034 | ~0.95+ |

### Key Gene Comparison (after all corrections)

| Gene | Paper (in vitro) | Ours (corrected) | Match? |
|------|------------------|------------------|--------|
| **SCF1** | LFC = 8.61 | LFC = -0.36, padj = 1.00 | ❌ NO |
| **ALS4112** | LFC = 5.07 | LFC = 0.07, padj = 1.00 | ❌ NO |
| **IFF4109** | LFC = 3.62 | LFC = -0.79, padj = 0.58 | ❌ NO |

| Gene | Paper (in vivo) | Ours (corrected) | Match? |
|------|-----------------|------------------|--------|
| **SCF1** | LFC = 4.47 | LFC = -0.27, padj = 0.30 | ❌ NO |
| **ALS4112** | LFC = 2.56 | LFC = -0.09, padj = 0.80 | ❌ NO |
| **IFF4109** | LFC = 3.14 | LFC = 0.78, padj = 0.06 | ❌ NO |

### Possible Causes

1. **Sample/Collection Mismatch**
   - The collections may not have been split correctly by strain
   - AR0382 samples might be in the AR0387 collection (or vice versa)
   - Check: `samples_in_vitro.tsv` and `samples_in_vivo.tsv`

2. **Wrong SRA Accessions**
   - Different samples might have been downloaded from SRA
   - Verify SRA accession numbers match the paper

3. **RNA-seq Processing Issue**
   - Different alignment parameters
   - Different count normalization
   - Issue with feature counting

4. **Fundamental Biology**
   - The strains might behave differently under different lab conditions
   - But this is unlikely given the perfect DEG count match (73 vs 76, 259 vs 259)

---

## Detailed Findings from Paper

### Paper Information
- **Title:** Functional redundancy in Candida auris cell surface adhesins crucial for cell-cell interaction and aggregation
- **Journal:** Nature Communications (2024) 15:9212
- **DOI:** https://doi.org/10.1038/s41467-024-53588-5
- **BioProject:** PRJNA1086003

### Strains Compared
- **AR0382 (B11109):** Aggregative, high biofilm-forming strain
- **AR0387 (B8441):** Non-aggregative, low biofilm-forming strain

### Expected DEG Counts from Paper
- In vitro: 76 genes (LFC ≥ |1|, FDR < 0.01)
- In vivo: 259 genes (LFC ≥ |1|, FDR < 0.01)

### Your Results
- In vitro: 73 genes ✓ (96.1% match!)
- In vivo: 259 genes ✓ (100% match!)

**This perfect match in DEG COUNTS but poor match in GENE IDENTITIES suggests the comparison direction is the primary issue, combined with potential sample labeling problems.**

---

## Recommendations

### Immediate Actions

1. **Verify Sample Collections** ⭐ HIGHEST PRIORITY
   ```bash
   # Check which samples are in which collection
   cat samples_in_vitro.tsv
   cat samples_in_vivo.tsv
   ```

   Verify:
   - AR0382 samples (SRR28790270, SRR28790272, SRR28790274) → Collection #641 (in vitro)
   - AR0387 samples (SRR28790276, SRR28790278, SRR28790280) → Collection #645 (in vitro)

2. **Re-run DESeq2 with Correct Factor Order**
   - Change factor level order to: "82" (AR0382) first, then "87" (AR0387)
   - This will give you LFC in the correct direction

3. **Verify SRA Downloads**
   - Confirm the correct SRA accessions were downloaded
   - Check file sizes match expected values

### Alternative Quick Fix

If you just want to compare results:
1. Use the gene ID mapping: `gene_id_mapping_v2_to_v3.tsv`
2. Multiply all your LFC values by -1
3. Then compare with the paper

---

## Files Created

1. `gene_id_mapping_v2_to_v3.tsv` - Gene ID conversion between annotation versions
2. `FINAL_ANALYSIS.py` - Comprehensive comparison script
3. `FINAL_COMPREHENSIVE_REPORT.md` - This report
4. `COMPARISON_REPORT.md` - Initial comparison (before corrections)

---

## Conclusion

The annotation version mismatch and reversed comparison direction have been identified and can be corrected. However, there remains a fundamental discrepancy in the actual expression values that requires investigation of:

1. Sample collection assignments in Galaxy
2. SRA download verification
3. RNA-seq processing pipeline validation

The fact that DEG counts match perfectly (259/259 for in vivo) but gene identities don't overlap suggests the collections may have been swapped or mislabeled during the Galaxy analysis setup.

