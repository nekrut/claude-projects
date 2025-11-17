# DESeq2 Differential Expression Analysis
## Replicating the Analysis from Wang et al. 2024

### Paper Reference
**Title:** "Functional redundancy in Candida auris cell surface adhesins crucial for cell-cell interaction and aggregation"
**Journal:** Nature Communications (2024) 15:9212
**DOI:** https://doi.org/10.1038/s41467-024-53588-5

### Study Design

The paper describes two experiments comparing gene expression between:
- **AR0382** (B11109): Aggregative, high biofilm-forming strain
- **AR0387** (B8441): Non-aggregative, low biofilm-forming strain

#### Experiment 1: In Vitro Biofilm Formation
- **Growth conditions:** 6-well plates in RPMI 1640-HEPES media, 37°C for 24h
- **Samples:** 3 biological replicates per strain (6 total)
- **AR0382 samples:** SRR28790270, SRR28790272, SRR28790274
- **AR0387 samples:** SRR28790276, SRR28790278, SRR28790280
- **Expected DEGs:** ~76 genes (LFC ≥ |1|, FDR < 0.01)

#### Experiment 2: In Vivo Catheter Infection
- **Growth conditions:** Catheters implanted subcutaneously in mice, 37°C for 72h
- **Samples:** 3 AR0382 + 4 AR0387 replicates (7 total)
- **AR0382 samples:** SRR28791430, SRR28791431, SRR28791432
- **AR0387 samples:** SRR28791433, SRR28791434, SRR28791437, SRR28791438
- **Expected DEGs:** ~259 genes (LFC ≥ |1|, FDR < 0.01)

### Analysis Pipeline

#### Step 1: Sample Organization
1. Split original counts table (#601) into two collections:
   - In vitro collection (#621): 6 samples
   - In vivo collection (#629): 7 samples

2. Added group tags to all datasets for easy identification:
   - Format: `group:` + sample name
   - Example: `group:82_Bio_1`, `group:87-1`

#### Step 2: Create Strain-Specific Sub-Collections
For DESeq2 to work properly with collections, samples were organized into strain-specific sub-collections:

**In vitro:**
- Collection #641: PRJNA1086003_in_vitro_AR0382 (3 samples)
- Collection #645: PRJNA1086003_in_vitro_AR0387 (3 samples)

**In vivo:**
- Collection #651: PRJNA1086003_in_vivo_AR0382 (3 samples)
- Collection #656: PRJNA1086003_in_vivo_AR0387 (4 samples)

#### Step 3: Run DESeq2 with Separate Collections (CORRECT METHOD)

**Tool:** DESeq2 v2.11.40.8+galaxy0

**Key Concept:** Feed each strain's samples as a separate collection to DESeq2

**In vitro experiment:**
- Factor name: strain
- Factor level "87" (AR0387): Collection #645 - PRJNA1086003_in_vitro_AR0387
- Factor level "82" (AR0382): Collection #641 - PRJNA1086003_in_vitro_AR0382

**In vivo experiment:**
- Factor name: strain
- Factor level "87" (AR0387): Collection #656 - PRJNA1086003_in_vivo_AR0387
- Factor level "82" (AR0382): Collection #651 - PRJNA1086003_in_vivo_AR0382

**Parameters:**
- FDR threshold (alpha): 0.01
- LFC threshold: 0 (filter for |LFC| ≥ 1 in post-processing)
- Beta priors: False
- Outputs: Result file + diagnostic plots

### Results Location

Results are available in the Galaxy history:
https://usegalaxy.org/u/cartman/h/prjna1086003

**In vitro results:** DESeq2 outputs from latest run
**In vivo results:** DESeq2 outputs from latest run

### Key Findings from Paper

The paper identified the following key upregulated genes in AR0382:
- **SCF1** (B9J08_001458): Cell surface adhesin with Flo11 domain
- **ALS4112** (B9J08_004112): Als-family adhesin
- **IFF4109** (B9J08_004109): IFF/HYR1 family adhesin
- Several other IFF/HYR1 family members

These adhesins were shown to have complementary and redundant roles in:
- Cell-cell adherence
- Aggregation
- Biofilm formation

### Scripts Used

1. **split_collection.py**: Split original collection into in vitro and in vivo
2. **add_tags_to_collections.py**: Added group tags to datasets
3. **run_deseq2_with_tags.py**: Created sub-collections and ran DESeq2 analyses

### Analysis Parameters Match Paper

| Parameter | Paper | Our Analysis |
|-----------|-------|--------------|
| Statistical method | DESeq2 | DESeq2 |
| LFC threshold | ≥ \|1\| | ≥ \|1\| (post-filter) |
| FDR threshold | < 0.01 | < 0.01 |
| Comparison | AR0382 vs AR0387 | AR0382 vs AR0387 |
| In vitro replicates | 3 vs 3 | 3 vs 3 |
| In vivo replicates | 3 vs 4 | 3 vs 4 |

### Next Steps

1. Wait for DESeq2 jobs to complete in Galaxy
2. Download result files
3. Filter for genes with |LFC| ≥ 1 and FDR < 0.01
4. Compare with Supplementary Data 1 (in vitro) and Supplementary Data 2 (in vivo) from paper
5. Verify that key adhesin genes (SCF1, ALS4112, etc.) are among top upregulated genes
