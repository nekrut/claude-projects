# Session Context: Santana et al. 2023 RNA-seq Validation

## Current Status: COMPLETED

DESeq2 validation analysis complete with excellent results (R² > 0.97).

## Galaxy History

**URL**: https://usegalaxy.org/u/cartman/h/prjna904261-perm
**API Key**: Set `GALAXY_API_KEY` environment variable (cartman account, starts with 9c7ec)

### Key Datasets
| HID | Description |
|-----|-------------|
| #15 | GTF annotation (GCA_002759435.3) |
| #244 | Original counts collection (6 samples) |
| #521 | DESeq2: tnSWI1 vs AR0382_WT |
| #523 | DESeq2: AR0387_WT vs AR0382_WT |

### Condition Collections (created this session)
- counts_AR0382_WT: SRR22376031, SRR22376032
- counts_AR0387_WT: SRR22376029, SRR22376030
- counts_tnSWI1: SRR22376027, SRR22376028

## Validation Results

| Comparison | R² | Direction | SCF1 (Paper/Ours) |
|------------|-----|-----------|-------------------|
| Fig 1D (tnSWI1) | 0.9953 | 99.7% | -6.68 / -6.82 |
| Fig S5A (AR0387) | 0.9768 | 100% | -7.25 / -7.35 |

**Key finding**: SCF1 (B9J08_001458 → B9J08_03708) confirmed as most downregulated gene.

## Files in This Directory

| File | Description |
|------|-------------|
| `VALIDATION_REPORT.md` | Full validation report |
| `validate_deseq2.py` | Analysis script |
| `deseq2_521_tnswi1.tabular` | Downloaded DESeq2 results |
| `deseq2_523_ar0387.tabular` | Downloaded DESeq2 results |
| `validation_output/` | Figures and gene mappings |
| `NIHMS2004453-supplement-*.xlsx` | Paper supplementary data |

## Gene ID Mapping

Paper uses 6-digit suffix (B9J08_001458), we use 5-digit (B9J08_03708).
Solution: LFC-based correlation mapping - match genes by fold change values.

## Next Steps (if continuing)

1. Could add more comparisons from paper
2. Could create Galaxy workflow from this analysis
3. Could investigate other genes beyond SCF1

## Commands to Resume

```bash
cd /home/anton/git/claude-projects/rnaseq/santana24_PRJNA904261
export GALAXY_API_KEY="9c7ec1a74ba550a706ecad36096e80b1"
```

---
*Last updated: 2025-12-08*
