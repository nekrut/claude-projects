# Phase 2: DESeq2 Results Validation

## Prerequisites

- DESeq2 results downloaded from Galaxy:
  - `analysis/deseq2_tnSWI1.tsv`
  - `analysis/deseq2_AR0387.tsv`
- Publication supplement: `NIHMS2004453-supplement-Data_1_Source_Data.xlsx`

## The Gene ID Problem

**Issue**: Publication and our analysis use different genome annotation versions.

| Source | Annotation | Format | SCF1 ID |
|--------|------------|--------|---------|
| Publication | v2 | 6-digit | B9J08_001458 |
| Our counts | v3 | 5-digit | B9J08_03708 |

**Solution**: LFC-based correlation mapping. Genes with identical expression produce identical fold changes, enabling unambiguous matching.

## Running Validation

```bash
cd /home/anton/git/claude-projects/rnaseq/santana24_PRJNA904261_try3

# Validate both comparisons
python scripts/validate.py \
    --supplement ../santana24_PRJNA904261/NIHMS2004453-supplement-Data_1_Source_Data.xlsx \
    --deseq2-tnswi1 analysis/deseq2_tnSWI1.tsv \
    --deseq2-ar0387 analysis/deseq2_AR0387.tsv \
    --output-dir analysis/
```

## Outputs

| File | Description |
|------|-------------|
| `gene_mapping_tnSWI1.csv` | v2→v3 ID mapping for comparison 1 |
| `gene_mapping_AR0387.csv` | v2→v3 ID mapping for comparison 2 |
| `validation_tnSWI1.png` | Correlation + Bland-Altman plot |
| `validation_AR0387.png` | Correlation + Bland-Altman plot |
| `validation_report.txt` | Summary statistics |

## Interpreting Results

### Correlation Metrics

| Metric | Excellent | Good | Acceptable |
|--------|-----------|------|------------|
| Pearson R² | >0.99 | >0.95 | >0.90 |
| Spearman R | >0.99 | >0.95 | >0.90 |
| Direction match | 100% | >95% | >90% |

### Key Validation Points

1. **SCF1 confirmation**: B9J08_03708 should be most downregulated gene
2. **Direction agreement**: All mapped genes should have same LFC sign
3. **Low systematic bias**: Mean LFC difference near zero in Bland-Altman plot

## Expected Results

### Comparison 1: AR0382 vs tnSWI1

| Metric | Expected |
|--------|----------|
| Mapped genes | ~200 |
| Pearson R² | 0.999+ |
| Direction match | 100% |
| SCF1 LFC | ~-6.8 |

### Comparison 2: AR0382 vs AR0387

| Metric | Expected |
|--------|----------|
| Mapped genes | ~165 |
| Pearson R² | 0.989+ |
| Direction match | 100% |
| SCF1 LFC | ~-7.3 |

## Manual Verification

Check SCF1 in both datasets:
```python
import pandas as pd

# Our results
deseq = pd.read_csv('analysis/deseq2_tnSWI1.tsv', sep='\t', header=None)
scf1 = deseq[deseq[0] == 'B9J08_03708']
print(f"SCF1 LFC: {scf1[2].values[0]:.2f}")
```
