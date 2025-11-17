#!/usr/bin/env python3
"""
Run DESeq2 CORRECTLY using collections.
Feed the entire collection and provide factor information to tell DESeq2 which samples are which.
"""

from bioblend.galaxy import GalaxyInstance
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

def create_factor_file(gi, history_id, collection_id, strain_mapping, factor_filename):
    """
    Create a factor file that maps samples in the collection to their conditions.
    This file tells DESeq2 which samples belong to which factor level.
    """

    # Get collection details
    collection_details = gi.histories.show_dataset_collection(history_id, collection_id)
    elements = collection_details.get('elements', [])

    # Create factor file content
    factor_lines = ["SampleName\tstrain\n"]

    for elem in elements:
        sample_name = elem.get('element_identifier', '')

        # Find strain for this sample
        strain = None
        for srr_id, sample_strain in strain_mapping.items():
            if srr_id in sample_name:
                strain = sample_strain
                break

        if strain:
            factor_lines.append(f"{sample_name}\t{strain}\n")
        else:
            print(f"  Warning: Could not find strain for {sample_name}")

    factor_content = "".join(factor_lines)

    # Write factor file to disk first
    local_factor_path = f"/tmp/{factor_filename}"
    with open(local_factor_path, 'w') as f:
        f.write(factor_content)

    print(f"✓ Created local factor file: {local_factor_path}")

    # Upload factor file to Galaxy
    try:
        result = gi.tools.upload_file(
            local_factor_path,
            history_id,
            file_name=factor_filename,
            file_type='tabular'
        )
        print(f"✓ Uploaded factor file to Galaxy: {factor_filename}")
        return result
    except Exception as e:
        print(f"✗ Error uploading factor file: {e}")
        return None

def run_deseq2_with_collection(gi, history_id, collection_id, collection_name,
                                experiment_type, strain_mapping):
    """
    Run DESeq2 on the ENTIRE collection with factor information.
    """

    print(f"\n{'='*70}")
    print(f"Running DESeq2 for {experiment_type} experiment")
    print(f"Collection: {collection_name}")
    print(f"{'='*70}")

    # Get collection details to show what we're analyzing
    collection_details = gi.histories.show_dataset_collection(history_id, collection_id)
    elements = collection_details.get('elements', [])

    print(f"\nCollection has {len(elements)} samples:")

    ar0382_count = 0
    ar0387_count = 0

    for elem in elements:
        sample_name = elem.get('element_identifier', '')
        strain = None
        for srr_id, sample_strain in strain_mapping.items():
            if srr_id in sample_name:
                strain = sample_strain
                if strain == 'AR0382':
                    ar0382_count += 1
                elif strain == 'AR0387':
                    ar0387_count += 1
                break
        print(f"  - {sample_name}: {strain}")

    print(f"\nSummary: {ar0382_count} AR0382 samples, {ar0387_count} AR0387 samples")

    # Create factor file
    factor_filename = f"factor_file_{experiment_type.replace(' ', '_')}.tsv"
    factor_file = create_factor_file(gi, history_id, collection_id, strain_mapping, factor_filename)

    if not factor_file:
        print("✗ Failed to create factor file")
        return None

    # Get the factor file dataset ID from the upload result
    import time

    # The upload result contains the created datasets
    factor_dataset_id = None
    if factor_file and 'outputs' in factor_file:
        for output in factor_file['outputs']:
            if output.get('name') == factor_filename:
                factor_dataset_id = output.get('id')
                print(f"  Factor file dataset ID: {factor_dataset_id}")
                break

    # If not found in outputs, search history
    if not factor_dataset_id:
        print("  Searching history for factor file...")
        time.sleep(3)  # Wait for upload to complete
        history_contents = gi.histories.show_history(history_id, contents=True)
        for item in reversed(history_contents):  # Check most recent first
            if item.get('name') == factor_filename and item.get('state') != 'deleted':
                factor_dataset_id = item.get('id')
                print(f"  Found factor file dataset ID: {factor_dataset_id}")
                break

    if not factor_dataset_id:
        print("✗ Could not find uploaded factor file")
        return None

    # Now run DESeq2 with the collection and factor file
    print(f"\nSubmitting DESeq2 job...")

    deseq2_tool_id = "toolshed.g2.bx.psu.edu/repos/iuc/deseq2/deseq2/2.11.40.8+galaxy0"

    # DESeq2 parameters - using the collection with a factor file
    deseq2_params = {
        'select_data': {
            'how': 'datasets_vs_factors',  # This mode uses factor file
            'countsFile': {
                'src': 'hdca',
                'id': collection_id
            },
            'factorFile': {
                'src': 'hda',
                'id': factor_dataset_id
            },
            'tximport': {
                'txtype': 'none'
            }
        },
        'advanced_options': {
            'use_beta_priors': False,
            'alpha': 0.01,  # FDR < 0.01 from paper
            'lfcThreshold': 0  # Filter for |LFC| >= 1 in post-processing
        },
        'output_options': {
            'output_normalized': True,
            'output_rlog': False
        },
        'tximport': {
            'txtype': 'none'
        }
    }

    try:
        result = gi.tools.run_tool(
            history_id=history_id,
            tool_id=deseq2_tool_id,
            tool_inputs=deseq2_params
        )
        print(f"✓ DESeq2 job submitted!")
        print(f"  Job outputs: {len(result.get('outputs', []))}")
        for output in result.get('outputs', []):
            print(f"    - {output.get('name')}")

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
    print(f"Found history: {history['name']}")

    # Get the collections
    history_contents = gi.histories.show_history(history_id, contents=True)

    in_vitro_collection = None
    in_vivo_collection = None

    for item in history_contents:
        if item.get('history_content_type') == 'dataset_collection':
            name = item['name']
            # Get the original collections (not the sub-collections we created)
            if name == 'PRJNA1086003_in_vitro':
                in_vitro_collection = item
            elif name == 'PRJNA1086003_in_vivo':
                in_vivo_collection = item

    if not in_vitro_collection or not in_vivo_collection:
        print("Error: Could not find in_vitro and in_vivo collections")
        return

    print(f"\nUsing collections:")
    print(f"  In vitro: #{in_vitro_collection['hid']} - {in_vitro_collection['name']}")
    print(f"  In vivo: #{in_vivo_collection['hid']} - {in_vivo_collection['name']}")

    # Read strain mappings
    in_vitro_strains = read_strain_mapping('samples_in_vitro.tsv')
    in_vivo_strains = read_strain_mapping('samples_in_vivo.tsv')

    # Run DESeq2 for in vitro
    in_vitro_result = run_deseq2_with_collection(
        gi,
        history_id,
        in_vitro_collection['id'],
        in_vitro_collection['name'],
        "in vitro",
        in_vitro_strains
    )

    # Run DESeq2 for in vivo
    in_vivo_result = run_deseq2_with_collection(
        gi,
        history_id,
        in_vivo_collection['id'],
        in_vivo_collection['name'],
        "in vivo",
        in_vivo_strains
    )

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"In vitro DESeq2: {'✓ Success' if in_vitro_result else '✗ Failed'}")
    print(f"In vivo DESeq2: {'✓ Success' if in_vivo_result else '✗ Failed'}")
    print(f"\nExpected from paper:")
    print(f"  In vitro: ~76 DEGs (LFC ≥ |1|, FDR < 0.01)")
    print(f"  In vivo: ~259 DEGs (LFC ≥ |1|, FDR < 0.01)")
    print(f"\nView results at: https://usegalaxy.org/u/cartman/h/prjna1086003")

if __name__ == "__main__":
    main()
