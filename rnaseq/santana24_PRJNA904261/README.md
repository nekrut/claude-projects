# Santana et al. (2024) - SCF1 Adhesin Characterization

## Publication
- **Paper**: Santana DJ et al. (2024) "A Candida auris-specific adhesin, Scf1, governs surface association, colonization, and virulence"
- **Journal**: Science
- **NCBI BioProject**: [PRJNA904261](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA904261)

## Comparisons
1. **AR0382 vs tnSWI1** (Figure 1D): 203 DEGs - SWI1 mutant shows loss of SCF1 expression
2. **AR0382 vs AR0387** (Figure S5A): 165 DEGs - strain comparison

## Directory Structure
```
santana24_PRJNA904261/
├── README.md                    # This file
├── ANALYSIS_REPORT.md           # Detailed validation results
├── paper/                       # Publication files
│   ├── nihms-2004453.pdf
│   └── supplements/
├── analysis/
│   ├── validated/               # GTF-based validated results
│   │   ├── gene_mapping_*.csv   # v2→v3 gene ID mapping
│   │   ├── protein_comparison_*.csv
│   │   └── validation_*.png     # LFC correlation plots
│   ├── deprecated/              # Old LFC-based mapping (unreliable)
│   ├── deseq2_*.tsv            # Raw DESeq2 output
│   └── *.csv, *.md             # Supporting files
└── reference/                   # → ../shared_reference (symlink)
```

## Annotation Version Note
- **Paper used**: GCA_002759435.2 (v2) - gene IDs: 6-digit suffix (e.g., B9J08_001458)
- **Our analysis**: GCA_002759435.3 (v3) - gene IDs: 5-digit suffix (e.g., B9J08_03708)
- **Mapping method**: NCBI `old_locus_tag` attribute in v3 GTF

## Validation Results

| Comparison | R² | Direction | Protein Match |
|------------|-----|-----------|---------------|
| AR0382 vs tnSWI1 | 0.9397 | 99% | 100% (167/167) |
| AR0382 vs AR0387 | 0.8884 | 97% | 100% (140/140) |

## Key Genes
- **SCF1** (B9J08_001458→B9J08_03708): Primary adhesin, most strongly downregulated in SWI1 mutant (LFC: -6.68 paper, -6.82 validated)
- **MGD1** (B9J08_000656→B9J08_02614): Methylglyoxalase, stress response gene

---
*Reanalysis performed with Galaxy/DESeq2, validated via protein sequence comparison*
