#!/usr/bin/env python3
"""
Run DESeq2 the CORRECT way using separate collections for each factor level.
"""

from bioblend.galaxy import GalaxyInstance

# Galaxy connection details
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "prjna1086003"

def run_deseq2_with_separate_collections(gi, history_id, collection_82_id, collection_87_id,
                                         experiment_name):
    """
    Run DESeq2 with separate collections for each strain.

    Factor level 1: "87" (AR0387) → collection_87_id
    Factor level 2: "82" (AR0382) → collection_82_id
    """

    print(f"\n{'='*70}")
    print(f"Running DESeq2 for {experiment_name}")
    print(f"{'='*70}")
    print(f"Factor level '87' (AR0387): Collection #{collection_87_id}")
    print(f"Factor level '82' (AR0382): Collection #{collection_82_id}")

    deseq2_tool_id = "toolshed.g2.bx.psu.edu/repos/iuc/deseq2/deseq2/2.11.40.8+galaxy0"

    # DESeq2 parameters using collections mode
    deseq2_params = {
        'select_data': {
            'how': 'collection_paired',  # Use paired collections mode
            'collection_mode': {
                'collection_mode_selector': 'datasets',
                'factorName': 'strain',
                'factors': [
                    {
                        'factorLevel': '87',
                        'countsFile': {'src': 'hdca', 'id': collection_87_id}
                    },
                    {
                        'factorLevel': '82',
                        'countsFile': {'src': 'hdca', 'id': collection_82_id}
                    }
                ]
            }
        },
        'tximport': {
            'txtype': 'none'
        },
        'advanced_options': {
            'use_beta_priors': False,
            'alpha': 0.01,  # FDR threshold
            'lfcThreshold': 0  # Will filter for |LFC| >= 1 later
        },
        'output_options': {
            'output_normalized': True,
            'output_rlog': False
        }
    }

    try:
        print(f"\nSubmitting DESeq2 job...")
        result = gi.tools.run_tool(
            history_id=history_id,
            tool_id=deseq2_tool_id,
            tool_inputs=deseq2_params
        )
        print(f"✓ DESeq2 job submitted!")
        print(f"  Outputs: {len(result.get('outputs', []))}")
        for output in result.get('outputs', []):
            print(f"    - {output.get('name')}")
        return result
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    # Connect to Galaxy
    gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

    # Get history
    all_histories = gi.histories.get_histories()
    history = None
    for h in all_histories:
        if HISTORY_NAME.lower() in h['name'].lower():
            history = h
            break

    if not history:
        print(f"Error: History '{HISTORY_NAME}' not found")
        return

    history_id = history['id']
    print(f"Found history: {history['name']}")

    # Get all collections
    history_contents = gi.histories.show_history(history_id, contents=True)

    collections = {}
    for item in history_contents:
        if item.get('history_content_type') == 'dataset_collection':
            hid = item.get('hid')
            name = item.get('name')
            collections[hid] = {'id': item.get('id'), 'name': name}

    # Find the sub-collections we created
    in_vitro_82 = collections.get(641)
    in_vitro_87 = collections.get(645)
    in_vivo_82 = collections.get(651)
    in_vivo_87 = collections.get(656)

    print(f"\nFound collections:")
    print(f"  In vitro AR0382 (#641): {in_vitro_82['name'] if in_vitro_82 else 'NOT FOUND'}")
    print(f"  In vitro AR0387 (#645): {in_vitro_87['name'] if in_vitro_87 else 'NOT FOUND'}")
    print(f"  In vivo AR0382 (#651): {in_vivo_82['name'] if in_vivo_82 else 'NOT FOUND'}")
    print(f"  In vivo AR0387 (#656): {in_vivo_87['name'] if in_vivo_87 else 'NOT FOUND'}")

    if not all([in_vitro_82, in_vitro_87, in_vivo_82, in_vivo_87]):
        print("\n✗ Error: Not all required collections found!")
        return

    # Run DESeq2 for in vitro
    in_vitro_result = run_deseq2_with_separate_collections(
        gi,
        history_id,
        in_vitro_82['id'],  # Collection #641 (AR0382)
        in_vitro_87['id'],  # Collection #645 (AR0387)
        "in vitro experiment"
    )

    # Run DESeq2 for in vivo
    in_vivo_result = run_deseq2_with_separate_collections(
        gi,
        history_id,
        in_vivo_82['id'],   # Collection #651 (AR0382)
        in_vivo_87['id'],   # Collection #656 (AR0387)
        "in vivo experiment"
    )

    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"In vitro DESeq2: {'✓ Success' if in_vitro_result else '✗ Failed'}")
    print(f"In vivo DESeq2: {'✓ Success' if in_vivo_result else '✗ Failed'}")
    print(f"\nExpected from paper:")
    print(f"  In vitro: ~76 DEGs (LFC ≥ |1|, FDR < 0.01)")
    print(f"  In vivo: ~259 DEGs (LFC ≥ |1|, FDR < 0.01)")
    print(f"\nComparing strain 82 (AR0382, aggregative) vs 87 (AR0387, non-aggregative)")
    print(f"\nView results at: https://usegalaxy.org/u/cartman/h/prjna1086003")

if __name__ == "__main__":
    main()
