#!/usr/bin/env python3
"""
Run DESeq2 using group tags in Galaxy collections.
This uses Galaxy's built-in support for analyzing collections based on group tags.
"""

from bioblend.galaxy import GalaxyInstance
import json

# Galaxy connection details
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "prjna1086003"

def run_deseq2_with_group_tags(gi, history_id, collection_id, collection_name, experiment_type):
    """
    Run DESeq2 using the group tags we added to samples.

    Strategy: Create sub-collections based on strain (AR0382 vs AR0387)
    and then run DESeq2 comparing them.
    """

    print(f"\n{'='*70}")
    print(f"Setting up DESeq2 for {experiment_type} experiment")
    print(f"Collection: {collection_name}")
    print(f"{'='*70}")

    # Get collection details
    collection_details = gi.histories.show_dataset_collection(history_id, collection_id)
    elements = collection_details.get('elements', [])

    print(f"\nCollection has {len(elements)} elements")

    # Organize elements by strain based on tags or sample info
    ar0382_elements = []
    ar0387_elements = []

    for elem in elements:
        elem_id = elem.get('element_identifier', '')
        dataset_id = elem['object']['id']

        # Get dataset tags
        try:
            dataset_info = gi.datasets.show_dataset(dataset_id)
            tags = dataset_info.get('tags', [])

            # Determine strain from tags or name
            is_ar0382 = False
            is_ar0387 = False

            for tag in tags:
                if 'AR0382' in tag or '82' in tag:
                    is_ar0382 = True
                elif 'AR0387' in tag or '87' in tag:
                    is_ar0387 = True

            # If no tags worked, use element identifier
            if not is_ar0382 and not is_ar0387:
                if '82' in elem_id and '87' not in elem_id:
                    is_ar0382 = True
                elif '87' in elem_id:
                    is_ar0387 = True

            if is_ar0382:
                ar0382_elements.append(elem)
            elif is_ar0387:
                ar0387_elements.append(elem)
            else:
                print(f"  Warning: Could not determine strain for {elem_id}")

        except Exception as e:
            print(f"  Error processing {elem_id}: {e}")

    print(f"\nAR0382 samples: {len(ar0382_elements)}")
    for elem in ar0382_elements:
        print(f"  - {elem.get('element_identifier')}")

    print(f"\nAR0387 samples: {len(ar0387_elements)}")
    for elem in ar0387_elements:
        print(f"  - {elem.get('element_identifier')}")

    # Create sub-collections for each strain
    print(f"\nCreating sub-collections for each strain...")

    # Create AR0382 collection
    try:
        ar0382_collection = gi.histories.create_dataset_collection(
            history_id=history_id,
            collection_description={
                'collection_type': 'list',
                'name': f'{collection_name}_AR0382',
                'element_identifiers': [
                    {
                        'id': elem['object']['id'],
                        'name': elem['element_identifier'],
                        'src': 'hda'
                    }
                    for elem in ar0382_elements
                ]
            }
        )
        print(f"✓ Created AR0382 sub-collection (#{ar0382_collection.get('hid')})")
        ar0382_coll_id = ar0382_collection['id']
    except Exception as e:
        print(f"✗ Error creating AR0382 collection: {e}")
        return None

    # Create AR0387 collection
    try:
        ar0387_collection = gi.histories.create_dataset_collection(
            history_id=history_id,
            collection_description={
                'collection_type': 'list',
                'name': f'{collection_name}_AR0387',
                'element_identifiers': [
                    {
                        'id': elem['object']['id'],
                        'name': elem['element_identifier'],
                        'src': 'hda'
                    }
                    for elem in ar0387_elements
                ]
            }
        )
        print(f"✓ Created AR0387 sub-collection (#{ar0387_collection.get('hid')})")
        ar0387_coll_id = ar0387_collection['id']
    except Exception as e:
        print(f"✗ Error creating AR0387 collection: {e}")
        return None

    # Now run DESeq2 with separate collections
    print(f"\nRunning DESeq2 comparing AR0382 vs AR0387...")

    deseq2_tool_id = "toolshed.g2.bx.psu.edu/repos/iuc/deseq2/deseq2/2.11.40.8+galaxy0"

    # DESeq2 parameters with separate collections
    deseq2_params = {
        'select_data': {
            'how': 'collections',
            'rep_factorName': ['strain'],
            'rep_factorLevel': [
                {
                    'factorLevel': 'AR0382',
                    'countsFile': [{'src': 'hdca', 'id': ar0382_coll_id}]
                },
                {
                    'factorLevel': 'AR0387',
                    'countsFile': [{'src': 'hdca', 'id': ar0387_coll_id}]
                }
            ],
            'tximport': {'txtype': 'none'}
        },
        'output_options': {
            'output_normalized': True,
            'output_rlog': False
        },
        'advanced_options': {
            'use_beta_priors': False,
            'alpha': 0.01,  # FDR < 0.01 from paper
            'lfcThreshold': 0  # We'll filter for LFC >= 1 in post-processing
        }
    }

    try:
        result = gi.tools.run_tool(
            history_id=history_id,
            tool_id=deseq2_tool_id,
            tool_inputs=deseq2_params
        )
        print(f"✓ DESeq2 job submitted!")
        print(f"  Outputs created: {len(result.get('outputs', []))}")
        for output in result.get('outputs', [])[:5]:
            print(f"    - {output.get('name', 'Unnamed')}")

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
            if 'in_vitro' in item['name'] and '_AR' not in item['name']:
                in_vitro_collection = item
            elif 'in_vivo' in item['name'] and '_AR' not in item['name']:
                in_vivo_collection = item

    if not in_vitro_collection or not in_vivo_collection:
        print("Error: Could not find both in_vitro and in_vivo collections")
        return

    print(f"\nUsing collections:")
    print(f"  In vitro: #{in_vitro_collection['hid']} - {in_vitro_collection['name']}")
    print(f"  In vivo: #{in_vivo_collection['hid']} - {in_vivo_collection['name']}")

    # Run DESeq2 for in vitro
    in_vitro_result = run_deseq2_with_group_tags(
        gi,
        history_id,
        in_vitro_collection['id'],
        in_vitro_collection['name'],
        "in vitro"
    )

    # Run DESeq2 for in vivo
    in_vivo_result = run_deseq2_with_group_tags(
        gi,
        history_id,
        in_vivo_collection['id'],
        in_vivo_collection['name'],
        "in vivo"
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
