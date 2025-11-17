#!/usr/bin/env python3
"""
Split Galaxy collection #601 into in_vitro and in_vivo collections
based on the sample TSV files.
"""

import csv
from bioblend.galaxy import GalaxyInstance

# Galaxy connection details
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "prjna1086003"

def read_sample_ids(tsv_file):
    """Read sample Run IDs from TSV file."""
    sample_ids = []
    with open(tsv_file, 'r') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            sample_ids.append(row['Run'])
    return sample_ids

def main():
    # Connect to Galaxy
    gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

    # Get all histories and find the one we need
    all_histories = gi.histories.get_histories()
    print(f"Found {len(all_histories)} histories")

    # Try to find by name (case-insensitive)
    history = None
    for h in all_histories:
        if HISTORY_NAME.lower() in h['name'].lower():
            history = h
            break

    if not history:
        print(f"Available histories:")
        for h in all_histories[:10]:  # Show first 10
            print(f"  - {h['name']} (ID: {h['id']})")
        print(f"\nError: History containing '{HISTORY_NAME}' not found")
        return

    history_id = history['id']
    print(f"Found history: {history['name']} (ID: {history_id})")

    # Get collection #601
    collection_id = "601"
    try:
        # Get all datasets in the history to find collection #601
        history_contents = gi.histories.show_history(history_id, contents=True)

        # Find the collection with hid 601
        collection = None
        for item in history_contents:
            if item.get('hid') == 601 and item.get('history_content_type') == 'dataset_collection':
                collection = item
                break

        if not collection:
            print(f"Error: Collection #601 not found in history")
            print("Available collections:")
            for item in history_contents:
                if item.get('history_content_type') == 'dataset_collection':
                    print(f"  #{item['hid']}: {item['name']}")
            return

        print(f"Found collection #601: {collection['name']}")

        # Get full collection details
        collection_details = gi.histories.show_dataset_collection(
            history_id,
            collection['id']
        )

        # Read sample IDs from TSV files
        in_vitro_samples = read_sample_ids('samples_in_vitro.tsv')
        in_vivo_samples = read_sample_ids('samples_in_vivo.tsv')

        print(f"\nIn vitro samples: {len(in_vitro_samples)}")
        print(f"In vivo samples: {len(in_vivo_samples)}")

        # Get collection elements
        elements = collection_details.get('elements', [])
        print(f"\nCollection has {len(elements)} elements")

        # Identify elements for each group
        in_vitro_elements = []
        in_vivo_elements = []

        for element in elements:
            element_name = element.get('element_identifier', '')

            # Check if element name contains any of the sample IDs
            matched_vitro = False
            matched_vivo = False

            for sample_id in in_vitro_samples:
                if sample_id in element_name:
                    in_vitro_elements.append(element)
                    matched_vitro = True
                    break

            if not matched_vitro:
                for sample_id in in_vivo_samples:
                    if sample_id in element_name:
                        in_vivo_elements.append(element)
                        matched_vivo = True
                        break

            if not matched_vitro and not matched_vivo:
                print(f"Warning: Element '{element_name}' not matched to any sample")

        print(f"\nMatched {len(in_vitro_elements)} in vitro elements")
        print(f"Matched {len(in_vivo_elements)} in vivo elements")

        # Create new collections
        if in_vitro_elements:
            print("\nCreating in_vitro collection...")
            in_vitro_collection = gi.histories.create_dataset_collection(
                history_id=history_id,
                collection_description={
                    'collection_type': collection_details['collection_type'],
                    'name': 'PRJNA1086003_in_vitro',
                    'element_identifiers': [
                        {
                            'id': elem['object']['id'],
                            'name': elem['element_identifier'],
                            'src': 'hda'
                        }
                        for elem in in_vitro_elements
                    ]
                }
            )
            print(f"Created in_vitro collection: {in_vitro_collection['name']} (#{in_vitro_collection.get('hid', 'N/A')})")

        if in_vivo_elements:
            print("\nCreating in_vivo collection...")
            in_vivo_collection = gi.histories.create_dataset_collection(
                history_id=history_id,
                collection_description={
                    'collection_type': collection_details['collection_type'],
                    'name': 'PRJNA1086003_in_vivo',
                    'element_identifiers': [
                        {
                            'id': elem['object']['id'],
                            'name': elem['element_identifier'],
                            'src': 'hda'
                        }
                        for elem in in_vivo_elements
                    ]
                }
            )
            print(f"Created in_vivo collection: {in_vivo_collection['name']} (#{in_vivo_collection.get('hid', 'N/A')})")

        print("\n✓ Collections created successfully!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
