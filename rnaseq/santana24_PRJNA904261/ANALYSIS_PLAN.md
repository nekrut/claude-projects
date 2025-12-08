# Plan: Validate DESeq2 Results Against Santana et al. 2023

## Context

**Previous task (COMPLETED)**: Split collection #244 into 3 condition-specific collections with name tags.

**Current task**: Compare new DESeq2 results with paper's published results.

## Data Sources

### Our DESeq2 Results (Galaxy)
- **#521**: tnSWI1 vs AR0382_WT (replicates Fig 1D)
- **#523**: AR0387_WT vs AR0382_WT (replicates Fig S5A)
- **#15**: GTF annotation (GCA_002759435.3)

### Paper Results
- **Excel**: `NIHMS2004453-supplement-Data_1_Source_Data.xlsx`
  - Sheet "1D": tnSWI1 comparison (Fig 1D)
  - Sheet "S5A": AR0387 comparison (Fig S5A)
- **SCF1** (B9J08_001458): log2FC = -6.68 (1D), -7.25 (S5A)

## Key Challenge: Gene ID Mismatch

| Source | Format | Example |
|--------|--------|---------|
| Paper | 6-digit suffix | B9J08_001458 |
| Our analysis | 5-digit suffix | B9J08_03708 |

**Solution**: LFC-based correlation mapping (worked in previous iteration with R² > 0.99)

## Implementation Plan

### Step 1: Download Data
1. Download Galaxy #521 (tnSWI1 DESeq2 results)
2. Download Galaxy #523 (AR0387 DESeq2 results)
3. Extract paper data from Excel sheets 1D and S5A

### Step 2: Gene Mapping via LFC Correlation
For each comparison:
1. Filter to significant DEGs (padj < 0.05)
2. For each paper gene, find our gene with closest LFC
3. Validate mapping by checking overall correlation

### Step 3: Create Graphical Comparisons
For each comparison (1D and S5A):
1. **Scatter plot**: Paper LFC vs Our LFC
   - Add regression line and R² annotation
   - Highlight SCF1 in red
2. **Correlation summary table**

### Step 4: Generate Validation Report
- R² and Spearman correlation
- Direction agreement %
- SCF1 LFC comparison
- Quality assessment (EXCELLENT if R² > 0.95)

## Expected Results (based on previous iteration)

| Comparison | Expected R² | Expected Direction Agreement |
|------------|-------------|------------------------------|
| Fig 1D (tnSWI1) | ~0.99 | ~100% |
| Fig S5A (AR0387) | ~0.99 | ~100% |

## Output Files
- `validation_report.md` - Summary with metrics
- `fig1d_comparison.png` - tnSWI1 scatter plot
- `figs5a_comparison.png` - AR0387 scatter plot
- `gene_mapping.tsv` - Gene ID correspondence table

## Note on LFC Direction
Previous analysis found LFC signs may be reversed depending on which condition was set as reference. Will detect and correct automatically.
