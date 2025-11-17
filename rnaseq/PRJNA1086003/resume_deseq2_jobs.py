#!/usr/bin/env python3
"""
Resume paused DESeq2 jobs and check errors.
"""

from bioblend.galaxy import GalaxyInstance

# Galaxy connection details
GALAXY_URL = "https://usegalaxy.org"
API_KEY = "YOUR_GALAXY_API_KEY"
HISTORY_NAME = "prjna1086003"

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
    print(f"Found history: {history['name']} (ID: {history_id})")

    # Get all datasets
    history_contents = gi.histories.show_history(history_id, contents=True, deleted=False)

    # Find DESeq2 datasets
    deseq_datasets = [item for item in history_contents if 'deseq' in item.get('name', '').lower()]

    print(f"\nFound {len(deseq_datasets)} DESeq2-related datasets")

    # Check each dataset
    for ds in deseq_datasets:
        hid = ds.get('hid')
        name = ds.get('name')
        state = ds.get('state')
        dataset_id = ds.get('id')

        print(f"\n#{hid}: {name}")
        print(f"  State: {state}")

        if state == 'error':
            # Get error details
            try:
                dataset_info = gi.datasets.show_dataset(dataset_id)
                if 'misc_info' in dataset_info:
                    print(f"  Error info: {dataset_info.get('misc_info', 'No error info')}")
            except Exception as e:
                print(f"  Could not get error details: {e}")

        elif state == 'paused':
            # Try to resume the job
            try:
                # First, check if we can get the job info
                print(f"  Attempting to resume...")

                # Get job ID for this dataset
                job_id = ds.get('creating_job')
                if job_id:
                    print(f"  Job ID: {job_id}")

                    # Check job details
                    try:
                        job_info = gi.jobs.show_job(job_id)
                        print(f"  Job state: {job_info.get('state')}")

                        # Note: Paused jobs usually require manual intervention in Galaxy
                        # They may be waiting for user input or approval
                        print(f"  → This job requires manual action in Galaxy interface")
                    except Exception as e:
                        print(f"  Could not get job info: {e}")
                else:
                    print(f"  No job ID found")

            except Exception as e:
                print(f"  Could not resume: {e}")

    print(f"\n\n{'='*70}")
    print("Summary")
    print(f"{'='*70}")
    print(f"\nPaused jobs typically need manual action in Galaxy web interface.")
    print(f"Please visit: https://usegalaxy.org/u/cartman/h/prjna1086003")
    print(f"\nTo resume paused jobs:")
    print(f"1. Click on the paused dataset (yellow)")
    print(f"2. Look for a 'Resume' or 'Run' button")
    print(f"3. Provide any required parameters")

    # Look for the most recent results
    result_files = [ds for ds in deseq_datasets if 'result file' in ds.get('name', '').lower()]
    plot_files = [ds for ds in deseq_datasets if 'plots' in ds.get('name', '').lower()]

    print(f"\n\nDESeq2 Result files: {len(result_files)}")
    print(f"DESeq2 Plot files: {len(plot_files)}")

if __name__ == "__main__":
    main()
