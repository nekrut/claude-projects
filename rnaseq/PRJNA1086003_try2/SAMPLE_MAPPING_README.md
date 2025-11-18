# Sample Mapping for PRJNA1086003

## Study Overview

This study investigates *Candida auris* cell surface adhesins crucial for cell-cell interaction and aggregation. The research compares two *C. auris* strains with different phenotypes:

- **AR0382 (B11109)**: Aggregative strain with high biofilm-forming ability
- **AR0387 (B8441)**: Non-aggregative strain with low biofilm-forming ability

## Experimental Design

The study includes **two growth conditions**:

1. **In vitro biofilm**: Biofilms grown in RPMI media in 6-well plates (24h at 37°C)
2. **In vivo catheter**: Biofilms grown on catheters implanted subcutaneously in mice (72h)

## Sample Details

### Total: 13 RNA-seq samples

#### In vitro biofilm samples (6 samples):
- **AR0382** (Aggregative): 3 biological replicates
  - SRR28790270, SRR28790272, SRR28790274
  
- **AR0387** (Non-aggregative): 3 biological replicates
  - SRR28790276, SRR28790278, SRR28790280

#### In vivo catheter samples (7 samples):
- **AR0382** (Aggregative): 3 biological replicates
  - SRR28791430, SRR28791431, SRR28791432
  
- **AR0387** (Non-aggregative): 4 biological replicates
  - SRR28791433, SRR28791434, SRR28791437, SRR28791438

## Key Findings

The study identified **SCF1** and **ALS4112** as highly upregulated adhesin genes in the aggregative strain (AR0382) during both in vitro and in vivo biofilm growth:

- **SCF1** (B9J08_001458): 
  - In vitro LFC: 8.61 (FDR: 4.78e-29)
  - In vivo LFC: 4.47 (FDR: 7.10e-26)
  
- **ALS4112** (B9J08_004112):
  - In vitro LFC: 5.07 (FDR: 3.81e-24)
  - In vivo LFC: 2.56 (FDR: 1.84e-06)

## Recommended Comparisons for DESeq2

1. **Aggregative vs Non-aggregative (In vitro)**
   - AR0382_invitro vs AR0387_invitro
   
2. **Aggregative vs Non-aggregative (In vivo)**
   - AR0382_invivo vs AR0387_invivo
   
3. **In vivo vs In vitro (Aggregative)**
   - AR0382_invivo vs AR0382_invitro
   
4. **In vivo vs In vitro (Non-aggregative)**
   - AR0387_invivo vs AR0387_invitro

## Files Created

- `sample_mapping.tsv`: Detailed mapping with all metadata
- `sample_info_deseq2.csv`: Simplified format ready for DESeq2 analysis
- `SraRunInfo.csv`: Original SRA metadata from NCBI

## Reference

Wang TW, et al. (2024) Functional redundancy in Candida auris cell surface adhesins crucial for cell-cell interaction and aggregation. Nature Communications 15:9212.
https://doi.org/10.1038/s41467-024-53588-5
