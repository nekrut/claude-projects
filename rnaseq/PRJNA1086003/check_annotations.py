#!/usr/bin/env python3
"""
Download and check the gene annotation file
"""

from bioblend.galaxy import GalaxyInstance

# Galaxy connection
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "PRJNA1086003"
ANNOTATION_HID = 87

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

    # Get all datasets
    datasets = gi.histories.show_history(history_id, contents=True)

    # Find annotation dataset
    annotation_dataset = None
    for dataset in datasets:
        if dataset['hid'] == ANNOTATION_HID:
            annotation_dataset = dataset
            print(f"\nFound annotation dataset #{ANNOTATION_HID}: {dataset['name']}")
            break

    if annotation_dataset:
        print(f"\nDownloading annotation file...")
        try:
            gi.datasets.download_dataset(
                dataset_id=annotation_dataset['id'],
                file_path="gene_annotations.tsv",
                use_default_filename=False
            )
            print("✓ Saved to: gene_annotations.tsv")

            # Show first few lines
            print("\nFirst 10 lines of annotation file:")
            with open("gene_annotations.tsv", 'r') as f:
                for i, line in enumerate(f):
                    if i >= 10:
                        break
                    print(f"  {line.rstrip()}")

        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"Error: Could not find dataset #{ANNOTATION_HID}")

if __name__ == "__main__":
    main()
