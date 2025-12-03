# Collection Filtering Log

## Objective

Create 4 filtered collections from Galaxy collection #407 (Counts Table) based on experimental conditions:
1. in_vitro AR0382 (3 samples)
2. in_vitro AR0387 (3 samples)
3. in_vivo AR0382 (3 samples)
4. in_vivo AR0387 (4 samples)

## Source Data

- **Galaxy History:** PRJNA1086003 Final (`bbd44e69cb8906b59f131af7b542c1b1`)
- **Source Collection:** #407 "Counts Table" (`4de1b65e3e854e25`) - 13 tabular files

## Sample Mapping

Obtained from NCBI SRA metadata for PRJNA1086003:

| SRR ID | Sample Name | Strain | Condition |
|--------|-------------|--------|-----------|
| SRR28790270 | 82_Bio_1 | AR0382 | in_vitro |
| SRR28790272 | 82_Bio_2 | AR0382 | in_vitro |
| SRR28790274 | 82_Bio_3 | AR0382 | in_vitro |
| SRR28790276 | 87_Bio_1 | AR0387 | in_vitro |
| SRR28790278 | 87_Bio_2 | AR0387 | in_vitro |
| SRR28790280 | 87_Bio_3 | AR0387 | in_vitro |
| SRR28791430 | 82_RNA_inVivo_blueink | AR0382 | in_vivo |
| SRR28791431 | RNA_invivo_82_blackink | AR0382 | in_vivo |
| SRR28791432 | 82 | AR0382 | in_vivo |
| SRR28791433 | 87-1 | AR0387 | in_vivo |
| SRR28791434 | 87-2 | AR0387 | in_vivo |
| SRR28791437 | 87-3 | AR0387 | in_vivo |
| SRR28791438 | RNA_invivo_87 | AR0387 | in_vivo |

**Note:** The ANALYSIS_REPORT.md had incorrect SRR IDs (SRR28102xxx) - actual IDs are SRR2879xxxx.

## Method

Used Galaxy's `__FILTER_FROM_FILE__` tool for reproducible filtering.

### Step 1: Upload Identifier Files

Created 4 text files with SRR IDs (one per line) and uploaded via Galaxy API:

```bash
curl -X POST "https://usegalaxy.org/api/tools" \
  -H "x-api-key: $GALAXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "upload1",
    "history_id": "bbd44e69cb8906b59f131af7b542c1b1",
    "inputs": {
      "file_type": "txt",
      "files_0|url_paste": "SRR28790270\nSRR28790272\nSRR28790274",
      "files_0|type": "upload_dataset",
      "files_0|NAME": "identifiers_invitro_AR0382"
    }
  }'
```

Uploaded files:
- HID 692: `identifiers_invitro_AR0382` (`f9cad7b01a4721353d584744305a1699`)
- HID 693: `identifiers_invitro_AR0387` (`f9cad7b01a472135c221d98b580ef552`)
- HID 694: `identifiers_invivo_AR0382` (`f9cad7b01a4721350aa26ea75d7ab59b`)
- HID 695: `identifiers_invivo_AR0387` (`f9cad7b01a47213571e6f90064463208`)

### Step 2: Filter Collection

Used `__FILTER_FROM_FILE__` with `remove_if_absent` mode:

```bash
curl -X POST "https://usegalaxy.org/api/tools" \
  -H "x-api-key: $GALAXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool_id": "__FILTER_FROM_FILE__",
    "history_id": "bbd44e69cb8906b59f131af7b542c1b1",
    "inputs": {
      "input": {"values": [{"id": "4de1b65e3e854e25", "src": "hdca"}]},
      "how|how_filter": "remove_if_absent",
      "how|filter_source": {"values": [{"id": "IDENTIFIER_FILE_ID", "src": "hda"}]}
    }
  }'
```

### Step 3: Rename Collections

Used PUT request to rename filtered collections:

```bash
curl -X PUT "https://usegalaxy.org/api/histories/HISTORY_ID/contents/dataset_collections/COLLECTION_ID" \
  -H "x-api-key: $GALAXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "in_vitro AR0382"}'
```

## Results

| HID | Name | Collection ID | Elements |
|-----|------|---------------|----------|
| #759 | in_vitro AR0382 | b5995868b58569b3 | SRR28790270, SRR28790272, SRR28790274 |
| #774 | in_vitro AR0387 | ebc1fcb59fab4fa3 | SRR28790276, SRR28790278, SRR28790280 |
| #789 | in_vivo AR0382 | 845448de811b347f | SRR28791430, SRR28791431, SRR28791432 |
| #805 | in_vivo AR0387 | 172a5d8047423854 | SRR28791433, SRR28791434, SRR28791437, SRR28791438 |

## Problems Encountered

### 1. API Access Issues

Initial attempts to access the Galaxy history URL directly via WebFetch failed - Galaxy requires JavaScript to render content.

**Solution:** Used Galaxy REST API with `GALAXY_API_KEY` environment variable.

### 2. Empty History List

First API call to `/api/histories` returned empty array despite valid API key.

**Cause:** Query parameters weren't finding the history.

**Solution:** Used `/api/histories?slug=prjna1086003-final` to find the correct history ID.

### 3. Incorrect Tool Input Format (First Attempt)

Initial filter tool invocations used wrong input structure:
```json
{
  "input": {"src": "hdca", "id": "..."},
  "how": {
    "how_filter": "remove_if_absent",
    "filter_source": {"src": "hda", "id": "..."}
  }
}
```

This caused jobs to complete but produce empty collections - the tool used default inputs instead of specified ones.

**Solution:** Used correct Galaxy tool input format with `values` array:
```json
{
  "input": {"values": [{"id": "...", "src": "hdca"}]},
  "how|how_filter": "remove_if_absent",
  "how|filter_source": {"values": [{"id": "...", "src": "hda"}]}
}
```

### 4. Finding Output Collections

Tool `/api/jobs/JOB_ID/outputs` returned empty array for collection operations.

**Solution:** Used `/api/jobs/JOB_ID?full=true` which includes `output_collections` field with the created collection IDs.

### 5. Python F-string Escaping in Bash

Complex f-strings with quotes caused syntax errors when embedded in bash heredocs.

**Solution:** Used simpler print statements or wrote Python to temp files.

## Reproducibility

All operations used Galaxy's native tools:
- `upload1` for identifier files
- `__FILTER_FROM_FILE__` for collection filtering

This ensures:
- All steps captured in Galaxy history
- Can be extracted to a reusable workflow
- Fully reproducible by anyone with access to the history
