# Wang et al. (2024) - Glycan-Lectin Interactions in *C. auris*

## Publication
- **Paper**: Wang Y et al. (2024) "Cell surface glycan-lectin interactions modulate *Candida auris* colonization and fungemia"
- **Journal**: Nature Communications
- **DOI**: [10.1038/s41467-024-50434-4](https://doi.org/10.1038/s41467-024-50434-4)
- **NCBI BioProject**: [PRJNA1086003](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1086003)

## Comparisons
1. **In Vitro** (AR0382 vs AR0387): 76 DEGs - aggregative vs non-aggregative strains
2. **In Vivo** (AR0382 vs AR0387): 259 DEGs - mouse kidney colonization

## Directory Structure
```
wang24_PRJNA1086003/
├── README.md                    # This file
├── ANALYSIS_REPORT.md           # Detailed validation results
├── paper/                       # Publication files
│   ├── s41467-024-53588-5.pdf
│   ├── wang24_invitro_publication.csv
│   ├── wang24_invivo_publication.csv
│   └── supplements/
├── analysis/
│   ├── validated/               # GTF-based validated results
│   │   └── protein_comparison_*.csv
│   ├── deprecated/              # Old LFC-based mapping (unreliable)
│   │   └── gene_mapping_by_lfc*.csv
│   ├── deseq2_*.tsv            # Raw DESeq2 output
│   └── *.csv                   # Comparison and overlap files
└── reference/                   # → ../shared_reference (symlink)
```

## Annotation Version Note
- **Paper used**: GCA_002759435.2 (v2) - gene IDs: 6-digit suffix (e.g., B9J08_001458)
- **Our analysis**: GCA_002759435.3 (v3) - gene IDs: 5-digit suffix (e.g., B9J08_03708)
- **Mapping method**: NCBI `old_locus_tag` attribute in v3 GTF

## Validation Results

| Comparison | R² | Direction | Protein Match |
|------------|-----|-----------|---------------|
| In Vitro | 0.9780 | 100% | 100% (68/68) |
| In Vivo | 0.9998 | 100% | 100% (229/229) |

## Key Genes
- **SCF1** (B9J08_001458→B9J08_03708): Primary adhesin (LFC: 8.61 in vitro)
- **ALS4112** (B9J08_004112→B9J08_04866): Major adhesin (LFC: 5.07 in vitro)
- **IFF4109** (B9J08_004109→B9J08_04863): IFF family adhesin
- **MDR1** (B9J08_003981→B9J08_01838): Drug efflux transporter (LFC: -4.03 in vitro)

## Biological Context
- **AR0382** (aggregative): High biofilm formation, upregulated adhesins (SCF1, ALS4112)
- **AR0387** (non-aggregative): Low biofilm, higher drug efflux activity (MDR1, TPO3)

---
*Reanalysis performed with Galaxy/DESeq2, validated via protein sequence comparison*
