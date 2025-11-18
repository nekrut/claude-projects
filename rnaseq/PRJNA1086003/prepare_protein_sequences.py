#!/usr/bin/env python3
"""
Prepare protein sequences for DEGs from paper and our analysis
in both v2 and v3 annotation formats
"""

import pandas as pd
import numpy as np
from Bio import Entrez, SeqIO
import time
import requests

# Set email for Entrez
Entrez.email = "your_email@example.com"

# Thresholds
LFC_THRESHOLD = 1.0
PADJ_THRESHOLD = 0.01

def normalize_gene_id_v2_to_v3(gene_id):
    """Convert v2 (6-digit) to v3 (5-digit)"""
    if not isinstance(gene_id, str):
        return gene_id
    parts = gene_id.split('_')
    if len(parts) == 2 and parts[0] == 'B9J08':
        numeric = parts[1].lstrip('0') or '0'
        return f"B9J08_{numeric.zfill(5)}"
    return gene_id

def normalize_gene_id_v3_to_v2(gene_id):
    """Convert v3 (5-digit) to v2 (6-digit)"""
    if not isinstance(gene_id, str):
        return gene_id
    parts = gene_id.split('_')
    if len(parts) == 2 and parts[0] == 'B9J08':
        numeric = parts[1]
        return f"B9J08_{numeric.zfill(6)}"
    return gene_id

# Load paper's DEGs
print("Loading paper's DEGs...")
paper_vitro_raw = pd.read_excel("41467_2024_53588_MOESM3_ESM.xlsx")
paper_vivo_raw = pd.read_excel("41467_2024_53588_MOESM4_ESM.xlsx")

paper_vitro = paper_vitro_raw.iloc[2:].copy()
paper_vitro.columns = ['Gene_ID_v2', 'LFC', 'FDR', 'Gene_name', 'Description']
paper_vitro['LFC'] = pd.to_numeric(paper_vitro['LFC'], errors='coerce')
paper_vitro = paper_vitro.dropna(subset=['LFC'])
paper_vitro['Gene_ID_v3'] = paper_vitro['Gene_ID_v2'].apply(normalize_gene_id_v2_to_v3)

paper_vivo = paper_vivo_raw.iloc[2:].copy()
paper_vivo.columns = ['Gene_ID_v2', 'LFC', 'FDR', 'Gene_name', 'Description']
paper_vivo['LFC'] = pd.to_numeric(paper_vivo['LFC'], errors='coerce')
paper_vivo = paper_vivo.dropna(subset=['LFC'])
paper_vivo['Gene_ID_v3'] = paper_vivo['Gene_ID_v2'].apply(normalize_gene_id_v2_to_v3)

print(f"  Paper in vitro DEGs: {len(paper_vitro)}")
print(f"  Paper in vivo DEGs: {len(paper_vivo)}")

# Load our DEGs and filter
print("\nLoading our DEGs...")
our_vitro = pd.read_csv("deseq2_in_vitro_results.tsv", sep='\t', header=None,
                        names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])
our_vivo = pd.read_csv("deseq2_in_vivo_results.tsv", sep='\t', header=None,
                       names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])

# Filter for significant DEGs
our_vitro_sig = our_vitro[
    (our_vitro['padj'] < PADJ_THRESHOLD) &
    (np.abs(our_vitro['log2FoldChange']) >= LFC_THRESHOLD)
].copy()
our_vitro_sig['Gene_ID_v3'] = our_vitro_sig['GeneID']
our_vitro_sig['Gene_ID_v2'] = our_vitro_sig['GeneID'].apply(normalize_gene_id_v3_to_v2)

our_vivo_sig = our_vivo[
    (our_vivo['padj'] < PADJ_THRESHOLD) &
    (np.abs(our_vivo['log2FoldChange']) >= LFC_THRESHOLD)
].copy()
our_vivo_sig['Gene_ID_v3'] = our_vivo_sig['GeneID']
our_vivo_sig['Gene_ID_v2'] = our_vivo_sig['GeneID'].apply(normalize_gene_id_v3_to_v2)

print(f"  Our in vitro DEGs: {len(our_vitro_sig)}")
print(f"  Our in vivo DEGs: {len(our_vivo_sig)}")

# Save gene lists
print("\nSaving gene lists...")
paper_vitro[['Gene_ID_v2', 'Gene_ID_v3', 'LFC']].to_csv('paper_vitro_degs.tsv', sep='\t', index=False)
paper_vivo[['Gene_ID_v2', 'Gene_ID_v3', 'LFC']].to_csv('paper_vivo_degs.tsv', sep='\t', index=False)
our_vitro_sig[['Gene_ID_v2', 'Gene_ID_v3', 'log2FoldChange']].to_csv('our_vitro_degs.tsv', sep='\t', index=False)
our_vivo_sig[['Gene_ID_v2', 'Gene_ID_v3', 'log2FoldChange']].to_csv('our_vivo_degs.tsv', sep='\t', index=False)

print("\n✓ Gene lists saved:")
print("  - paper_vitro_degs.tsv")
print("  - paper_vivo_degs.tsv")
print("  - our_vitro_degs.tsv")
print("  - our_vivo_degs.tsv")

# Now we need to download protein sequences from NCBI
# We'll use the NCBI datasets API for this
print("\nProtein sequences will be extracted from NCBI annotations...")
print("Next: Run download_protein_sequences.py")
