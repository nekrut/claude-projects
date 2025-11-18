#!/usr/bin/env python3
"""
Rebuild DEG lists with correct NCBI mappings
"""

import pandas as pd

print("="*80)
print("REBUILDING DEG LISTS WITH CORRECT MAPPINGS")
print("="*80)

# Load official mappings
print("\nLoading official mappings...")
v2_to_v3 = pd.read_csv('official_mapping_v2_to_v3.tsv', sep='\t')
v3_to_v2 = pd.read_csv('official_mapping_v3_to_v2.tsv', sep='\t')

print(f"  v2→v3 mappings: {len(v2_to_v3)}")
print(f"  v3→v2 mappings: {len(v3_to_v2)}")

# Create lookup dicts
v2_to_v3_dict = dict(zip(v2_to_v3['Gene_ID_v2'], v2_to_v3['Gene_ID_v3']))
v3_to_v2_dict = dict(zip(v3_to_v2['Gene_ID_v3'], v3_to_v2['Gene_ID_v2']))

# Load paper's DEG lists (they used v2 annotation)
print("\n" + "-"*80)
print("Loading paper's supplemental data...")
print("-"*80)

# In vitro
paper_vitro_raw = pd.read_excel('41467_2024_53588_MOESM3_ESM.xlsx')
paper_vitro = paper_vitro_raw.iloc[2:].copy()
paper_vitro.columns = ['Gene_ID', 'Log2FC', 'FDR', 'Gene_name', 'Description']
paper_vitro['Log2FC'] = pd.to_numeric(paper_vitro['Log2FC'], errors='coerce')
paper_vitro = paper_vitro.dropna(subset=['Log2FC'])

# In vivo
paper_vivo_raw = pd.read_excel('41467_2024_53588_MOESM4_ESM.xlsx')
paper_vivo = paper_vivo_raw.iloc[2:].copy()
paper_vivo.columns = ['Gene_ID', 'Log2FC', 'FDR', 'Gene_name', 'Description']
paper_vivo['Log2FC'] = pd.to_numeric(paper_vivo['Log2FC'], errors='coerce')
paper_vivo = paper_vivo.dropna(subset=['Log2FC'])

print(f"  Paper in_vitro DEGs: {len(paper_vitro)}")
print(f"  Paper in_vivo DEGs: {len(paper_vivo)}")

# Load our DESeq2 results (we used v3 annotation)
print("\nLoading our DESeq2 results...")
our_vitro_raw = pd.read_csv('deseq2_in_vitro_results.tsv', sep='\t', header=None,
                             names=['gene_id', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])
our_vitro = our_vitro_raw[our_vitro_raw['padj'] < 0.05].copy()

our_vivo_raw = pd.read_csv('deseq2_in_vivo_results.tsv', sep='\t', header=None,
                            names=['gene_id', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])
our_vivo = our_vivo_raw[our_vivo_raw['padj'] < 0.05].copy()

print(f"  Our in_vitro DEGs: {len(our_vitro)}")
print(f"  Our in_vivo DEGs: {len(our_vivo)}")

# Create corrected DEG lists
print("\n" + "="*80)
print("CREATING CORRECTED DEG LISTS")
print("="*80)

# 1. Paper's DEGs (v2) + map to v3
print("\n1. Paper's in_vitro DEGs (corrected)...")
paper_vitro_correct = []
for idx, row in paper_vitro.iterrows():
    gene_v2 = row['Gene_ID']
    gene_v3 = v2_to_v3_dict.get(gene_v2, 'NA')
    paper_vitro_correct.append({
        'Gene_ID_v2': gene_v2,
        'Gene_ID_v3': gene_v3,
        'log2FoldChange': row['Log2FC']
    })

paper_vitro_df = pd.DataFrame(paper_vitro_correct)
paper_vitro_df.to_csv('paper_vitro_degs_corrected.tsv', sep='\t', index=False)
print(f"   Saved: paper_vitro_degs_corrected.tsv")
print(f"   Mapped to v3: {(paper_vitro_df['Gene_ID_v3'] != 'NA').sum()}/{len(paper_vitro_df)}")

# 2. Paper's in_vivo DEGs
print("\n2. Paper's in_vivo DEGs (corrected)...")
paper_vivo_correct = []
for idx, row in paper_vivo.iterrows():
    gene_v2 = row['Gene_ID']
    gene_v3 = v2_to_v3_dict.get(gene_v2, 'NA')
    paper_vivo_correct.append({
        'Gene_ID_v2': gene_v2,
        'Gene_ID_v3': gene_v3,
        'log2FoldChange': row['Log2FC']
    })

paper_vivo_df = pd.DataFrame(paper_vivo_correct)
paper_vivo_df.to_csv('paper_vivo_degs_corrected.tsv', sep='\t', index=False)
print(f"   Saved: paper_vivo_degs_corrected.tsv")
print(f"   Mapped to v3: {(paper_vivo_df['Gene_ID_v3'] != 'NA').sum()}/{len(paper_vivo_df)}")

# 3. Our DEGs (v3) + map to v2
print("\n3. Our in_vitro DEGs (corrected)...")
our_vitro_correct = []
for idx, row in our_vitro.iterrows():
    gene_v3 = row['gene_id']
    gene_v2 = v3_to_v2_dict.get(gene_v3, 'NA')
    our_vitro_correct.append({
        'Gene_ID_v2': gene_v2,
        'Gene_ID_v3': gene_v3,
        'log2FoldChange': row['log2FoldChange']
    })

our_vitro_df = pd.DataFrame(our_vitro_correct)
our_vitro_df.to_csv('our_vitro_degs_corrected.tsv', sep='\t', index=False)
print(f"   Saved: our_vitro_degs_corrected.tsv")
print(f"   Mapped to v2: {(our_vitro_df['Gene_ID_v2'] != 'NA').sum()}/{len(our_vitro_df)}")

# 4. Our in_vivo DEGs
print("\n4. Our in_vivo DEGs (corrected)...")
our_vivo_correct = []
for idx, row in our_vivo.iterrows():
    gene_v3 = row['gene_id']
    gene_v2 = v3_to_v2_dict.get(gene_v3, 'NA')
    our_vivo_correct.append({
        'Gene_ID_v2': gene_v2,
        'Gene_ID_v3': gene_v3,
        'log2FoldChange': row['log2FoldChange']
    })

our_vivo_df = pd.DataFrame(our_vivo_correct)
our_vivo_df.to_csv('our_vivo_degs_corrected.tsv', sep='\t', index=False)
print(f"   Saved: our_vivo_degs_corrected.tsv")
print(f"   Mapped to v2: {(our_vivo_df['Gene_ID_v2'] != 'NA').sum()}/{len(our_vivo_df)}")

print("\n✓ All corrected DEG lists created!")
