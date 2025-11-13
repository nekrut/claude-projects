# Galaxy Dataset Labeling Session Documentation

## Overview
This document details all steps taken to locate and verify group tags on Galaxy collections #402 and #260 in the PRJNA904261 history.

## Session Date
2025-11-12

## Objectives
1. Locate collection #402 in the Galaxy history and verify that individual datasets are labeled with group tags as specified in `labels.tsv`
2. Apply group tags to collection #260 elements using the same specifications from `labels.tsv`

---

## Prerequisites

### Files in Repository
1. **script.md** - Contains Galaxy connection information and reference links:
   - Galaxy instance: https://usegalaxy.org
   - Galaxy API key: `YOUR_GALAXY_API_KEY`
   - History URL: https://usegalaxy.org/u/cartman/h/prjna904261
   - Reference documentation links for BioBlend, Galaxy API, and GTN tutorial on group tags

2. **labels.tsv** - Mapping of dataset identifiers to group tags:
   ```
   SRR22376030    group:AR0387_A
   SRR22376027    group:AR0382_tnSWI1_B
   SRR22376028    group:AR0382_tnSWI1_A
   SRR22376029    group:AR0387_B
   SRR22376031    group:AR0382_B
   SRR22376032    group:AR0382_A
   ```

### Reference Documentation
- **BioBlend Documentation**: https://bioblend.readthedocs.io/en/latest/
- **Galaxy API Documentation**: https://usegalaxy.org/api/docs
- **GTN Group Tags Tutorial**: https://training.galaxyproject.org/training-material/topics/galaxy-interface/tutorials/group-tags/tutorial.html

---

## Steps Taken

### Step 1: Research and Understanding
**Action**: Reviewed reference documentation to understand:
- How group tags work in Galaxy
- BioBlend API for accessing histories and collections
- Galaxy API endpoints for dataset operations

**Key Findings**:
- Group tags use the format `group:label_name`
- Group tags enable complex analyses without reshaping collections
- Group tags currently do not propagate to derived datasets
- BioBlend provides both object-oriented and client-based APIs

---

### Step 2: Environment Setup
**Action**: Installed BioBlend Python library

**Command**:
```bash
pip install bioblend
```

**Result**: Successfully installed bioblend 1.7.0 and dependencies:
- PyYAML
- requests-toolbelt
- tuspy
- aiohttp and related packages

---

### Step 3: Locate Galaxy History
**Action**: Created `explore_history.py` to connect to Galaxy and find the target history

**Script**: `explore_history.py`
```python
from bioblend.galaxy import GalaxyInstance

GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"

gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)
histories = gi.histories.get_histories()
```

**Result**:
- Found 214 histories in the account
- Located target history: **PRJNA904261**
- History ID: `bbd44e69cb8906b5713a37cc4e6846ea`

---

### Step 4: Locate Collection #402
**Action**: Extended `explore_history.py` to find all collections in the history

**Key Code**:
```python
history_contents = gi.histories.show_history(
    history_id=history_id,
    contents=True
)
collection_items = [
    item for item in history_contents
    if item.get('history_content_type') == 'dataset_collection'
]
```

**Result**:
- Found 50 collections in the history (out of 404 total items)
- **Located Collection #402**:
  - Name: `dataset 261-266 and 395 and collection 260 (Tagged)`
  - Collection ID: `92456119b5c0275e`
  - Type: `list`

---

### Step 5: Inspect Collection Elements
**Action**: Created `inspect_collection.py` to examine the contents of collection #402

**Script**: `inspect_collection.py`
```python
collection_details = gi.histories.show_dataset_collection(
    history_id=HISTORY_ID,
    dataset_collection_id=COLLECTION_ID
)
```

**Result**: Collection #402 contains 6 elements (datasets):

| Element Identifier | Dataset Name | Dataset ID | Current Tags |
|-------------------|--------------|------------|--------------|
| SRR22376030 | Counts Table | f9cad7b01a47213532b48b5103176fdc | group:AR0387_A |
| SRR22376027 | Counts Table | f9cad7b01a47213516625ba610e560f1 | group:AR0382_tnSWI1_B |
| SRR22376028 | Counts Table | f9cad7b01a472135cfc50ea794fb81a9 | group:AR0382_tnSWI1_A |
| SRR22376029 | Counts Table | f9cad7b01a4721353519051e70705d7a | group:AR0387_B |
| SRR22376031 | Counts Table | f9cad7b01a472135fffce6fd8995ceed | group:AR0382_B |
| SRR22376032 | Counts Table | f9cad7b01a472135eef3f87d62b8c2e9 | group:AR0382_A |

---

### Step 6: Verify Tags Match Specifications
**Action**: Created `verify_tags.py` to compare current tags against `labels.tsv`

**Script**: `verify_tags.py`
```python
# Read labels.tsv
label_mapping = {}
with open('labels.tsv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        label_mapping[row[0]] = row[1]

# Compare with collection elements
for element in collection_details['elements']:
    elem_identifier = element['element_identifier']
    current_tags = element['object'].get('tags', [])
    expected_tag = label_mapping.get(elem_identifier)
    # Verify match...
```

**Result**: ✓ **All tags match perfectly!**

| SRR ID | Expected Tag | Current Tag | Status |
|--------|--------------|-------------|--------|
| SRR22376030 | group:AR0387_A | group:AR0387_A | ✓ Match |
| SRR22376027 | group:AR0382_tnSWI1_B | group:AR0382_tnSWI1_B | ✓ Match |
| SRR22376028 | group:AR0382_tnSWI1_A | group:AR0382_tnSWI1_A | ✓ Match |
| SRR22376029 | group:AR0387_B | group:AR0387_B | ✓ Match |
| SRR22376031 | group:AR0382_B | group:AR0382_B | ✓ Match |
| SRR22376032 | group:AR0382_A | group:AR0382_A | ✓ Match |

---

## Part 2: Labeling Collection #260

### Step 7: Locate Collection #260
**Action**: Created `find_collection_260.py` to locate and inspect collection #260

**Script**: `find_collection_260.py`
```python
# Find collection with HID 260
for item in collection_items:
    if item.get('hid') == 260:
        collection_id = item.get('id')
        # Get collection details...
```

**Result**:
- **Located Collection #260**:
  - Name: `Counts Table`
  - Collection ID: `50490a95897034a8`
  - Type: `list`
  - Element Count: 6 datasets
  - **All datasets had NO tags applied**

### Step 8: Apply Group Tags to Collection #260
**Action**: Created `apply_tags_260.py` to apply group tags to all elements in collection #260

**Script**: `apply_tags_260.py`
```python
# Read labels from labels.tsv
label_mapping = {}
with open('labels.tsv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        label_mapping[row[0]] = row[1]

# Apply tags to each element
for element in collection_details['elements']:
    elem_identifier = element['element_identifier']
    dataset_id = element['object']['id']
    expected_tag = label_mapping.get(elem_identifier)

    if expected_tag:
        gi.histories.update_dataset(
            history_id=HISTORY_ID,
            dataset_id=dataset_id,
            tags=[expected_tag]
        )
```

**Result**: Successfully applied tags to all 6 elements:

| Element Identifier | Dataset ID | Tag Applied | Status |
|-------------------|------------|-------------|--------|
| SRR22376030 | f9cad7b01a472135f425c06506130871 | group:AR0387_A | ✓ Success |
| SRR22376027 | f9cad7b01a472135a81260eea3c3f843 | group:AR0382_tnSWI1_B | ✓ Success |
| SRR22376028 | f9cad7b01a472135174bb1a61dc72d1f | group:AR0382_tnSWI1_A | ✓ Success |
| SRR22376029 | f9cad7b01a472135a8419cc06176f6ad | group:AR0387_B | ✓ Success |
| SRR22376031 | f9cad7b01a472135601c5feb34a0919d | group:AR0382_B | ✓ Success |
| SRR22376032 | f9cad7b01a4721359c38b2dbae1c572c | group:AR0382_A | ✓ Success |

### Step 9: Verify Tags on Collection #260
**Action**: Created `verify_tags_260.py` to confirm tags were correctly applied

**Result**: ✓ **All tags verified successfully!**

| SRR ID | Expected Tag | Current Tag | Status |
|--------|--------------|-------------|--------|
| SRR22376030 | group:AR0387_A | group:AR0387_A | ✓ Match |
| SRR22376027 | group:AR0382_tnSWI1_B | group:AR0382_tnSWI1_B | ✓ Match |
| SRR22376028 | group:AR0382_tnSWI1_A | group:AR0382_tnSWI1_A | ✓ Match |
| SRR22376029 | group:AR0387_B | group:AR0387_B | ✓ Match |
| SRR22376031 | group:AR0382_B | group:AR0382_B | ✓ Match |
| SRR22376032 | group:AR0382_A | group:AR0382_A | ✓ Match |

---

## Final Status

### Task Completion - Collection #402
✓ Successfully located collection #402 in Galaxy history PRJNA904261
✓ Retrieved all 6 dataset elements in the collection
✓ Verified all group tags match the specifications in labels.tsv
✓ No tagging action required - tags were already correctly applied

### Task Completion - Collection #260
✓ Successfully located collection #260 in Galaxy history PRJNA904261
✓ Retrieved all 6 dataset elements in the collection
✓ Applied group tags to all 6 elements based on labels.tsv
✓ Verified all tags were correctly applied

### Scripts Created
1. **explore_history.py** - Connects to Galaxy and locates the target history and collections
2. **inspect_collection.py** - Examines collection #402 and displays all elements with their tags
3. **verify_tags.py** - Validates that collection #402 tags match labels.tsv specifications
4. **find_collection_260.py** - Locates and inspects collection #260
5. **apply_tags_260.py** - Applies group tags to collection #260 elements
6. **verify_tags_260.py** - Validates that collection #260 tags were correctly applied

---

## How to Reproduce This Work

### 1. Prerequisites
```bash
pip install bioblend
```

### 2. Set Up Credentials
Ensure you have:
- Galaxy API key
- Galaxy instance URL
- History ID or history name

### 3. Locate Collection
```bash
python explore_history.py
```
This will list all collections in the history and identify collection #402.

### 4. Inspect Collection Details
```bash
python inspect_collection.py
```
This will show all elements in collection #402 with their current tags.

### 5. Verify Tags on Collection #402
```bash
python verify_tags.py
```
This will compare current tags against the specifications in labels.tsv.

### 6. Find and Label Collection #260
```bash
python find_collection_260.py
```
This will locate collection #260 and show its current state.

### 7. Apply Tags to Collection #260
```bash
python apply_tags_260.py
```
This will apply group tags from labels.tsv to all elements in collection #260.

### 8. Verify Tags on Collection #260
```bash
python verify_tags_260.py
```
This will verify that tags were correctly applied to collection #260.

---

## Key Learnings

### Galaxy Group Tags
- Group tags are prefixed with `group:`
- They enable tools like DESeq2 to select datasets by condition
- Elements in a collection are identified by their element_identifier (e.g., SRR22376030)
- Tags are stored as a list in the dataset object

### BioBlend API Usage
- Use `GalaxyInstance` to establish connection
- `get_histories()` retrieves all histories
- `show_history(history_id, contents=True)` gets history contents
- `show_dataset_collection(history_id, dataset_collection_id)` gets collection details
- Collection elements contain `element_identifier` and `object` with dataset details

### History Collection Structure
- A history can contain datasets and collections
- Collections have a `history_content_type` of `dataset_collection`
- Collections are identified by both HID (history item number like #402) and UUID
- Each collection element has type `hda` (History Dataset Association) for regular datasets

---

## API Reference Quick Guide

### Connect to Galaxy
```python
from bioblend.galaxy import GalaxyInstance
gi = GalaxyInstance(url="https://usegalaxy.org", key="YOUR_API_KEY")
```

### List Histories
```python
histories = gi.histories.get_histories()
```

### Get History Contents
```python
contents = gi.histories.show_history(history_id=HISTORY_ID, contents=True)
```

### Filter for Collections
```python
collections = [
    item for item in contents
    if item.get('history_content_type') == 'dataset_collection'
]
```

### Get Collection Details
```python
details = gi.histories.show_dataset_collection(
    history_id=HISTORY_ID,
    dataset_collection_id=COLLECTION_ID
)
```

### Access Element Tags
```python
for element in details['elements']:
    tags = element['object'].get('tags', [])
    element_id = element['element_identifier']
```

### Update Dataset Tags
```python
# Apply or update tags on a specific dataset
gi.histories.update_dataset(
    history_id=HISTORY_ID,
    dataset_id=DATASET_ID,
    tags=['group:label_name']
)
```

---

## Troubleshooting Notes

### Issue 1: Method Parameter Name
**Problem**: `show_dataset_collection()` raised `TypeError` for unexpected keyword `collection_id`

**Solution**: The correct parameter name is `dataset_collection_id`, not `collection_id`

```python
# Incorrect
gi.histories.show_dataset_collection(history_id=ID, collection_id=ID)

# Correct
gi.histories.show_dataset_collection(history_id=ID, dataset_collection_id=ID)
```

---

## Future Use Cases

If you need to **apply or update tags** on datasets in a collection, you would use:

```python
# Update tags on a dataset
gi.histories.update_dataset(
    history_id=HISTORY_ID,
    dataset_id=DATASET_ID,
    tags=['group:new_label']
)
```

Note: This would require iterating through collection elements and updating each dataset individually.

---

## Summary

**Mission**: Locate, verify, and apply group tags on Galaxy collections #402 and #260

**Collection #402 Result**:
- ✓ Success - All 6 datasets already had correct group tags applied
- No modification was necessary

**Collection #260 Result**:
- ✓ Success - Applied group tags to all 6 datasets
- All tags verified to match labels.tsv specifications

**Process**: Efficient workflow using BioBlend API
**Tools**: Python 3.9, BioBlend 1.7.0, Galaxy API

Both collections now have properly applied group tags matching the specifications in `labels.tsv`, enabling tools like DESeq2 to select datasets by experimental conditions.
