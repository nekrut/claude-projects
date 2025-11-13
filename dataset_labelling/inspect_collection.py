#!/usr/bin/env python3
"""
Script to inspect collection #402 and its elements
"""

from bioblend.galaxy import GalaxyInstance

# Galaxy credentials from script.md
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"

# Collection details from previous script
HISTORY_ID = "bbd44e69cb8906b5713a37cc4e6846ea"
COLLECTION_ID = "92456119b5c0275e"

# Connect to Galaxy instance
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

print("Fetching collection #402 details...")
# The correct method is show_dataset_collection with dataset_collection_id
collection_details = gi.histories.show_dataset_collection(
    history_id=HISTORY_ID,
    dataset_collection_id=COLLECTION_ID
)

print(f"\nCollection Name: {collection_details['name']}")
print(f"Collection Type: {collection_details['collection_type']}")
print(f"Element Count: {collection_details['element_count']}")
print(f"\nElements in collection:")

# Display all elements
for idx, element in enumerate(collection_details['elements'], 1):
    elem_name = element['element_identifier']
    elem_type = element['element_type']

    print(f"\n{idx}. Element: {elem_name}")
    print(f"   Type: {elem_type}")

    if elem_type == 'hda':  # History Dataset Association
        dataset_id = element['object']['id']
        dataset_name = element['object'].get('name', 'N/A')
        dataset_tags = element['object'].get('tags', [])

        print(f"   Dataset Name: {dataset_name}")
        print(f"   Dataset ID: {dataset_id}")
        print(f"   Current Tags: {dataset_tags}")

        # Check if this dataset name matches any in our labels.tsv
        # The labels.tsv has SRR identifiers
        print(f"   Checking for SRR identifier in name...")
        if 'SRR' in dataset_name:
            # Extract SRR number
            import re
            srr_match = re.search(r'SRR\d+', dataset_name)
            if srr_match:
                srr_id = srr_match.group()
                print(f"   Found SRR ID: {srr_id}")

print("\n" + "="*60)
print("Summary: Found all elements in collection #402")
