#!/usr/bin/env python3
"""
Check if DESeq2 results were created and find the appropriate tool parameters.
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

    # Get recent datasets to find DESeq2 outputs
    history_contents = gi.histories.show_history(history_id, contents=True, deleted=False)

    print(f"\nRecent datasets in history (showing last 20):")
    print(f"{'HID':<6} {'State':<10} {'Name':<60}")
    print("=" * 76)

    # Sort by HID descending to show most recent first
    sorted_contents = sorted(history_contents, key=lambda x: x.get('hid', 0), reverse=True)

    for item in sorted_contents[:20]:
        hid = item.get('hid', 'N/A')
        state = item.get('state', 'unknown')
        name = item.get('name', 'Unnamed')[:60]
        item_type = item.get('history_content_type', 'dataset')

        if 'deseq' in name.lower() or 'DESeq' in name:
            print(f"#{hid:<5} {state:<10} {name} ({item_type})")

    # Also check for DESeq2 tool information
    print(f"\n\nSearching for DESeq2 tool...")
    tools = gi.tools.get_tools(name="deseq2")
    if tools:
        print(f"Found {len(tools)} DESeq2 tool(s):")
        for tool in tools[:3]:
            print(f"  - {tool['name']} ({tool['id']})")

            # Get tool details
            try:
                tool_details = gi.tools.show_tool(tool['id'])
                print(f"    Version: {tool_details.get('version', 'N/A')}")
            except:
                pass
    else:
        print("No DESeq2 tools found")

    # List all DESeq2-related datasets
    deseq_datasets = [item for item in history_contents if 'deseq' in item.get('name', '').lower()]
    if deseq_datasets:
        print(f"\n\nAll DESeq2-related datasets found: {len(deseq_datasets)}")
        for ds in deseq_datasets[-10:]:  # Show last 10
            print(f"  #{ds.get('hid')}: {ds.get('name')} - {ds.get('state')}")

if __name__ == "__main__":
    main()
