# Santana et al. (2024) RNA-seq Validation Analysis

## Study Overview

**Paper**: Santana et al. (2024) - *Candida auris* SCF1 adhesin study  
**BioProject**: [PRJNA904261](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA904261)  
**Galaxy History**: [PRJNA904261 Final](https://usegalaxy.org/u/cartman/h/prjna904261-final)

## Experimental Design

| Sample | Condition | Description | Replicates |
|--------|-----------|-------------|------------|
| AR0382 | Wild-type | Highly adhesive clinical isolate (Clade I) | 2 |
| AR0387 | Alt. strain | Poorly adhesive clinical isolate | 2 |
| AR0382_tnSWI1 | Mutant | SWI1 transposon mutant | 2 |

## RNA-seq Pipeline

**See workflow diagram**: Galaxy dataset #387 (`galaxy_workflow_diagram.png`)

![Workflow Diagram](galaxy_workflow_diagram.png)

### Pre-processing (existing in history)
1. **Raw Data**: 6 paired-end samples (#14)
2. **QC**: FastQC (#274), fastp trimming (#29)
3. **Alignment**: STAR → BAM files (#44)
4. **Quantification**: featureCounts → Counts Table (#211)

### DESeq2 Analysis (this session)
- Split collection #211 into condition-specific collections:
  - **#363**: AR0382 Counts (tag: `name:AR0382`)
  - **#378**: AR0387 Counts (tag: `name:AR0387`)
  - **#381**: AR0382_tnSWI1 Counts (tag: `name:tnSWI1`)

- DESeq2 comparisons:
  - **#382**: AR0382 vs tnSWI1 (replicates Figure 1D)
  - **#384**: AR0382 vs AR0387 (replicates Figure S5A)

## Validation Results

### Gene ID Mapping Challenge

The paper used a different genome annotation version:
- **Paper gene IDs**: 6-digit suffix (e.g., `B9J08_001458`) from GCA_002759435.2
- **Our gene IDs**: 5-digit suffix (e.g., `B9J08_03708`) from GCA_002759435.3

**Solution**: Official NCBI gene ID mapping via the `old_locus_tag` attribute in the GCA_002759435.3 GTF file, which explicitly links v3 gene IDs to their corresponding v2 IDs.

### Comparison 1: AR0382 vs tnSWI1 (Figure 1D)

| Metric | Value |
|--------|-------|
| DEGs mapped | 203/203 |
| Pearson R² | **0.9397** |
| Regression slope | 1.18 |
| Direction agreement | **99.0%** |
| Mean |LFC diff| | 0.413 |

### Comparison 2: AR0382 vs AR0387 (Figure S5A)

| Metric | Value |
|--------|-------|
| DEGs mapped | 165/166 |
| Pearson R² | **0.8884** |
| Regression slope | 1.13 |
| Direction agreement | **97.0%** |
| Mean |LFC diff| | 0.314 |

### Key Gene: SCF1 (Surface Colonization Factor 1)

| Dataset | Gene ID | log2FC | Status |
|---------|---------|--------|--------|
| Paper (Fig 1D) | B9J08_001458 | -6.68 | Most downregulated |
| Our analysis | B9J08_03708 | -6.82 | Confirmed |

*Gene ID mapping validated via NCBI old_locus_tag: B9J08_001458 (v2) → B9J08_03708 (v3)

## Technical Notes

### LFC Direction Reversal

Our DESeq2 analysis used AR0382 as treatment (not reference), resulting in opposite LFC signs compared to the paper. This was detected and corrected automatically by checking correlation sign.

### Gene ID Mapping Method

Gene IDs were mapped using the official NCBI `old_locus_tag` attribute from the GCA_002759435.3 annotation GTF file, which provides the authoritative correspondence between annotation versions.

### Quality Assessment

Both comparisons demonstrate strong reproducibility:
- R² ~0.89-0.94 (strong correlation)
- >97% direction agreement
- Mean LFC differences <0.5
- Regression slopes ~1.1-1.2 (slight systematic difference likely due to different normalization methods)

## Galaxy Artifacts

| HID | Name | Description |
|-----|------|-------------|
| #15 | GTF | C. auris annotation (GCA_002759435.3) |
| #211 | Counts Table | featureCounts output (6 samples) |
| #363 | AR0382 Counts | Wild-type samples (n=2) |
| #378 | AR0387 Counts | Alt. strain samples (n=2) |
| #381 | AR0382_tnSWI1 Counts | Mutant samples (n=2) |
| #382 | DESeq2 Results | AR0382 vs tnSWI1 |
| #384 | DESeq2 Results | AR0382 vs AR0387 |
| #386 | ANALYSIS_REPORT.md | This report |
| #387 | galaxy_workflow_diagram.png | Workflow diagram |

## Conclusions

1. **Reproducibility confirmed**: Strong correlation (R² = 0.94 and 0.89) between our reanalysis and published results
2. **SCF1 validated**: The key finding—SCF1 as the most strongly downregulated gene—is fully reproduced (LFC: -6.68 paper vs -6.82 ours)
3. **Gene ID mapping**: Official NCBI old_locus_tag mapping successfully resolved gene ID discrepancies between annotation versions

## References

- Santana et al. (2024) - Original publication
- Galaxy workflow: RNA-seq for Paired-end fastqs with fasta reference
- Genome annotations: GCA_002759435.2 (paper) and GCA_002759435.3 (our analysis)

---
*Analysis performed: 2024-12-12*
*Generated with Claude Code*
