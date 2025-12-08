# Santana et al. 2024 RNA-seq Reproduction

Reproduction of *C. auris* SCF1 adhesin study (PRJNA904261).

## Study Overview

**Publication**: Santana et al. 2024 - SCF1 as primary regulatory target of SWI1 chromatin remodeling complex

**Key finding**: SCF1 most strongly downregulated gene in SWI1 knockout

## Samples

| SRA Accession | Strain | Description | Condition |
|---------------|--------|-------------|-----------|
| SRR22376031 | AR0382 | Burn wound isolate | WT high-adhesion |
| SRR22376032 | AR0382 | Burn wound isolate | WT high-adhesion |
| SRR22376029 | AR0387 | Blood isolate | WT low-adhesion |
| SRR22376030 | AR0387 | Blood isolate | WT low-adhesion |
| SRR22376027 | AR0382_tnSWI1 | SWI1 knockout | Mutant |
| SRR22376028 | AR0382_tnSWI1 | SWI1 knockout | Mutant |

## Workflow

### Phase 1: Galaxy Analysis
See [01_galaxy_setup.md](01_galaxy_setup.md)
1. Filter featureCounts collection into 3 strain-specific collections
2. Run DESeq2 for two comparisons:
   - AR0382 vs tnSWI1 (Figure 1D)
   - AR0382 vs AR0387 (Figure S5A)

### Phase 2: Validation
See [02_validation.md](02_validation.md)
1. Download DESeq2 results
2. Extract publication DEGs from Excel supplement
3. Run LFC-based gene mapping (handles v2→v3 ID mismatch)
4. Generate validation plots

## Expected Results

| Comparison | R² | Direction Match |
|------------|-----|-----------------|
| AR0382 vs tnSWI1 | >0.99 | 100% |
| AR0382 vs AR0387 | >0.98 | 100% |

SCF1 (B9J08_03708) confirmed as most downregulated gene in both comparisons.

## Critical Note: Gene ID Versions

Publication uses v2 annotation (6-digit: B9J08_001458)
Our analysis uses v3 annotation (5-digit: B9J08_03708)

LFC-based correlation mapping resolves this mismatch.
