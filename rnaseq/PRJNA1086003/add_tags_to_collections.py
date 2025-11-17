#!/usr/bin/env python3
"""
Add tags from Sample Name column to datasets in Galaxy collections.
"""

import csv
from bioblend.galaxy import GalaxyInstance

# Galaxy connection details
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "prjna1086003"

def read_sample_mapping(tsv_file):
    """Read mapping of Run IDs to Sample Names from TSV file."""
    mapping = {}
    with open(tsv_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            mapping[row['Run']] = row['Sample Name']
    return mapping

def add_tags_to_collection(gi, history_id, collection_hid, sample_mapping, collection_name):
    """Add tags to datasets in a collection."""
    print(f"\nProcessing collection #{collection_hid}: {collection_name}")

    # Get history contents to find the collection
    history_contents = gi.histories.show_history(history_id, contents=True)

    # Find the collection
    collection = None
    for item in history_contents:
        if item.get('hid') == collection_hid and item.get('history_content_type') == 'dataset_collection':
            collection = item
            break

    if not collection:
        print(f"Error: Collection #{collection_hid} not found")
        return

    print(f"Found collection: {collection['name']}")

    # Get collection details
    collection_details = gi.histories.show_dataset_collection(
        history_id,
        collection['id']
    )

    elements = collection_details.get('elements', [])
    print(f"Collection has {len(elements)} elements")

    # Process each element
    tagged_count = 0
    for element in elements:
        element_name = element.get('element_identifier', '')

        # Find matching sample
        matched_sample = None
        matched_run = None
        for run_id, sample_name in sample_mapping.items():
            if run_id in element_name:
                matched_sample = sample_name
                matched_run = run_id
                break

        if matched_sample:
            # Get the dataset
            dataset = element.get('object', {})
            dataset_id = dataset.get('id')

            if dataset_id:
                try:
                    # Get current tags
                    dataset_info = gi.datasets.show_dataset(dataset_id)
                    current_tags = dataset_info.get('tags', [])

                    # Add the new tag if not already present
                    if matched_sample not in current_tags:
                        current_tags.append(matched_sample)

                        # Update dataset with new tags using histories API
                        gi.histories.update_dataset(
                            history_id,
                            dataset_id,
                            tags=current_tags
                        )
                        print(f"  ✓ Tagged dataset '{element_name}' with '{matched_sample}'")
                        tagged_count += 1
                    else:
                        print(f"  - Dataset '{element_name}' already has tag '{matched_sample}'")
                except Exception as e:
                    print(f"  ✗ Error tagging dataset '{element_name}': {e}")
        else:
            print(f"  ? No matching sample found for element '{element_name}'")

    print(f"Successfully tagged {tagged_count} datasets in {collection_name}")

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

    # Read sample mappings
    in_vitro_mapping = read_sample_mapping('samples_in_vitro.tsv')
    in_vivo_mapping = read_sample_mapping('samples_in_vivo.tsv')

    print(f"\nIn vitro mapping: {len(in_vitro_mapping)} samples")
    print(f"In vivo mapping: {len(in_vivo_mapping)} samples")

    # Add tags to both collections
    add_tags_to_collection(gi, history_id, 621, in_vitro_mapping, "PRJNA1086003_in_vitro")
    add_tags_to_collection(gi, history_id, 629, in_vivo_mapping, "PRJNA1086003_in_vivo")

    print("\n✓ Tagging completed!")

if __name__ == "__main__":
    main()
