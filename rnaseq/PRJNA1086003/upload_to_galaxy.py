#!/usr/bin/env python3
"""
Upload FASTA files to Galaxy history
"""

from bioblend.galaxy import GalaxyInstance

# Galaxy connection
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "PRJNA1086003"

# Files to upload
files_to_upload = [
    # IN VITRO
    ("paper_vitro_degs_v2.fasta", "Paper in_vitro DEGs (v2 annotation)", "fasta"),
    ("paper_vitro_degs_v3.fasta", "Paper in_vitro DEGs (v3 annotation)", "fasta"),
    ("our_vitro_degs_v2.fasta", "Our in_vitro DEGs (v2 annotation)", "fasta"),
    ("our_vitro_degs_v3.fasta", "Our in_vitro DEGs (v3 annotation)", "fasta"),
    # IN VIVO
    ("paper_vivo_degs_v2.fasta", "Paper in_vivo DEGs (v2 annotation)", "fasta"),
    ("paper_vivo_degs_v3.fasta", "Paper in_vivo DEGs (v3 annotation)", "fasta"),
    ("our_vivo_degs_v2.fasta", "Our in_vivo DEGs (v2 annotation)", "fasta"),
    ("our_vivo_degs_v3.fasta", "Our in_vivo DEGs (v3 annotation)", "fasta"),
]

def main():
    print("="*80)
    print("UPLOADING FASTA FILES TO GALAXY")
    print("="*80)

    # Connect to Galaxy
    gi = GalaxyInstance(url=GALAXY_URL, key=API_KEY)

    # Get history
    histories = gi.histories.get_histories(name=HISTORY_NAME)
    if not histories:
        print(f"Error: History '{HISTORY_NAME}' not found")
        return

    history_id = histories[0]['id']
    print(f"\nFound history: {HISTORY_NAME} (ID: {history_id})")

    # Upload each file
    print(f"\nUploading {len(files_to_upload)} files...")
    uploaded = []

    for file_path, name, file_type in files_to_upload:
        print(f"\n  Uploading: {name}...")
        print(f"    File: {file_path}")

        try:
            result = gi.tools.upload_file(
                path=file_path,
                history_id=history_id,
                file_name=name,
                file_type=file_type
            )

            # Get dataset info
            if result and 'outputs' in result:
                dataset_id = result['outputs'][0]['id']
                print(f"    ✓ Uploaded as dataset #{result['outputs'][0]['hid']}")
                uploaded.append((name, dataset_id))
            else:
                print(f"    ✗ Upload failed")

        except Exception as e:
            print(f"    ✗ Error: {e}")

    print("\n" + "="*80)
    print("UPLOAD SUMMARY")
    print("="*80)
    print(f"\n✓ Successfully uploaded {len(uploaded)} files to Galaxy history")
    print(f"\nHistory URL: https://usegalaxy.org/u/cartman/h/prjna1086003")

    print("\nUploaded datasets:")
    for name, dataset_id in uploaded:
        print(f"  - {name}")

if __name__ == "__main__":
    main()
