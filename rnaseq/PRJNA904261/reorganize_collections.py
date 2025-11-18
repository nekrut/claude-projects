#!/usr/bin/env python3
"""
Script to reorganize Galaxy collection #260 into condition-specific collections
for differential expression analysis with DESeq2
"""

import requests
import json

# Galaxy connection info
API_KEY = "YOUR_GALAXY_API_KEY"
GALAXY_URL = "https://usegalaxy.org"
HISTORY_ID = "bbd44e69cb8906b5713a37cc4e6846ea"
COLLECTION_ID = "50490a95897034a8"

headers = {"x-api-key": API_KEY}

# Sample to condition mapping
SAMPLE_MAPPING = {
    "SRR22376030": {"condition": "AR0387_blood_WT", "replicate": "A", "name": "AR0387_A"},
    "SRR22376029": {"condition": "AR0387_blood_WT", "replicate": "B", "name": "AR0387_B"},
    "SRR22376032": {"condition": "AR0382_burn_WT", "replicate": "A", "name": "AR0382_A"},
    "SRR22376031": {"condition": "AR0382_burn_WT", "replicate": "B", "name": "AR0382_B"},
    "SRR22376028": {"condition": "AR0382_tnSWI1_KO", "replicate": "A", "name": "AR0382_tnSWI1_A"},
    "SRR22376027": {"condition": "AR0382_tnSWI1_KO", "replicate": "B", "name": "AR0382_tnSWI1_B"},
}

CONDITIONS = {
    "AR0387_blood_WT": ["SRR22376030", "SRR22376029"],
    "AR0382_burn_WT": ["SRR22376032", "SRR22376031"],
    "AR0382_tnSWI1_KO": ["SRR22376028", "SRR22376027"],
}


def get_collection_elements():
    """Get all elements from the original collection"""
    url = f"{GALAXY_URL}/api/dataset_collections/{COLLECTION_ID}"
    response = requests.get(url, headers=headers)
    collection_info = response.json()
    return collection_info.get('elements', [])


def get_element_details(element):
    """Extract dataset ID from collection element"""
    return {
        'id': element['object']['id'],
        'identifier': element['element_identifier'],
        'name': element['object']['name']
    }


def create_collection(name, elements, collection_type="list"):
    """Create a new collection in the history"""
    url = f"{GALAXY_URL}/api/histories/{HISTORY_ID}/contents/dataset_collections"

    # Format elements for API
    formatted_elements = []
    for element in elements:
        formatted_elements.append({
            "name": element['identifier'],
            "src": "hda",
            "id": element['id']
        })

    payload = {
        "collection_type": collection_type,
        "name": name,
        "element_identifiers": formatted_elements,
        "hide_source_items": False
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in [200, 201]:
        print(f"✓ Created collection: {name}")
        return response.json()
    else:
        print(f"✗ Failed to create collection: {name}")
        print(f"  Status code: {response.status_code}")
        print(f"  Response: {response.text}")
        return None


def main():
    print("=" * 60)
    print("Reorganizing Galaxy Collection for DESeq2 Analysis")
    print("=" * 60)

    # Get original collection elements
    print("\n1. Fetching original collection elements...")
    elements = get_collection_elements()

    # Create mapping of SRR to element details
    element_map = {}
    for element in elements:
        details = get_element_details(element)
        element_map[details['identifier']] = details
        print(f"   Found: {details['identifier']} → {SAMPLE_MAPPING[details['identifier']]['name']}")

    # Create condition-specific collections
    print("\n2. Creating condition-specific collections...")
    created_collections = {}

    for condition_name, srr_list in CONDITIONS.items():
        print(f"\n   Creating: {condition_name}")

        # Gather elements for this condition
        condition_elements = []
        for srr in srr_list:
            if srr in element_map:
                element = element_map[srr]
                sample_info = SAMPLE_MAPPING[srr]
                # Rename with meaningful names
                element['identifier'] = sample_info['name']
                condition_elements.append(element)
                print(f"     - {srr} ({sample_info['name']}, replicate {sample_info['replicate']})")

        # Create the collection
        result = create_collection(condition_name, condition_elements)
        if result:
            created_collections[condition_name] = result

    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Original collection: Counts Table (#{COLLECTION_ID})")
    print(f"Total samples: {len(element_map)}")
    print(f"\nNew collections created: {len(created_collections)}")
    for name, info in created_collections.items():
        print(f"  - {name} (HID: {info.get('hid', 'N/A')})")

    print("\n" + "=" * 60)
    print("Next Steps for DESeq2 Analysis")
    print("=" * 60)
    print("1. In Galaxy, open the DESeq2 tool")
    print("2. For Factor 1 (Condition):")
    print("   - Add 3 factor levels (one for each condition)")
    print("   - Assign the corresponding collections to each level")
    print("\nExample comparisons:")
    print("  • AR0382_tnSWI1_KO vs AR0382_burn_WT (SWI1 knockout effect)")
    print("  • AR0387_blood_WT vs AR0382_burn_WT (strain differences)")
    print("  • AR0382_tnSWI1_KO vs AR0387_blood_WT (mutant vs blood WT)")


if __name__ == "__main__":
    main()
