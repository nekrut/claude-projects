#!/usr/bin/env python3
"""
Run DESeq2 in Galaxy to replicate the differential expression analysis from the paper.
Comparing AR0382 (aggregative) vs AR0387 (non-aggregative) strains.
"""

from bioblend.galaxy import GalaxyInstance
import time
import csv

# Galaxy connection details
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "prjna1086003"

def read_strain_mapping(tsv_file):
    """Read mapping of Run IDs to strains from TSV file."""
    mapping = {}
    with open(tsv_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            mapping[row['Run']] = row['strain']
    return mapping

def find_tool_id(gi, tool_name):
    """Find the tool ID for DESeq2."""
    tools = gi.tools.get_tools(name=tool_name)
    if tools:
        return tools[0]['id']
    return None

def run_deseq2(gi, history_id, collection_id, collection_name, experiment_type, strain_mapping):
    """
    Run DESeq2 on a collection.

    For the paper's analysis:
    - Factor: strain (AR0382 vs AR0387)
    - Strain info comes from TSV files
    """

    print(f"\n{'='*60}")
    print(f"Running DESeq2 for {experiment_type} experiment")
    print(f"Collection: {collection_name}")
    print(f"{'='*60}")

    # Find DESeq2 tool
    deseq2_tool_id = "toolshed.g2.bx.psu.edu/repos/iuc/deseq2/deseq2/2.11.40.8+galaxy0"

    print(f"\nUsing DESeq2 tool: {deseq2_tool_id}")

    # Get collection details to identify factor levels
    history_contents = gi.histories.show_history(history_id, contents=True)
    collection = None
    for item in history_contents:
        if item.get('id') == collection_id and item.get('history_content_type') == 'dataset_collection':
            collection = item
            break

    if not collection:
        print(f"Error: Collection not found")
        return None

    collection_details = gi.histories.show_dataset_collection(history_id, collection_id)
    elements = collection_details.get('elements', [])

    # Identify factor levels using strain mapping
    ar0382_samples = []
    ar0387_samples = []

    for elem in elements:
        name = elem.get('element_identifier', '')
        # Find the SRR ID in the element name
        for srr_id, strain in strain_mapping.items():
            if srr_id in name:
                if strain == 'AR0382':
                    ar0382_samples.append(name)
                elif strain == 'AR0387':
                    ar0387_samples.append(name)
                break

    print(f"\nAR0382 samples (n={len(ar0382_samples)}): {ar0382_samples}")
    print(f"AR0387 samples (n={len(ar0387_samples)}): {ar0387_samples}")

    # Prepare factor information
    # We need to create a factor file that maps samples to conditions
    factor_name = "strain"

    # For DESeq2, we need to specify:
    # 1. The count matrix (our collection)
    # 2. Factor information (which samples belong to which group)
    # 3. Comparison to make (AR0382 vs AR0387)

    print(f"\nPreparing DESeq2 analysis:")
    print(f"  Factor: {factor_name}")
    print(f"  Factor level 1 (treatment): AR0382 ({len(ar0382_samples)} replicates)")
    print(f"  Factor level 2 (control): AR0387 ({len(ar0387_samples)} replicates)")
    print(f"  Comparison: AR0382 vs AR0387")

    # DESeq2 parameters based on the paper:
    # - LFC threshold: 1 (≥ |1|)
    # - FDR: 0.01 (< 0.01)

    deseq2_params = {
        'select_data': {
            'rep_factorName': [factor_name],
            'rep_factorLevel': [
                {
                    'factorLevel': 'AR0382',
                    'countsFile': [{'src': 'hdca', 'id': collection_id}]
                },
                {
                    'factorLevel': 'AR0387',
                    'countsFile': [{'src': 'hdca', 'id': collection_id}]
                }
            ],
            'how': 'collections',
            'tximport|txtype': 'none',
            'tximport|mapping_format|gtf_file': None
        },
        'output_options': {
            'output_normalized': 'true',
            'output_rlog': 'true'
        },
        'advanced_options': {
            'use_beta_priors': 'false',
            'alpha': '0.01',  # FDR threshold from paper
            'lfcThreshold': '1'  # Log2 fold change threshold from paper
        }
    }

    try:
        print(f"\nSubmitting DESeq2 job...")

        # Run the tool
        result = gi.tools.run_tool(
            history_id=history_id,
            tool_id=deseq2_tool_id,
            tool_inputs=deseq2_params
        )

        print(f"✓ DESeq2 job submitted successfully!")
        print(f"  Job ID: {result.get('id', 'N/A')}")
        print(f"  Outputs: {len(result.get('outputs', []))} files")

        return result

    except Exception as e:
        print(f"✗ Error running DESeq2: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    # Connect to Galaxy
    gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

    # Get the history
    all_histories = gi.histories.get_histories()
    history = None
    for h in all_histories:
        if HISTORY_NAME.lower() in h['name'].lower():
            history = h
            break

    if not history:
        print(f"Error: History containing '{HISTORY_NAME}' not found")
        return

    history_id = history['id']
    print(f"Found history: {history['name']} (ID: {history_id})")

    # Get the collections
    history_contents = gi.histories.show_history(history_id, contents=True)

    in_vitro_collection = None
    in_vivo_collection = None

    for item in history_contents:
        if item.get('history_content_type') == 'dataset_collection':
            if 'in_vitro' in item['name']:
                in_vitro_collection = item
            elif 'in_vivo' in item['name']:
                in_vivo_collection = item

    if not in_vitro_collection or not in_vivo_collection:
        print("Error: Could not find both in_vitro and in_vivo collections")
        return

    print(f"\nFound collections:")
    print(f"  In vitro: {in_vitro_collection['name']} (#{in_vitro_collection['hid']})")
    print(f"  In vivo: {in_vivo_collection['name']} (#{in_vivo_collection['hid']})")

    # Read strain mappings from TSV files
    in_vitro_strains = read_strain_mapping('samples_in_vitro.tsv')
    in_vivo_strains = read_strain_mapping('samples_in_vivo.tsv')

    print(f"\nStrain mapping loaded:")
    print(f"  In vitro: {len(in_vitro_strains)} samples")
    print(f"  In vivo: {len(in_vivo_strains)} samples")

    # Run DESeq2 for in vitro experiment
    in_vitro_result = run_deseq2(
        gi,
        history_id,
        in_vitro_collection['id'],
        in_vitro_collection['name'],
        "in vitro",
        in_vitro_strains
    )

    # Run DESeq2 for in vivo experiment
    in_vivo_result = run_deseq2(
        gi,
        history_id,
        in_vivo_collection['id'],
        in_vivo_collection['name'],
        "in vivo",
        in_vivo_strains
    )

    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    print(f"In vitro DESeq2: {'Success' if in_vitro_result else 'Failed'}")
    print(f"In vivo DESeq2: {'Success' if in_vivo_result else 'Failed'}")
    print(f"\nExpected results (from paper):")
    print(f"  In vitro: ~76 DEGs (LFC ≥ |1|, FDR < 0.01)")
    print(f"  In vivo: ~259 DEGs (LFC ≥ |1|, FDR < 0.01)")
    print(f"\nCheck your Galaxy history for the DESeq2 results!")

if __name__ == "__main__":
    main()
