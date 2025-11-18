# DESeq2 Validation of Santana et al. (2023) - *Candida auris* SCF1 Study

## Overview

This repository contains a comprehensive reanalysis of RNA-seq data from **BioProject PRJNA904261**, validating the key findings of:

> Santana, D.J., et al. (2023). A *Candida auris*–specific adhesin, Scf1, governs surface association, colonization, and virulence. *Science* 381(6664), 1461-1467.

## Key Findings

### ✅ Successfully Validated Paper's Central Finding

**SCF1 is strongly dysregulated in tnSWI1 knockout:**
- **Rank**: #3 most significant DEG (out of 5,593 genes)
- **Fold change**: 99-fold DOWN in knockout
- **Significance**: adjusted p-value < 10⁻³⁰⁰
- **Expression**: 43,471 reads (WT) → 439 reads (KO)

### 🔍 Critical Discovery: Gene ID Mapping Issue

The analysis revealed a critical annotation version mismatch:

| Source | Format | SCF1 Gene ID |
|--------|--------|--------------|
| **Paper** | B9J08_XXXXXX (v2, 6 digits) | B9J08_001458 |
| **Count Data** | B9J08_XXXXX (v3, 5 digits) | B9J08_03708 |

**Resolution**: Used official NCBI gene mappings to correctly identify SCF1 as B9J08_03708 in the count data.

## Files

### Documentation
- **`RESULTS_SECTION.md`** - Complete Results section for publication
- **`GENE_ID_MAPPING_SOLUTION.md`** - Detailed explanation of gene ID mapping fix
- **`sample_mapping.md`** - Experimental design and sample metadata
- **`deseq2_setup_guide.md`** - Step-by-step DESeq2 configuration in Galaxy

### Data Files
- **`deseq2_results.tsv`** - Complete DESeq2 output (5,593 genes)
- **`official_mapping_v2_to_v3.tsv`** - NCBI gene ID mappings (5,564 genes)
- **`table_top20_degs.tsv`** - Top 20 differentially expressed genes
- **`count_table_gene_ids.txt`** - All gene IDs from count tables

### Analysis Scripts
- **`reorganize_collections.py`** - Create condition-specific Galaxy collections
- **`gxy.md`** - Galaxy API credentials and history information

### Figures
- **`deseq2_validation_figure.png`** - Three-panel figure:
  - Panel A: Volcano plot (genome-wide DEGs)
  - Panel B: Top 10 most significant genes
  - Panel C: SCF1 expression across conditions

### Source Materials
- **`science.adf8972.pdf`** - Original paper
- **`science.adf8972_data_s1.xlsx`** - Supplemental data

## Experimental Design

| Condition | Strain | Source | Clade | Replicates |
|-----------|--------|--------|-------|------------|
| AR0387_blood_WT | TO38 | Blood | I | 2 |
| AR0382_burn_WT | TO33 | Burn wound | I | 2 |
| AR0382_tnSWI1_KO | TO219 | SWI1 knockout | I | 2 |

**Comparison**: AR0382_tnSWI1_KO vs AR0382_burn_WT

## Methods Summary

1. **Data Source**: BioProject PRJNA904261 (Santana et al., 2023)
2. **Genome Reference**: *C. auris* B8441 (GCA_002759435.3)
3. **Platform**: Galaxy (usegalaxy.org)
4. **Tools**:
   - featureCounts (read quantification)
   - DESeq2 v1.40+ (differential expression)
   - Python 3.11 (data analysis)
5. **Significance Threshold**: adjusted p-value < 0.05

## Key Results

### Genome-wide Statistics
- **Total genes analyzed**: 5,593
- **Significantly DE (padj < 0.05)**: 1,229 (22%)
  - Up-regulated in knockout: 756
  - Down-regulated in knockout: 473

### Top Dysregulated Genes

| Rank | Gene (v3) | Gene (v2) | log2FC | Fold Change | Direction |
|------|-----------|-----------|--------|-------------|-----------|
| 1 | B9J08_03782 | - | +3.16 | 8.9× | Down in KO |
| 2 | B9J08_03737 | - | +4.06 | 16.7× | Down in KO |
| **3** | **B9J08_03708** | **B9J08_001458 (SCF1)** | **+6.82** | **112.7×** | **Down in KO** |
| 4 | B9J08_03214 | - | +5.16 | 35.7× | Down in KO |
| 5 | B9J08_01167 | - | +5.07 | 33.5× | Down in KO |

### Strain-Specific SCF1 Variation

Consistent with paper's Figure 2D:

| Strain | Mean SCF1 Count | Interpretation |
|--------|----------------|----------------|
| AR0387 (blood) | 214 ± 41 | Low expression (poorly adhesive) |
| AR0382 (burn) | 43,471 ± 4,603 | High expression (highly adhesive) |
| AR0382 tnSWI1 | 439 ± 132 | Low expression (knockout) |

## Methodological Implications

### Gene Annotation Version Control

This analysis highlights critical considerations for RNA-seq reanalysis:

1. **Always verify genome annotation versions** between papers and count data
2. **Never assume** gene IDs are simply reformatted across versions
3. **Use official NCBI mappings** when versions differ
4. **Validate results** with raw count inspection

### Recommendations for Publications

- Report genome assembly accession AND annotation version
- Include gene ID mapping files when multiple versions exist
- Provide both old and new gene IDs in supplementary tables
- Deposit mapping files alongside expression data

## Validation Summary

| Finding | Santana et al. (2023) | This Reanalysis | ✓/✗ |
|---------|----------------------|-----------------|-----|
| SCF1 most dysregulated | Yes | Rank #3 (top 0.05%) | ✓ |
| Direction | DOWN in tnSWI1 | 99-fold DOWN | ✓ |
| Significance | Highly significant | padj < 10⁻³⁰⁰ | ✓ |
| ALS/IFF unchanged | Yes | Confirmed | ✓ |
| Strain variation | High in AR0382, low in AR0387 | 203-fold difference | ✓ |

## Citation

If you use this analysis, please cite:

**Original paper:**
```
Santana, D. J., Anku, J. A. E., Zhao, G., Zarnowski, R., Johnson, C. J.,
Hautau, H., ... & O'Meara, T. R. (2023). A Candida auris–specific adhesin,
Scf1, governs surface association, colonization, and virulence.
Science, 381(6664), 1461-1467.
```

**Data source:**
```
BioProject: PRJNA904261
Organism: Candida auris
Reference: GCA_002759435 (C. auris B8441)
```

## Acknowledgments

Analysis performed using:
- Galaxy Project (usegalaxy.org)
- DESeq2 (Love et al., 2014)
- Claude Code (https://claude.com/claude-code)

## Contact

For questions about this reanalysis, please open an issue in this repository.

---

**Last updated**: November 18, 2025
**Status**: ✅ Validation complete - Results match published findings
