#!/usr/bin/env python3
"""
Final comprehensive comparison with proper gene ID mapping
"""

import pandas as pd
import numpy as np

# Load gene ID mapping
mapping = pd.read_csv('gene_id_mapping_v2_to_v3.tsv', sep='\t')

# Load our DESeq2 results
our_vitro = pd.read_csv("deseq2_in_vitro_results.tsv", sep='\t', header=None,
                        names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])
our_vivo = pd.read_csv("deseq2_in_vivo_results.tsv", sep='\t', header=None,
                       names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])

# Load paper's data
paper_vitro_raw = pd.read_excel("41467_2024_53588_MOESM3_ESM.xlsx")
paper_vivo_raw = pd.read_excel("41467_2024_53588_MOESM4_ESM.xlsx")

# Parse paper's data (skip headers)
paper_vitro = paper_vitro_raw.iloc[2:].copy()
paper_vitro.columns = ['Gene_ID_v2', 'LFC', 'FDR', 'Gene_name', 'Description']
paper_vitro['LFC'] = pd.to_numeric(paper_vitro['LFC'], errors='coerce')
paper_vitro = paper_vitro.dropna(subset=['LFC'])

paper_vivo = paper_vivo_raw.iloc[2:].copy()
paper_vivo.columns = ['Gene_ID_v2', 'LFC', 'FDR', 'Gene_name', 'Description']
paper_vivo['LFC'] = pd.to_numeric(paper_vivo['LFC'], errors='coerce')
paper_vivo = paper_vivo.dropna(subset=['LFC'])

# Add v3 gene IDs to paper's data
def normalize_gene_id(gene_id):
    if not isinstance(gene_id, str):
        return gene_id
    parts = gene_id.split('_')
    if len(parts) == 2 and parts[0] == 'B9J08':
        numeric = parts[1].lstrip('0') or '0'
        return f"B9J08_{numeric.zfill(5)}"
    return gene_id

paper_vitro['Gene_ID_v3'] = paper_vitro['Gene_ID_v2'].apply(normalize_gene_id)
paper_vivo['Gene_ID_v3'] = paper_vivo['Gene_ID_v2'].apply(normalize_gene_id)

print("="*80)
print("FINAL COMPREHENSIVE ANALYSIS")
print("="*80)

print("\n" + "="*80)
print("1. ANNOTATION VERSION ISSUE IDENTIFIED")
print("="*80)
print("\n📋 Summary:")
print(f"  Paper used:  B8441 v2 annotation (6-digit gene IDs: B9J08_001458)")
print(f"  You used:    B8441 v3 annotation (5-digit gene IDs: B9J08_01458)")
print(f"  Both use the SAME genome: C. auris strain B8441 (AR0387)")

print("\n" + "="*80)
print("2. COMPARISON DIRECTION ISSUE")
print("="*80)
print("\nFrom the paper (page 2):")
print('  "AR0382 (B11109) and nonaggregative AR0387 (B8441)"')
print(f"  Paper's LFC: AR0382 / AR0387 (positive = upregulated in AR0382)")
print(f"\nYour DESeq2 setup (from gxy.md):")
print(f"  Factor level '87' (AR0387) vs '82' (AR0382)")
print(f"  Your LFC: AR0387 / AR0382 (positive = upregulated in AR0387)")
print(f"\n⚠️  Your comparison is REVERSED!")

print("\n" + "="*80)
print("3. KEY GENES ANALYSIS (with corrected gene IDs & reversed LFC)")
print("="*80)

key_genes = {
    'SCF1': ('B9J08_001458', 'B9J08_01458'),
    'ALS4112': ('B9J08_004112', 'B9J08_04112'),
    'IFF4109': ('B9J08_004109', 'B9J08_04109')
}

for gene_name, (gene_v2, gene_v3) in key_genes.items():
    print(f"\n{gene_name} ({gene_v2} / {gene_v3}):")

    # Paper in vitro
    paper_vitro_match = paper_vitro[paper_vitro['Gene_ID_v3'] == gene_v3]
    if len(paper_vitro_match) > 0:
        paper_lfc_vitro = paper_vitro_match.iloc[0]['LFC']
        print(f"  Paper in vitro:  LFC = {paper_lfc_vitro:6.2f}")
    else:
        print(f"  Paper in vitro:  NOT IN LIST")

    # Our in vitro (REVERSED)
    our_vitro_match = our_vitro[our_vitro['GeneID'] == gene_v3]
    if len(our_vitro_match) > 0:
        our_lfc_vitro = our_vitro_match.iloc[0]['log2FoldChange']
        our_lfc_vitro_rev = -our_lfc_vitro  # Reverse
        our_padj_vitro = our_vitro_match.iloc[0]['padj']
        print(f"  Our in vitro:    LFC = {our_lfc_vitro_rev:6.2f} (reversed), padj = {our_padj_vitro:.2e}")

    # Paper in vivo
    paper_vivo_match = paper_vivo[paper_vivo['Gene_ID_v3'] == gene_v3]
    if len(paper_vivo_match) > 0:
        paper_lfc_vivo = paper_vivo_match.iloc[0]['LFC']
        print(f"  Paper in vivo:   LFC = {paper_lfc_vivo:6.2f}")
    else:
        print(f"  Paper in vivo:   NOT IN LIST")

    # Our in vivo (REVERSED)
    our_vivo_match = our_vivo[our_vivo['GeneID'] == gene_v3]
    if len(our_vivo_match) > 0:
        our_lfc_vivo = our_vivo_match.iloc[0]['log2FoldChange']
        our_lfc_vivo_rev = -our_lfc_vivo  # Reverse
        our_padj_vivo = our_vivo_match.iloc[0]['padj']
        print(f"  Our in vivo:     LFC = {our_lfc_vivo_rev:6.2f} (reversed), padj = {our_padj_vivo:.2e}")

# Now compare with reversed LFC
print("\n" + "="*80)
print("4. OVERALL COMPARISON (with reversed LFC)")
print("="*80)

# Merge paper and our data
vitro_merged = paper_vitro.merge(our_vitro, left_on='Gene_ID_v3', right_on='GeneID', how='inner')
vitro_merged['our_LFC_reversed'] = -vitro_merged['log2FoldChange']

vivo_merged = paper_vivo.merge(our_vivo, left_on='Gene_ID_v3', right_on='GeneID', how='inner')
vivo_merged['our_LFC_reversed'] = -vivo_merged['log2FoldChange']

print(f"\nIn Vitro:")
print(f"  Genes in paper: {len(paper_vitro)}")
print(f"  Genes in our results (all): {len(our_vitro)}")
print(f"  Genes matched (v2 IDs -> v3 IDs): {len(vitro_merged)}")

if len(vitro_merged) > 0:
    print(f"\n  Correlation of LFC (reversed): {vitro_merged['LFC'].corr(vitro_merged['our_LFC_reversed']):.3f}")
    print(f"\n  Top 5 matched genes:")
    top5 = vitro_merged.nlargest(5, 'LFC')[['Gene_ID_v2', 'Gene_ID_v3', 'LFC', 'our_LFC_reversed']]
    print(top5.to_string(index=False))

print(f"\nIn Vivo:")
print(f"  Genes in paper: {len(paper_vivo)}")
print(f"  Genes in our results (all): {len(our_vivo)}")
print(f"  Genes matched (v2 IDs -> v3 IDs): {len(vivo_merged)}")

if len(vivo_merged) > 0:
    print(f"\n  Correlation of LFC (reversed): {vivo_merged['LFC'].corr(vivo_merged['our_LFC_reversed']):.3f}")
    print(f"\n  Top 5 matched genes:")
    top5 = vivo_merged.nlargest(5, 'LFC')[['Gene_ID_v2', 'Gene_ID_v3', 'LFC', 'our_LFC_reversed']]
    print(top5.to_string(index=False))

print("\n" + "="*80)
print("5. RECOMMENDATIONS")
print("="*80)
print("\n1. ✓ Annotation version issue: IDENTIFIED")
print("   - Paper used B8441 v2 (6-digit IDs)")
print("   - You used B8441 v3 (5-digit IDs)")
print("   - Mapping created: gene_id_mapping_v2_to_v3.tsv")
print("\n2. ✓ Comparison direction: REVERSED")
print("   - Your results need LFC sign reversed (-LFC)")
print("\n3. Next steps:")
print("   - Re-run DESeq2 with corrected factor order (82 vs 87)")
print("   - OR multiply all LFC values by -1 in post-processing")
print("   - Compare correlation after correction")

