# Plan: Split Galaxy Collection #244 by Experimental Conditions

## Summary of Findings

### SRA Metadata (PRJNA904261) - 6 RNA-seq runs:

| Run Accession | Library Name | Condition | Replicate |
|--------------|--------------|-----------|-----------|
| SRR22376031 | AR0382_B | AR0382 WT | B |
| SRR22376032 | AR0382_A | AR0382 WT | A |
| SRR22376027 | AR0382_tnSWI1_B | tnSWI1 mutant | B |
| SRR22376028 | AR0382_tnSWI1_A | tnSWI1 mutant | A |
| SRR22376029 | AR0387_B | AR0387 WT | B |
| SRR22376030 | AR0387_A | AR0387 WT | A |

### Experimental Context (from Santana et al. 2023):

**3 Conditions:**
1. **AR0382** - Clade I, highly adhesive reference strain
2. **AR0387** - Clade I, poorly adhesive (206 coding SNPs from AR0382)
3. **AR0382_tnSWI1** - SWI1 insertional mutant (low adhesion, SCF1 downregulated)

**Comparisons in paper:**
- Fig 1D: tnSWI1 vs AR0382 → discovered SCF1
- Fig S5A: AR0387 vs AR0382 → confirmed SCF1 dysregulation

## Implementation Plan

**User preferences:**
- Output: 3 separate collections (one per condition)
- Identifiers: SRR accessions

### Step 1: Create identifier lists for each condition

**AR0382_WT.txt:**
```
SRR22376031
SRR22376032
```

**AR0387_WT.txt:**
```
SRR22376029
SRR22376030
```

**tnSWI1.txt:**
```
SRR22376027
SRR22376028
```

### Step 2: Upload identifier files to Galaxy history

Use Galaxy upload API to add the 3 text files to the history.

### Step 3: Filter collection using `__FILTER_FROM_FILE__`

For each condition, run:
```python
POST /api/tools
{
    "tool_id": "__FILTER_FROM_FILE__",
    "history_id": "<history_id>",
    "inputs": {
        "input": {"src": "hdca", "id": "<collection_244_id>"},
        "how": {
            "how_filter": "remove_if_absent",
            "filter_source": {"src": "hda", "id": "<identifier_file_id>"}
        }
    }
}
```

### Step 4: Rename output collections

Rename to descriptive names:
- `counts_AR0382_WT`
- `counts_AR0387_WT`
- `counts_tnSWI1`

## Mapping Summary

| SRR Accession | Condition | Replicate |
|--------------|-----------|-----------|
| SRR22376031 | AR0382_WT | B |
| SRR22376032 | AR0382_WT | A |
| SRR22376029 | AR0387_WT | B |
| SRR22376030 | AR0387_WT | A |
| SRR22376027 | tnSWI1 | B |
| SRR22376028 | tnSWI1 | A |
