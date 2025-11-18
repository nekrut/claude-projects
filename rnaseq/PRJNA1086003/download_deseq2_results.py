#!/usr/bin/env python3
"""
Download DESeq2 results from Galaxy for comparison with paper
"""

from bioblend.galaxy import GalaxyInstance

# Galaxy connection
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "PRJNA1086003"

# Dataset numbers in history (not IDs)
DESEQ2_IN_VITRO_HID = 671
DESEQ2_IN_VIVO_HID = 673

def main():
    # Connect to Galaxy
    gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

    # Get history ID
    histories = gi.histories.get_histories(name=HISTORY_NAME)
    if not histories:
        print(f"Error: History '{HISTORY_NAME}' not found")
        return

    history_id = histories[0]['id']
    print(f"Found history: {HISTORY_NAME} (ID: {history_id})")

    # Get all datasets in the history
    print("\nRetrieving datasets from history...")
    datasets = gi.histories.show_history(history_id, contents=True)

    # Find datasets by their history item number (hid)
    in_vitro_dataset = None
    in_vivo_dataset = None

    for dataset in datasets:
        if dataset['hid'] == DESEQ2_IN_VITRO_HID:
            in_vitro_dataset = dataset
            print(f"Found in vitro dataset #{DESEQ2_IN_VITRO_HID}: {dataset['name']}")
        elif dataset['hid'] == DESEQ2_IN_VIVO_HID:
            in_vivo_dataset = dataset
            print(f"Found in vivo dataset #{DESEQ2_IN_VIVO_HID}: {dataset['name']}")

    # Download in vitro results
    if in_vitro_dataset:
        print(f"\nDownloading in vitro DESeq2 results...")
        try:
            gi.datasets.download_dataset(
                dataset_id=in_vitro_dataset['id'],
                file_path="deseq2_in_vitro_results.tsv",
                use_default_filename=False
            )
            print("✓ Saved to: deseq2_in_vitro_results.tsv")
        except Exception as e:
            print(f"Error downloading in vitro dataset: {e}")
    else:
        print(f"Error: Could not find dataset #{DESEQ2_IN_VITRO_HID}")

    # Download in vivo results
    if in_vivo_dataset:
        print(f"\nDownloading in vivo DESeq2 results...")
        try:
            gi.datasets.download_dataset(
                dataset_id=in_vivo_dataset['id'],
                file_path="deseq2_in_vivo_results.tsv",
                use_default_filename=False
            )
            print("✓ Saved to: deseq2_in_vivo_results.tsv")
        except Exception as e:
            print(f"Error downloading in vivo dataset: {e}")
    else:
        print(f"Error: Could not find dataset #{DESEQ2_IN_VIVO_HID}")

    print("\nDownload complete!")

if __name__ == "__main__":
    main()
