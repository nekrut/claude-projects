#!/usr/bin/env python3
"""
Script to explore Galaxy history and find collection #402
"""

from bioblend.galaxy import GalaxyInstance

# Galaxy credentials from script.md
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"

# Connect to Galaxy instance
gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

# Get the history ID from the URL
# URL format: https://usegalaxy.org/u/cartman/h/prjna904261
# We need to get the actual history ID

# First, list all histories to find the one named 'prjna904261'
print("Fetching histories...")
histories = gi.histories.get_histories()

print(f"\nFound {len(histories)} histories")
for hist in histories:
    print(f"  - {hist['name']} (ID: {hist['id']})")
    if 'prjna904261' in hist['name'].lower():
        print(f"    ^ This looks like our target history!")
        history_id = hist['id']
        break
else:
    # If not found by name, try to get it by the slug
    print("\nTrying to get history by name 'prjna904261'...")
    try:
        # Try searching for it
        for hist in histories:
            history_id = hist['id']
            break
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

print(f"\nUsing history ID: {history_id}")

# Get all dataset collections in this history
print("\nFetching dataset collections in history...")
collections = gi.histories.show_matching_datasets(history_id=history_id)

print(f"Found {len(collections)} items in history")

# Now let's specifically look for collections
print("\nLooking for dataset collections...")
history_contents = gi.histories.show_history(history_id=history_id, contents=True)

# Filter for collections
collection_items = [item for item in history_contents if item.get('history_content_type') == 'dataset_collection']

print(f"\nFound {len(collection_items)} collections:")
for item in collection_items:
    hid = item.get('hid', 'N/A')
    name = item.get('name', 'N/A')
    collection_type = item.get('collection_type', 'N/A')
    print(f"  Collection #{hid}: {name} (type: {collection_type}, ID: {item.get('id')})")

    if hid == 402:
        print(f"\n*** FOUND COLLECTION #402! ***")
        print(f"Name: {name}")
        print(f"ID: {item.get('id')}")
        print(f"Type: {collection_type}")
