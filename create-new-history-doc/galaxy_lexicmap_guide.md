# Galaxy History Import and LexicMap Tool Usage Guide

## Table of Contents
1. [Quick Start Guide](#quick-start-guide)
2. [Detailed Instructions - Web Interface](#detailed-instructions---web-interface)
3. [Programmatic Access with BioBlend](#programmatic-access-with-bioblend)
4. [Understanding LexicMap](#understanding-lexicmap)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start Guide

### Prerequisites
- A Galaxy account at https://test.galaxyproject.org/
- Internet browser (Chrome, Firefox, Safari, or Edge)

### 5-Minute Workflow

1. **Create an account** at https://test.galaxyproject.org/
2. **Import the test history**: https://test.galaxyproject.org/u/anton/h/test-history
3. **Open LexicMap Search tool**: https://test.galaxyproject.org/?tool_id=toolshed.g2.bx.psu.edu%2Frepos%2Fiuc%2Flexicmap%2Flexicmap_search%2F0.8.0%2Bgalaxy0&version=latest
4. **Select "locally installed indices"** and check as many indices as possible
5. **Use datasets #1 and #2** as test data or upload your own data
6. **Execute** and wait for results

---

## Detailed Instructions - Web Interface

### Step 1: Create a Galaxy Account

1. Navigate to https://test.galaxyproject.org/
2. Click **"Login or Register"** in the top menu
3. Select **"Register"**
4. Fill in:
   - Email address
   - Password
   - Public name (username)
5. Click **"Create"**
6. Check your email for verification (if required)

### Step 2: Import a Shared History

#### Method A: Import from Shared Link (Recommended)

1. Click on the test history link: https://test.galaxyproject.org/u/anton/h/test-history
2. This opens the shared history view
3. Click the **"+"** (plus) icon or **"Import history"** button in the top right
4. The history will be copied to your account
5. Click **"View history"** to see the imported datasets

#### Method B: Import History from URL

1. In the Galaxy interface, click **"User"** → **"Histories"** in the top menu
2. Click **"Import from File"** button
3. Paste the URL of a history archive (.tar.gz file)
4. Click **"Submit"**
5. Wait for the import to complete (you'll see a progress bar)

#### Method C: Create New History and Upload Data

1. Click the **"+"** icon at the top of the History panel (right side)
2. Select **"Create new history"**
3. Name your history (e.g., "My LexicMap Analysis")
4. Click **"Upload Data"** button in the tools panel
5. Choose files from:
   - **Your computer** (drag and drop or browse)
   - **URL** (paste a direct link to a FASTA file)
   - **FTP** (if you've uploaded large files via FTP)

**Supported file formats for LexicMap:**
- FASTA (.fasta, .fa, .fna)
- Compressed FASTA (.fasta.gz, .fa.gz)
- Minimum sequence length: >150 bp recommended

### Step 3: Navigate to LexicMap Search Tool

#### Direct Link
Click this link: https://test.galaxyproject.org/?tool_id=toolshed.g2.bx.psu.edu%2Frepos%2Fiuc%2Flexicmap%2Flexicmap_search%2F0.8.0%2Bgalaxy0&version=latest

#### Via Tool Panel
1. In the left **Tools** panel, use the search box
2. Type **"lexicmap"** or **"sequence alignment"**
3. Click on **"LexicMap Search"** when it appears
4. The tool form will load in the center panel

### Step 4: Configure LexicMap Search Parameters

#### Basic Configuration

1. **Input sequences** (Query sequences):
   - Select your FASTA file from the dropdown
   - This should be dataset #1, #2, or your uploaded file
   - These are the sequences you want to search

2. **Reference genome database**:
   - Select **"locally installed indices"**
   - Check as many indices as possible for comprehensive search
   - Available indices may include:
     - GTDB (Genome Taxonomy Database)
     - RefSeq prokaryotes
     - GenBank prokaryotes
     - Custom genome collections

3. **Output format**:
   - Default: Tabular (TSV) format
   - Includes all alignment statistics

#### Advanced Parameters (Optional)

**Alignment Quality Thresholds:**
- **Minimum percent identity** (default: 80%)
  - Lower for divergent sequences (e.g., 70%)
  - Higher for strict matches (e.g., 90%)

- **Minimum query coverage per genome** (default: 70%)
  - Percentage of query that must align
  - Lower for partial matches (e.g., 50%)

- **Minimum query coverage per HSP** (default: 70%)
  - Coverage per high-scoring pair
  - Set to 0 for plasmid searches

- **Maximum number of target genomes** (default: 10000)
  - Limit results to top N genomes
  - Reduce for faster processing

**Alignment Parameters:**
- **Minimum match length** (default: varies by query type)
  - For genes: 100-500 bp
  - For plasmids: 1000+ bp

- **Maximum mismatch**: Control sensitivity
- **Gap penalties**: Adjust alignment scoring

### Step 5: Execute the Analysis

1. Review your parameter selections
2. Click the blue **"Execute"** button at the bottom of the form
3. The tool will appear in your history (right panel) with:
   - Gray/waiting: Job queued
   - Yellow/running: Job executing
   - Green/done: Job completed successfully
   - Red/error: Job failed (check error message)

**Estimated run times:**
- Single gene vs 1M genomes: ~30 seconds - 5 minutes
- Multiple genes: 5-15 minutes
- Large plasmids: 10-30 minutes

### Step 6: View and Interpret Results

#### View Results

1. Once the job turns green, click the **eye icon** to view
2. Results display in the center panel as a table
3. Click the **download icon** to save locally
4. Click the **info icon** for job details

#### Understanding the Output Columns

| Column | Meaning | What to Look For |
|--------|---------|------------------|
| **query** | Your query sequence ID | Identifies which input sequence |
| **qlen** | Query length (bp) | Reference for coverage calculations |
| **hits** | Number of hits found | More hits = more widespread |
| **sgenome** | Subject genome ID | The genome with a match |
| **sseqid** | Subject sequence ID | Specific contig/chromosome |
| **qcovGnm** | Query coverage (genome-wide) | >70% = good match |
| **pident** | Percent identity | >80% = strong similarity |
| **qstart, qend** | Query alignment region | Which part of query aligned |
| **sstart, send** | Subject alignment region | Location in reference genome |
| **evalue** | Statistical significance | Lower = more significant |
| **bitscore** | Alignment quality score | Higher = better alignment |

#### Interpreting Results

**High-quality matches:**
- pident > 90%
- qcovGnm > 80%
- evalue < 1e-50

**Moderate matches:**
- pident 70-90%
- qcovGnm 50-80%
- evalue < 1e-10

**Low-quality/distant matches:**
- pident < 70%
- qcovGnm < 50%
- Consider biological significance

### Step 7: Download or Share Results

#### Download Results
1. Click the **disk icon** (download) next to the result dataset
2. Choose format (usually TSV/tabular)
3. Save to your computer

#### Share Your History
1. Click **"History options"** (gear icon) in history panel
2. Select **"Share or Publish"**
3. Choose:
   - **"Make accessible via link"**: Anyone with URL can view
   - **"Publish"**: Publicly listed
   - **"Share with user"**: Share with specific Galaxy users

#### Export History
1. Click **"History options"** → **"Export History to File"**
2. Wait for export to complete
3. Download the .tar.gz archive
4. Import later or share the file

---

## Programmatic Access with BioBlend

For automation, scripting, and batch processing, use BioBlend (Python library).

### Installation

```bash
pip install bioblend
```

### Basic Setup

```python
from bioblend.galaxy import GalaxyInstance

# Connect to Galaxy
gi = GalaxyInstance(
    url='https://test.galaxyproject.org',
    key='YOUR_API_KEY'  # Get from User > Preferences > Manage API Key
)

# Test connection
print(gi.config.get_config())
```

### Get Your API Key

1. Log into https://test.galaxyproject.org
2. Click **"User"** → **"Preferences"**
3. Click **"Manage API Key"**
4. Click **"Create a new key"** (if no key exists)
5. Copy the key and keep it secure

### Import History via API

#### Import from URL

```python
# Import history from an exported archive URL
import_result = gi.histories.import_history(
    url='https://example.com/path/to/history.tar.gz'
)

print(f"Importing history: {import_result}")
# Returns job information - check status periodically
```

#### Import from Local File

```python
# Import from downloaded archive
import_result = gi.histories.import_history(
    file_path='/path/to/local/history_archive.tar.gz'
)
```

#### Copy Shared History

```python
# List public histories
published = gi.histories.get_published_histories()
for hist in published[:5]:
    print(f"{hist['name']}: {hist['id']}")

# Import a specific published history
imported = gi.histories.import_history(
    history_id='SHARED_HISTORY_ID'
)
```

### Create and Manage Histories

```python
# Create new history
new_history = gi.histories.create_history(
    name='API LexicMap Analysis'
)
history_id = new_history['id']
print(f"Created history: {history_id}")

# List all your histories
histories = gi.histories.get_histories()
for h in histories:
    print(f"History: {h['name']} (ID: {h['id']})")

# View specific history
history_details = gi.histories.show_history(
    history_id=history_id,
    contents=True  # Include datasets
)

# Show datasets in history
datasets = gi.histories.show_matching_datasets(
    history_id=history_id
)
for ds in datasets:
    print(f"Dataset: {ds['name']} ({ds['state']})")
```

### Upload Data to History

```python
# Upload local file
upload_result = gi.tools.upload_file(
    path='my_sequences.fasta',
    history_id=history_id,
    file_type='fasta'
)
dataset_id = upload_result['outputs'][0]['id']
print(f"Uploaded dataset ID: {dataset_id}")

# Upload from URL
upload_result = gi.tools.upload_from_ftp(
    path='https://example.com/data.fasta',
    history_id=history_id
)

# Upload large files via FTP
# First upload to FTP, then:
upload_result = gi.tools.upload_from_ftp(
    path='large_dataset.fasta',
    history_id=history_id
)
```

### Run LexicMap via API

```python
# Find LexicMap tool
tools = gi.tools.get_tools()
lexicmap_tools = [t for t in tools if 'lexicmap' in t['name'].lower()]
print(f"Found tools: {lexicmap_tools}")

# Get tool ID
tool_id = 'toolshed.g2.bx.psu.edu/repos/iuc/lexicmap/lexicmap_search/0.8.0+galaxy0'

# Show tool details
tool_info = gi.tools.show_tool(tool_id=tool_id)

# Run LexicMap search
inputs = {
    'query': {'src': 'hda', 'id': dataset_id},  # Input dataset
    'reference': 'locally_cached',  # Use local indices
    'align_min_match_pident': 80,
    'min_qcov_per_genome': 70,
    'top_n_genomes': 10000
}

job_result = gi.tools.run_tool(
    history_id=history_id,
    tool_id=tool_id,
    tool_inputs=inputs
)

print(f"Job submitted: {job_result}")
output_dataset_id = job_result['outputs'][0]['id']
```

### Monitor Job Status

```python
import time

def wait_for_dataset(gi, dataset_id, timeout=3600, interval=10):
    """Wait for dataset to complete"""
    elapsed = 0
    while elapsed < timeout:
        dataset = gi.datasets.show_dataset(dataset_id)
        state = dataset['state']

        print(f"Status: {state}")

        if state == 'ok':
            print("Job completed successfully!")
            return True
        elif state == 'error':
            print("Job failed!")
            return False

        time.sleep(interval)
        elapsed += interval

    print("Timeout reached")
    return False

# Use it
success = wait_for_dataset(gi, output_dataset_id)
```

### Download Results

```python
# Download dataset
gi.datasets.download_dataset(
    dataset_id=output_dataset_id,
    file_path='./lexicmap_results.tsv',
    use_default_filename=False
)

print("Results downloaded!")

# Read and process results
import pandas as pd
df = pd.read_csv('lexicmap_results.tsv', sep='\t')
print(f"Found {len(df)} alignments")
print(df.head())
```

### Export History

```python
# Export history
export_result = gi.histories.export_history(
    history_id=history_id,
    gzip=True,
    include_hidden=False,
    include_deleted=False,
    wait=True  # Wait for export to complete
)

# Download exported history
gi.histories.download_history(
    history_id=history_id,
    jeha_id=export_result['id'],
    outf='my_analysis_export.tar.gz'
)

print("History exported!")
```

### Complete Automation Script

```python
#!/usr/bin/env python3
"""
Automated LexicMap analysis pipeline
"""
import time
from bioblend.galaxy import GalaxyInstance

# Configuration
GALAXY_URL = 'https://test.galaxyproject.org'
API_KEY = 'YOUR_API_KEY'
QUERY_FILE = 'input_sequences.fasta'

# Initialize
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

# Create history
print("Creating history...")
history = gi.histories.create_history(name='Automated LexicMap Run')
hist_id = history['id']

# Upload data
print("Uploading query sequences...")
upload = gi.tools.upload_file(QUERY_FILE, hist_id, file_type='fasta')
query_dataset_id = upload['outputs'][0]['id']

# Wait for upload
time.sleep(5)

# Run LexicMap
print("Running LexicMap...")
tool_id = 'toolshed.g2.bx.psu.edu/repos/iuc/lexicmap/lexicmap_search/0.8.0+galaxy0'
inputs = {
    'query': {'src': 'hda', 'id': query_dataset_id},
    'reference': 'locally_cached',
    'align_min_match_pident': 80,
    'min_qcov_per_genome': 70
}
job = gi.tools.run_tool(hist_id, tool_id, inputs)
result_dataset_id = job['outputs'][0]['id']

# Wait for completion
print("Waiting for results...")
while True:
    ds = gi.datasets.show_dataset(result_dataset_id)
    if ds['state'] == 'ok':
        break
    elif ds['state'] == 'error':
        print("Job failed!")
        exit(1)
    time.sleep(10)

# Download results
print("Downloading results...")
gi.datasets.download_dataset(result_dataset_id, 'results.tsv', False)

# Export history
print("Exporting history...")
export = gi.histories.export_history(hist_id, gzip=True, wait=True)
gi.histories.download_history(hist_id, export['id'], 'analysis.tar.gz')

print(f"Complete! View history: {GALAXY_URL}/histories/view?id={hist_id}")
```

---

## Understanding LexicMap

### What is LexicMap?

LexicMap is a specialized sequence alignment tool designed for:
- **Querying genes, plasmids, or viral sequences** against massive genome databases
- **Fast searches** across millions of prokaryotic genomes
- **Memory-efficient** indexing and searching
- **Comprehensive results** including all hits with high sensitivity

### When to Use LexicMap

**Ideal use cases:**
- Identifying which organisms carry a specific gene
- Finding plasmid distribution across species
- Tracing horizontal gene transfer
- Screening for antimicrobial resistance genes
- Identifying prophages in bacterial genomes
- Environmental metagenomics source tracking

**Not suitable for:**
- Protein sequence searches (use BLAST or Diamond)
- Very short sequences <100 bp (use exact matching)
- Eukaryotic genome searches (optimized for prokaryotes)

### LexicMap vs Other Tools

| Feature | LexicMap | BLAST | DIAMOND | Bowtie2 |
|---------|----------|-------|---------|---------|
| **Input type** | Nucleotide | Both | Protein focus | Nucleotide |
| **Database size** | Millions of genomes | Limited | Large | Single ref |
| **Speed** | Very fast | Slow | Fast (protein) | Very fast |
| **Sensitivity** | High | High | High | Medium |
| **Use case** | Prokaryote screening | General | Protein search | Mapping |

### Performance Expectations

**Typical run times:**
- Single gene (500 bp) vs 1M genomes: 30 seconds - 2 minutes
- Plasmid (5 kb) vs 1M genomes: 5-15 minutes
- Multiple queries: ~1-2 min per query
- 16S rRNA gene vs 2.34M genomes: ~15 minutes

**Memory requirements:**
- Index building: Depends on database size (can be GBs)
- Searching: Relatively low (~2-8 GB)
- Galaxy instance: Handled by server

### Understanding Match Quality

**Query Coverage (qcovGnm):**
- Percentage of query that aligns to genome
- 100% = complete match
- 50-80% = partial match (may be fragmented assembly)
- <50% = incomplete/divergent match

**Percent Identity (pident):**
- Base-level identity in aligned region
- >95% = very similar (same species/strain)
- 85-95% = related (same genus)
- 70-85% = distant homologs
- <70% = weak similarity

**E-value:**
- Statistical significance (probability of random match)
- <1e-50 = highly significant
- 1e-10 to 1e-50 = significant
- >1e-5 = may be random

**Practical example:**
If searching for a resistance gene:
- qcovGnm >80% + pident >90% = High confidence hit
- qcovGnm 50-80% + pident >85% = Probable hit (investigate)
- qcovGnm <50% or pident <80% = Uncertain (needs validation)

---

## Advanced Usage

### Batch Processing Multiple Queries

#### Via Web Interface
1. Upload a multi-FASTA file with all query sequences
2. Run LexicMap once - it processes all sequences
3. Results table includes all queries with their matches

#### Via BioBlend (Recommended for large batches)
```python
import glob

query_files = glob.glob('queries/*.fasta')

for query_file in query_files:
    # Upload
    upload = gi.tools.upload_file(query_file, hist_id, file_type='fasta')
    dataset_id = upload['outputs'][0]['id']

    # Run LexicMap
    job = gi.tools.run_tool(hist_id, tool_id, {
        'query': {'src': 'hda', 'id': dataset_id},
        'reference': 'locally_cached',
        'align_min_match_pident': 80
    })

    print(f"Submitted: {query_file}")
```

### Filtering and Post-Processing Results

```python
import pandas as pd

# Load results
df = pd.read_csv('lexicmap_results.tsv', sep='\t')

# Filter high-quality hits
high_quality = df[
    (df['pident'] > 90) &
    (df['qcovGnm'] > 80) &
    (df['evalue'] < 1e-50)
]

# Count genomes per query
genome_counts = df.groupby('query')['sgenome'].nunique()
print("Genomes per query:")
print(genome_counts)

# Find queries in many genomes (widespread)
widespread = genome_counts[genome_counts > 100]
print(f"Widespread genes: {list(widespread.index)}")

# Export filtered results
high_quality.to_csv('filtered_hits.tsv', sep='\t', index=False)
```

### Comparing Multiple Analyses

```python
# Download multiple result datasets
result_ids = ['dataset1_id', 'dataset2_id', 'dataset3_id']
dataframes = []

for i, ds_id in enumerate(result_ids):
    gi.datasets.download_dataset(ds_id, f'temp_{i}.tsv', False)
    df = pd.read_csv(f'temp_{i}.tsv', sep='\t')
    df['analysis'] = f'Analysis_{i+1}'
    dataframes.append(df)

# Combine
combined = pd.concat(dataframes)

# Compare
pivot = combined.pivot_table(
    index='query',
    columns='analysis',
    values='hits',
    aggfunc='sum'
)
print(pivot)
```

### Using Collections for Multiple Samples

```python
# Upload multiple files as collection
file_paths = ['sample1.fasta', 'sample2.fasta', 'sample3.fasta']

# Upload files
dataset_ids = []
for path in file_paths:
    upload = gi.tools.upload_file(path, hist_id, file_type='fasta')
    dataset_ids.append(upload['outputs'][0]['id'])

# Create dataset collection
collection = gi.histories.create_dataset_collection(
    history_id=hist_id,
    collection_description={
        'name': 'My Samples',
        'type': 'list',
        'elements': [
            {'name': f'sample_{i}', 'src': 'hda', 'id': ds_id}
            for i, ds_id in enumerate(dataset_ids)
        ]
    }
)

# Run LexicMap on collection (processes all samples)
job = gi.tools.run_tool(hist_id, tool_id, {
    'query': {'src': 'hdca', 'id': collection['id']},
    'reference': 'locally_cached'
})
```

### Workflow Integration

1. **Create a workflow** in Galaxy web interface:
   - Upload data → LexicMap → Filter results → Generate report

2. **Save the workflow**

3. **Run workflow via API:**
```python
# Get workflows
workflows = gi.workflows.get_workflows()
workflow_id = workflows[0]['id']

# Run workflow
workflow_result = gi.workflows.invoke_workflow(
    workflow_id=workflow_id,
    inputs={
        '0': {'src': 'hda', 'id': query_dataset_id}
    },
    history_id=hist_id
)
```

---

## Troubleshooting

### History Import Issues

**Problem:** "Unable to import history from URL"
- **Check:** URL is publicly accessible (test in browser)
- **Check:** File is .tar.gz format (not .zip or .tar)
- **Solution:** Download file, then use "Import from file" with local file

**Problem:** "Import is stuck in pending"
- **Wait:** Large histories take time (>1GB can take 10-30 minutes)
- **Check:** History panel shows progress bar
- **Solution:** Refresh page; if still stuck after 1 hour, contact admin

**Problem:** "Datasets are red/failed after import"
- **Cause:** Original datasets may have been deleted
- **Solution:** Re-run failed jobs or upload source data again

**Problem:** Cannot see shared history
- **Check:** URL is correct and complete
- **Check:** History owner made it "accessible via link"
- **Solution:** Ask history owner to verify sharing settings

### LexicMap Tool Issues

**Problem:** "No tool outputs produced"
- **Check:** Input file is valid FASTA format
- **Check:** Sequences are nucleotide (not protein)
- **Check:** Sequences are >100 bp
- **Solution:** Validate FASTA file format

**Problem:** Job fails with "Out of memory"
- **Rare:** Server issue, not user-controllable on test.galaxyproject.org
- **Solution:** Reduce `top_n_genomes` parameter or split queries
- **Report:** Contact Galaxy support if persistent

**Problem:** "No results found"
- **Lower thresholds:** Reduce `align_min_match_pident` to 70%
- **Lower coverage:** Reduce `min_qcov_per_genome` to 50%
- **Check database:** Ensure appropriate reference database selected
- **Validate query:** Confirm sequences are from prokaryotes

**Problem:** Too many results (thousands of hits)
- **Increase identity:** Set `align_min_match_pident` to 90-95%
- **Increase coverage:** Set `min_qcov_per_genome` to 80-90%
- **Limit genomes:** Set `top_n_genomes` to 100 or 1000
- **Check query:** Very common genes (16S, housekeeping) produce many hits

**Problem:** Job stays yellow/running for hours
- **Normal:** Complex queries can take time
- **Check:** Job info (i icon) for status messages
- **Wait:** Up to 30 minutes for large queries
- **Contact:** Galaxy support if >1 hour

### BioBlend / API Issues

**Problem:** "Invalid API key" error
- **Check:** API key copied correctly (no spaces)
- **Regenerate:** Create new API key in Galaxy
- **Check URL:** Ensure using correct Galaxy instance URL

**Problem:** Connection timeout
- **Check:** Internet connection
- **Check:** Galaxy instance is accessible (open in browser)
- **Retry:** Connection issues may be temporary

**Problem:** "Tool not found" error
- **Check:** Tool ID is correct and complete
- **Solution:** Search for tool: `gi.tools.get_tools()` and find correct ID
- **Note:** Tool IDs include full Tool Shed path

**Problem:** Cannot download large datasets
- **Solution:** Increase timeout:
```python
gi.datasets.download_dataset(
    dataset_id=ds_id,
    file_path='output.tsv',
    use_default_filename=False,
    maxwait=600  # 10 minutes
)
```

**Problem:** Upload fails silently
- **Check:** File exists and is readable
- **Check:** File format specified correctly
- **Add error handling:**
```python
try:
    upload = gi.tools.upload_file(path, hist_id)
    print(f"Success: {upload}")
except Exception as e:
    print(f"Upload failed: {e}")
```

### Data Format Issues

**Problem:** "Invalid FASTA format" error
- **Check:** File starts with `>` (header line)
- **Check:** No blank lines at start
- **Check:** Sequences contain only ATGCN characters
- **Fix:** Use Galaxy "FASTA Tabular converter" tool

**Problem:** Results display incorrectly
- **Check:** File type is set to "tabular" or "tsv"
- **Fix:** Click pencil icon (edit attributes) → change datatype

**Problem:** Multi-FASTA file treated as single sequence
- **Rare:** Usually handled correctly
- **Check:** Upload file type is "fasta" not "txt"

### Performance Issues

**Problem:** Analysis is very slow
- **Normal:** Searching millions of genomes takes time
- **Reduce scope:** Check fewer reference databases
- **Increase thresholds:** Higher identity/coverage = faster
- **Split queries:** Run separately if multi-FASTA is large

**Problem:** Cannot upload large files via browser
- **Limit:** Browser uploads typically <2GB
- **Solution:** Use FTP upload:
  1. Upload file to Galaxy FTP (requires account setup)
  2. Use "Upload from FTP" in Galaxy interface
- **Alternative:** Use BioBlend API upload

---

## Additional Resources

### Galaxy Documentation
- **Main Galaxy Help**: https://help.galaxyproject.org/
- **Training Materials**: https://training.galaxyproject.org/
- **API Documentation**: https://usegalaxy.org/api/docs
- **Test Instance**: https://test.galaxyproject.org/

### BioBlend Resources
- **Documentation**: https://bioblend.readthedocs.io/
- **GitHub**: https://github.com/galaxyproject/bioblend
- **API Reference**: https://bioblend.readthedocs.io/en/latest/api_docs/galaxy/all.html
- **Examples**: https://github.com/galaxyproject/bioblend/tree/main/docs/examples

### LexicMap Resources
- **GitHub Repository**: https://github.com/shenwei356/LexicMap
- **Official Documentation**: https://bioinf.shenwei.me/LexicMap/
- **Publication**: Shen et al. (2025), Nature Biotechnology
- **Bioconda**: https://anaconda.org/bioconda/lexicmap
- **Tool Shed Entry**: https://toolshed.g2.bx.psu.edu/view/iuc/lexicmap

### Getting Help

**Galaxy Community:**
- **Forum**: https://help.galaxyproject.org/
- **Chat**: https://matrix.to/#/#galaxyproject_Lobby:gitter.im
- **Email**: help@galaxyproject.org

**LexicMap Issues:**
- **GitHub Issues**: https://github.com/shenwei356/LexicMap/issues

**For This Tutorial:**
- Check error messages in Galaxy job details
- Review BioBlend traceback for API errors
- Consult Galaxy training materials for workflows

---

## Quick Reference

### Essential Links
```
Test Galaxy Instance: https://test.galaxyproject.org/
Test History: https://test.galaxyproject.org/u/anton/h/test-history
LexicMap Tool: https://test.galaxyproject.org/?tool_id=toolshed.g2.bx.psu.edu%2Frepos%2Fiuc%2Flexicmap%2Flexicmap_search%2F0.8.0%2Bgalaxy0
API Docs: https://test.galaxyproject.org/api/docs
```

### Common BioBlend Commands
```python
# Connect
gi = GalaxyInstance(url=URL, key=API_KEY)

# Create history
hist = gi.histories.create_history(name="My Analysis")

# Upload file
upload = gi.tools.upload_file(path, hist['id'], file_type='fasta')

# Run LexicMap
job = gi.tools.run_tool(hist['id'], tool_id, inputs)

# Check status
status = gi.datasets.show_dataset(dataset_id)

# Download result
gi.datasets.download_dataset(dataset_id, 'output.tsv', False)
```

### LexicMap Parameter Quick Reference

| Parameter | Gene Search | Plasmid Search | Strict Match |
|-----------|-------------|----------------|--------------|
| Min % identity | 80 | 70 | 95 |
| Min qcov genome | 70 | 50 | 90 |
| Min qcov HSP | 70 | 0 | 80 |
| Min match length | - | 1000 | - |
| Top N genomes | 10000 | 10000 | 1000 |

---

**Document Version:** 1.0
**Last Updated:** November 2024
**Galaxy Test Instance Version:** 26.0
**LexicMap Tool Version:** 0.8.0+galaxy0
**Compatible BioBlend Version:** 1.6.0+

---

## Appendix: Example Workflows

### Example 1: Antimicrobial Resistance Gene Screening

```python
#!/usr/bin/env python3
from bioblend.galaxy import GalaxyInstance

gi = GalaxyInstance(
    url='https://test.galaxyproject.org',
    key='YOUR_API_KEY'
)

# Create history
hist = gi.histories.create_history(name='AMR Gene Screening')

# Upload resistance genes
upload = gi.tools.upload_file('amr_genes.fasta', hist['id'], file_type='fasta')
query_id = upload['outputs'][0]['id']

# Run LexicMap with high stringency
tool_id = 'toolshed.g2.bx.psu.edu/repos/iuc/lexicmap/lexicmap_search/0.8.0+galaxy0'
job = gi.tools.run_tool(hist['id'], tool_id, {
    'query': {'src': 'hda', 'id': query_id},
    'reference': 'locally_cached',
    'align_min_match_pident': 90,  # High identity for AMR
    'min_qcov_per_genome': 80
})

print(f"AMR screening job submitted: {job['id']}")
```

### Example 2: Plasmid Distribution Analysis

```python
# Lower thresholds for plasmids
job = gi.tools.run_tool(hist['id'], tool_id, {
    'query': {'src': 'hda', 'id': plasmid_dataset_id},
    'reference': 'locally_cached',
    'align_min_match_pident': 70,  # Lower for plasmids
    'min_qcov_per_genome': 50,
    'min_qcov_per_hsp': 0,  # Allow fragmented matches
    'align_min_match_len': 1000  # Longer matches
})
```

### Example 3: Multi-Sample Environmental Analysis

```python
# Process multiple environmental samples
samples = ['soil_sample1.fasta', 'soil_sample2.fasta', 'water_sample.fasta']

for sample in samples:
    upload = gi.tools.upload_file(sample, hist['id'], file_type='fasta')
    query_id = upload['outputs'][0]['id']

    job = gi.tools.run_tool(hist['id'], tool_id, {
        'query': {'src': 'hda', 'id': query_id},
        'reference': 'locally_cached',
        'align_min_match_pident': 75,
        'min_qcov_per_genome': 60
    })

    print(f"Sample {sample}: Job {job['id']}")
```

---

**End of Documentation**
