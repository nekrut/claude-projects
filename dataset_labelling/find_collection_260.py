#!/usr/bin/env python3
"""
Script to locate and inspect collection #260
"""

from bioblend.galaxy import GalaxyInstance

# Galaxy credentials
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_ID = "bbd44e69cb8906b5713a37cc4e6846ea"

# Connect to Galaxy instance
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

print("Fetching history contents to find collection #260...")
history_contents = gi.histories.show_history(history_id=HISTORY_ID, contents=True)

# Filter for collections
collection_items = [item for item in history_contents if item.get('history_content_type') == 'dataset_collection']

# Find collection #260
for item in collection_items:
    hid = item.get('hid', 'N/A')
    if hid == 260:
        print(f"\n*** FOUND COLLECTION #260! ***")
        print(f"Name: {item.get('name')}")
        print(f"ID: {item.get('id')}")
        print(f"Type: {item.get('collection_type')}")

        collection_id = item.get('id')

        # Get detailed collection information
        print("\nFetching collection details...")
        collection_details = gi.histories.show_dataset_collection(
            history_id=HISTORY_ID,
            dataset_collection_id=collection_id
        )

        print(f"\nCollection Name: {collection_details['name']}")
        print(f"Collection Type: {collection_details['collection_type']}")
        print(f"Element Count: {collection_details['element_count']}")
        print(f"\nElements in collection:")

        for idx, element in enumerate(collection_details['elements'], 1):
            elem_name = element['element_identifier']
            elem_type = element['element_type']

            print(f"\n{idx}. Element: {elem_name}")
            print(f"   Type: {elem_type}")

            if elem_type == 'hda':
                dataset_id = element['object']['id']
                dataset_name = element['object'].get('name', 'N/A')
                dataset_tags = element['object'].get('tags', [])

                print(f"   Dataset Name: {dataset_name}")
                print(f"   Dataset ID: {dataset_id}")
                print(f"   Current Tags: {dataset_tags}")

        break
else:
    print("Collection #260 not found!")
