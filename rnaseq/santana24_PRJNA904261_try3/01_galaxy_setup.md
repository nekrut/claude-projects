# Phase 1: Galaxy Collection Setup & DESeq2

## Prerequisites

Galaxy history `prjna904261-final` contains:
- HID #211: featureCounts master counts table (6 samples)
- HID #15: C. auris B8441 GTF annotation (GCA_002759435.3)

History URL: https://usegalaxy.org/u/cartman/h/prjna904261-final

## Step 1: Upload Identifier Files

Upload files from `identifier_files/` to Galaxy:
- `ar0382.txt` - AR0382 wild-type samples
- `ar0387.txt` - AR0387 wild-type samples
- `tnswi1.txt` - SWI1 knockout samples

**Upload method**: Get Data > Upload File

## Step 2: Filter Collections

Use tool: **Filter collection** (`__FILTER_FROM_FILE__`)

### Create AR0382 collection

| Parameter | Value |
|-----------|-------|
| Input collection | #211 (featureCounts output) |
| Filter mode | Keep if identifier in file |
| Identifier file | ar0382.txt |

Output: 2-element collection (SRR22376031, SRR22376032)

### Create AR0387 collection

| Parameter | Value |
|-----------|-------|
| Input collection | #211 |
| Filter mode | Keep if identifier in file |
| Identifier file | ar0387.txt |

Output: 2-element collection (SRR22376029, SRR22376030)

### Create tnSWI1 collection

| Parameter | Value |
|-----------|-------|
| Input collection | #211 |
| Filter mode | Keep if identifier in file |
| Identifier file | tnswi1.txt |

Output: 2-element collection (SRR22376027, SRR22376028)

## Step 3: Run DESeq2

Use tool: **DESeq2** (iuc)

### Comparison 1: AR0382 vs tnSWI1 (replicates Figure 1D)

| Parameter | Value |
|-----------|-------|
| Factor name | genotype |
| Factor level 1 name | WT |
| Factor level 1 counts | AR0382 collection |
| Factor level 2 name | mutant |
| Factor level 2 counts | tnSWI1 collection |
| Output normalized counts | No |
| Output all results | Yes |

### Comparison 2: AR0382 vs AR0387 (replicates Figure S5A)

| Parameter | Value |
|-----------|-------|
| Factor name | strain |
| Factor level 1 name | AR0382 |
| Factor level 1 counts | AR0382 collection |
| Factor level 2 name | AR0387 |
| Factor level 2 counts | AR0387 collection |
| Output normalized counts | No |
| Output all results | Yes |

## Step 4: Download Results

Download DESeq2 result tables as TSV:
- `deseq2_tnSWI1.tsv` - comparison 1
- `deseq2_AR0387.tsv` - comparison 2

Place in `analysis/` directory for validation.

## DESeq2 Output Format

Headerless TSV with columns:
```
GeneID  baseMean  log2FoldChange  lfcSE  stat  pvalue  padj
```

**Note**: DESeq2 reference level affects LFC sign. The validation script auto-detects direction.
