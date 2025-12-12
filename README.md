# claude-projects

Projects using Claude AI for bioinformatics and data analysis.

## Projects

### rnaseq/
RNA-seq reanalysis validation for *Candida auris* studies. Reanalyzed published datasets using Galaxy/DESeq2 and validated results against original publications.

**Key finding**: Claude's "clever" LFC-based gene mapping achieved R²=0.9996 but was 99% wrong. Correct mapping via NCBI `old_locus_tag` + protein sequence validation.

Studies validated:
- **Santana et al. (2024)** - SCF1 adhesin characterization (R²=0.94)
- **Wang et al. (2024)** - Glycan-lectin interactions (R²=0.98-0.9998)

Structure:
```
rnaseq/
├── santana24_PRJNA904261/     # Santana study (validated)
├── wang24_PRJNA1086003/       # Wang study (validated)
├── shared_reference/          # C. auris B8441 GTF/FASTA (v2, v3)
├── deseq2_validation/         # Validation notebooks
├── blog/                      # Blog: "AI Can Make Mistakes"
└── Cauris_rna_seq_survey/     # Literature survey (32 studies)
```

### create-new-history-doc/
Galaxy history creation documentation.

### dataset_labelling/
Dataset labelling tools and utilities.
