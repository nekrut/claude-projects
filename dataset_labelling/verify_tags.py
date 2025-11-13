#!/usr/bin/env python3
"""
Script to verify that the tags in collection #402 match labels.tsv
"""

from bioblend.galaxy import GalaxyInstance
import csv

# Galaxy credentials from script.md
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"

# Collection details
HISTORY_ID = "bbd44e69cb8906b5713a37cc4e6846ea"
COLLECTION_ID = "92456119b5c0275e"

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

print("\nFetching collection #402 details...")
collection_details = gi.histories.show_dataset_collection(
    history_id=HISTORY_ID,
    dataset_collection_id=COLLECTION_ID
)

print(f"\nVerifying tags for {collection_details['element_count']} elements:\n")

all_match = True
for element in collection_details['elements']:
    elem_identifier = element['element_identifier']
    current_tags = element['object'].get('tags', [])

    # Get expected tag from labels.tsv
    expected_tag = label_mapping.get(elem_identifier, None)

    if expected_tag:
        # Check if the expected tag is in current tags
        if expected_tag in current_tags:
            print(f"✓ {elem_identifier}: Tag matches! (has '{expected_tag}')")
        else:
            print(f"✗ {elem_identifier}: Tag MISMATCH!")
            print(f"    Expected: {expected_tag}")
            print(f"    Current:  {current_tags}")
            all_match = False
    else:
        print(f"? {elem_identifier}: No label specified in labels.tsv")
        print(f"    Current tags: {current_tags}")

print("\n" + "="*60)
if all_match:
    print("SUCCESS: All tags match the specifications in labels.tsv!")
else:
    print("MISMATCH: Some tags do not match labels.tsv")
