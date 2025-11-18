# PRJNA904261 Sample Information and Grouping

## Summary
This RNA-seq experiment studies *Candida auris* with 6 samples across 3 experimental conditions, comparing wild-type strains to a SWI1 knockout mutant.

## Experimental Conditions

### Condition 1: AR0387 (Strain TO38) - Wild Type from Blood
- **Description**: Wild-type strain isolated from blood
- **Collection Date**: 2008
- **Location**: Pakistan
- **Samples**:
  - `SRR22376030` → AR0387_A (Biological replicate A)
  - `SRR22376029` → AR0387_B (Biological replicate B)

### Condition 2: AR0382 (Strain TO33) - Wild Type from Burn Wound
- **Description**: Wild-type strain isolated from burn wound
- **Collection Date**: 2019-04-18
- **Location**: Pakistan
- **Samples**:
  - `SRR22376032` → AR0382_A (Biological replicate A)
  - `SRR22376031` → AR0382_B (Biological replicate B)

### Condition 3: AR0382 tnSWI1 (Strain TO219) - SWI1 Knockout Mutant
- **Description**: SWI1 transposon knockout mutant derived from AR0382
- **Parent Strain**: AR0382 (TO33)
- **Samples**:
  - `SRR22376028` → AR0382_tnSWI1_A (Biological replicate A)
  - `SRR22376027` → AR0382_tnSWI1_B (Biological replicate B)

## Galaxy Collections

### Current Structure
- **Collection #260**: "Counts Table" - Contains all 6 samples in a single list collection
  - Elements ordered by SRR number (not grouped by condition)

### Recommended Reorganization for DESeq2

For differential expression analysis, you should create separate collections for each condition:

#### Collection 1: AR0387_blood_WT
- SRR22376030 (AR0387_A)
- SRR22376029 (AR0387_B)

#### Collection 2: AR0382_burn_WT
- SRR22376032 (AR0382_A)
- SRR22376031 (AR0382_B)

#### Collection 3: AR0382_tnSWI1_KO
- SRR22376028 (AR0382_tnSWI1_A)
- SRR22376027 (AR0382_tnSWI1_B)

## Possible Comparisons for Differential Expression

1. **SWI1 Knockout vs Wild Type (Burn Wound Background)**
   - Compare: AR0382_tnSWI1_KO vs AR0382_burn_WT
   - Purpose: Identify genes affected by SWI1 knockout

2. **Blood vs Burn Wound (Both Wild Type)**
   - Compare: AR0387_blood_WT vs AR0382_burn_WT
   - Purpose: Identify strain/source-specific differences

3. **SWI1 Knockout vs Blood Wild Type**
   - Compare: AR0382_tnSWI1_KO vs AR0387_blood_WT
   - Purpose: Broader comparison of mutant to wild-type

## Galaxy Workflow Steps

To reorganize collection #260 for DESeq2 analysis:

1. Use "Extract Dataset" or "Filter Collection" tools to create 3 new collections
2. Use "Apply Rule to Collection" with the following grouping rules:
   - Group by strain/condition based on identifier patterns
   - Create nested list structure if needed for DESeq2

3. Alternative: Use Galaxy's tagging system:
   - Tag samples with condition names
   - Use "Filter by tags" to create condition-specific collections

## Notes
- All samples are paired-end RNA-seq (NextSeq 2000)
- Library prep: Random primed, Transcriptomic source
- This appears to be part of a larger study investigating SWI1 gene function in *C. auris*
