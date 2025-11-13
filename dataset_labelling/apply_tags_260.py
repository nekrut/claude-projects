#!/usr/bin/env python3
"""
Script to apply group tags to collection #260 elements based on labels.tsv
"""

from bioblend.galaxy import GalaxyInstance
import csv

# Galaxy credentials
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_ID = "bbd44e69cb8906b5713a37cc4e6846ea"
COLLECTION_260_ID = "50490a95897034a8"

# Read the labels.tsv file
print("Reading labels.tsv...")
label_mapping = {}
with open('labels.tsv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        srr_id = row[0]
        group_tag = row[1]
        label_mapping[srr_id] = group_tag
        print(f"  {srr_id} -> {group_tag}")

# Connect to Galaxy
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

print("\nFetching collection #260 details...")
collection_details = gi.histories.show_dataset_collection(
    history_id=HISTORY_ID,
    dataset_collection_id=COLLECTION_260_ID
)

print(f"\nApplying tags to {collection_details['element_count']} elements:\n")

for element in collection_details['elements']:
    elem_identifier = element['element_identifier']
    dataset_id = element['object']['id']
    current_tags = element['object'].get('tags', [])

    # Get expected tag from labels.tsv
    expected_tag = label_mapping.get(elem_identifier, None)

    if expected_tag:
        print(f"Processing {elem_identifier}...")
        print(f"  Dataset ID: {dataset_id}")
        print(f"  Current tags: {current_tags}")
        print(f"  Adding tag: {expected_tag}")

        # Update the dataset with the new tag
        try:
            gi.histories.update_dataset(
                history_id=HISTORY_ID,
                dataset_id=dataset_id,
                tags=[expected_tag]
            )
            print(f"  ✓ Successfully tagged!")
        except Exception as e:
            print(f"  ✗ Error: {e}")
    else:
        print(f"? {elem_identifier}: No label specified in labels.tsv")

print("\n" + "="*60)
print("Tag application complete!")
