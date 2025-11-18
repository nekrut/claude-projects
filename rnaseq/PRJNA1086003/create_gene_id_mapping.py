#!/usr/bin/env python3
"""
Create gene ID mapping between annotation versions based on genomic coordinates
Since v2 uses 6-digit IDs and v3 uses 5-digit IDs, we need to map them
"""

import pandas as pd

# For now, let's create a simple normalization function and apply it to paper's data
def normalize_gene_id_v2_to_v3(gene_id_v2):
    """
    Convert v2 6-digit gene IDs to v3 5-digit gene IDs
    B9J08_001458 -> B9J08_01458
    B9J08_004112 -> B9J08_04112
    """
    if not isinstance(gene_id_v2, str):
        return gene_id_v2

    parts = gene_id_v2.split('_')
    if len(parts) == 2 and parts[0] == 'B9J08':
        # Remove leading zeros but keep at least the number itself
        numeric = parts[1].lstrip('0') or '0'
        # Pad to 5 digits
        return f"B9J08_{numeric.zfill(5)}"
    return gene_id_v2

# Load paper's supplementary data
print("Loading paper's in vitro data...")
paper_vitro = pd.read_excel("41467_2024_53588_MOESM3_ESM.xlsx")

# Skip header rows and set proper column names
paper_vitro_data = paper_vitro.iloc[2:].copy()
paper_vitro_data.columns = ['Gene_ID_v2', 'LFC', 'FDR', 'Gene_name', 'Description']

# Convert numeric columns
paper_vitro_data['LFC'] = pd.to_numeric(paper_vitro_data['LFC'], errors='coerce')
paper_vitro_data['FDR'] = pd.to_numeric(paper_vitro_data['FDR'], errors='coerce')

# Create v3 gene IDs
paper_vitro_data['Gene_ID_v3'] = paper_vitro_data['Gene_ID_v2'].apply(normalize_gene_id_v2_to_v3)

# Save mapping
mapping = paper_vitro_data[['Gene_ID_v2', 'Gene_ID_v3', 'Gene_name']].drop_duplicates()
mapping.to_csv('gene_id_mapping_v2_to_v3.tsv', sep='\t', index=False)

print(f"✓ Created mapping for {len(mapping)} genes")
print(f"\nFirst 10 mappings:")
print(mapping.head(10).to_string(index=False))

# Check key genes
key_genes_v2 = ['B9J08_001458', 'B9J08_004112', 'B9J08_004109']
print(f"\nKey gene mappings:")
for gene_v2 in key_genes_v2:
    gene_v3 = normalize_gene_id_v2_to_v3(gene_v2)
    print(f"  {gene_v2} -> {gene_v3}")
