#!/usr/bin/env python3
"""
Extract official gene ID mapping from NCBI feature table
"""

import pandas as pd
import re

print("="*80)
print("EXTRACTING OFFICIAL NCBI GENE MAPPING")
print("="*80)

# Read feature table
print("\nReading v3 feature table...")
df = pd.read_csv('v3_feature_table.txt', sep='\t', low_memory=False)
# Remove # from column name if present
df.columns = [col.lstrip('# ') for col in df.columns]
print(f"  Total rows: {len(df)}")

# Filter to gene features
genes = df[df['feature'] == 'gene'].copy()
print(f"  Gene features: {len(genes)}")

# Extract locus_tag and old_locus_tag
print("\nExtracting mappings...")
mapping_v3_to_v2 = {}
mapping_v2_to_v3 = {}

for idx, row in genes.iterrows():
    v3_locus = row['locus_tag']
    attributes = row['attributes'] if pd.notna(row['attributes']) else ''

    # Extract old_locus_tag
    match = re.search(r'old_locus_tag=([^;,\s]+)', attributes)
    if match:
        v2_locus = match.group(1)
        mapping_v3_to_v2[v3_locus] = v2_locus
        mapping_v2_to_v3[v2_locus] = v3_locus

print(f"  Mapped genes: {len(mapping_v3_to_v2)}")

# Show sample mappings
print("\n" + "-"*80)
print("Sample mappings (v2 → v3):")
print("-"*80)
for i, (v2, v3) in enumerate(list(mapping_v2_to_v3.items())[:10]):
    print(f"  {v2} → {v3}")

# Save mapping files
print("\nSaving mapping files...")

# v2 to v3
with open('official_mapping_v2_to_v3.tsv', 'w') as f:
    f.write("Gene_ID_v2\tGene_ID_v3\n")
    for v2, v3 in sorted(mapping_v2_to_v3.items()):
        f.write(f"{v2}\t{v3}\n")

# v3 to v2
with open('official_mapping_v3_to_v2.tsv', 'w') as f:
    f.write("Gene_ID_v3\tGene_ID_v2\n")
    for v3, v2 in sorted(mapping_v3_to_v2.items()):
        f.write(f"{v3}\t{v2}\n")

print(f"✓ Saved official_mapping_v2_to_v3.tsv")
print(f"✓ Saved official_mapping_v3_to_v2.tsv")

# Test with our known genes
print("\n" + "="*80)
print("TESTING WITH KNOWN GENES")
print("="*80)

test_genes_v2 = ['B9J08_001458', 'B9J08_004451', 'B9J08_000592', 'B9J08_005317']
test_genes_v3 = ['B9J08_01458', 'B9J08_04451', 'B9J08_00592', 'B9J08_05317']

print("\nTesting v2 → v3 mapping:")
for v2 in test_genes_v2:
    v3_official = mapping_v2_to_v3.get(v2, 'NOT FOUND')
    v3_my_guess = 'B9J08_' + v2.split('_')[1].lstrip('0').zfill(5)
    print(f"  {v2}")
    print(f"    Official:  {v3_official}")
    print(f"    My guess:  {v3_my_guess}")
    print(f"    Match:     {'✓' if v3_official == v3_my_guess else '✗'}")

print("\nTesting v3 → v2 mapping:")
for v3 in test_genes_v3:
    v2_official = mapping_v3_to_v2.get(v3, 'NOT FOUND')
    print(f"  {v3} → {v2_official}")
