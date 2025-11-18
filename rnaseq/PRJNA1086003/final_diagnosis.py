#!/usr/bin/env python3
"""
Final diagnosis: Understanding the discrepancy
"""

import pandas as pd
import numpy as np

def main():
    print("="*80)
    print("FINAL DIAGNOSIS")
    print("="*80)

    # Load our results
    in_vitro = pd.read_csv("deseq2_in_vitro_results.tsv", sep='\t', header=None,
                           names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])
    in_vivo = pd.read_csv("deseq2_in_vivo_results.tsv", sep='\t', header=None,
                          names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])

    # Load paper's data
    paper_vitro = pd.read_excel("41467_2024_53588_MOESM3_ESM.xlsx")
    paper_vivo = pd.read_excel("41467_2024_53588_MOESM4_ESM.xlsx")

    # Extract paper's gene data (skip headers)
    paper_vitro_genes = paper_vitro.iloc[1:].copy()
    paper_vitro_genes.columns = ['Gene_ID', 'LFC', 'FDR', 'Gene_name', 'Description']
    paper_vitro_genes['LFC'] = pd.to_numeric(paper_vitro_genes['LFC'], errors='coerce')
    paper_vitro_genes = paper_vitro_genes.dropna(subset=['LFC'])

    paper_vivo_genes = paper_vivo.iloc[1:].copy()
    paper_vivo_genes.columns = ['Gene_ID', 'LFC', 'FDR', 'Gene_name', 'Description']
    paper_vivo_genes['LFC'] = pd.to_numeric(paper_vivo_genes['LFC'], errors='coerce')
    paper_vivo_genes = paper_vivo_genes.dropna(subset=['LFC'])

    # Normalize gene IDs
    def normalize_id(gene_id):
        parts = str(gene_id).split('_')
        if len(parts) == 2:
            return f"{parts[0]}_{parts[1].zfill(5)}"
        return gene_id

    paper_vitro_genes['Gene_ID_norm'] = paper_vitro_genes['Gene_ID'].apply(normalize_id)
    paper_vivo_genes['Gene_ID_norm'] = paper_vivo_genes['Gene_ID'].apply(normalize_id)

    # Check key adhesin genes
    key_genes = ['B9J08_01458', 'B9J08_04112', 'B9J08_04109']

    print("\n" + "="*80)
    print("KEY ADHESIN GENES COMPARISON")
    print("="*80)

    for gene in key_genes:
        print(f"\n{gene}:")

        # In vitro
        paper_vitro_row = paper_vitro_genes[paper_vitro_genes['Gene_ID_norm'] == gene]
        our_vitro_row = in_vitro[in_vitro['GeneID'] == gene]

        if len(paper_vitro_row) > 0:
            print(f"  Paper in vitro: LFC = {paper_vitro_row.iloc[0]['LFC']:.2f}")
        else:
            print(f"  Paper in vitro: NOT IN LIST")

        if len(our_vitro_row) > 0:
            row = our_vitro_row.iloc[0]
            print(f"  Our in vitro:   LFC = {row['log2FoldChange']:6.2f} (raw)")
            print(f"                  LFC = {-row['log2FoldChange']:6.2f} (reversed)")
            print(f"                  padj = {row['padj']:.2e}")

        # In vivo
        paper_vivo_row = paper_vivo_genes[paper_vivo_genes['Gene_ID_norm'] == gene]
        our_vivo_row = in_vivo[in_vivo['GeneID'] == gene]

        if len(paper_vivo_row) > 0:
            print(f"  Paper in vivo:  LFC = {paper_vivo_row.iloc[0]['LFC']:.2f}")
        else:
            print(f"  Paper in vivo:  NOT IN LIST")

        if len(our_vivo_row) > 0:
            row = our_vivo_row.iloc[0]
            print(f"  Our in vivo:    LFC = {row['log2FoldChange']:6.2f} (raw)")
            print(f"                  LFC = {-row['log2FoldChange']:6.2f} (reversed)")
            print(f"                  padj = {row['padj']:.2e}")

    # Compare top genes
    print("\n" + "="*80)
    print("TOP 5 GENES COMPARISON - IN VITRO")
    print("="*80)

    print("\nPaper's top 5 upregulated:")
    for idx, row in paper_vitro_genes.head(5).iterrows():
        gene_norm = row['Gene_ID_norm']
        our_row = in_vitro[in_vitro['GeneID'] == gene_norm]
        if len(our_row) > 0:
            our_lfc = our_row.iloc[0]['log2FoldChange']
            our_padj = our_row.iloc[0]['padj']
            print(f"  {gene_norm:15s} | Paper LFC: {row['LFC']:6.2f} | Our LFC: {our_lfc:6.2f} (raw) | Our padj: {our_padj:.2e}")
        else:
            print(f"  {gene_norm:15s} | Paper LFC: {row['LFC']:6.2f} | NOT IN OUR RESULTS")

    print("\nOur top 5 upregulated (raw positive LFC):")
    top_our = in_vitro.sort_values('log2FoldChange', ascending=False).head(5)
    for idx, row in top_our.iterrows():
        gene_id = row['GeneID']
        paper_row = paper_vitro_genes[paper_vitro_genes['Gene_ID_norm'] == gene_id]
        if len(paper_row) > 0:
            paper_lfc = paper_row.iloc[0]['LFC']
            print(f"  {gene_id:15s} | Our LFC: {row['log2FoldChange']:6.2f} | Paper LFC: {paper_lfc:6.2f} | padj: {row['padj']:.2e}")
        else:
            print(f"  {gene_id:15s} | Our LFC: {row['log2FoldChange']:6.2f} | NOT IN PAPER | padj: {row['padj']:.2e}")

    print("\n" + "="*80)
    print("CONCLUSION")
    print("="*80)
    print("\nIf the key genes in the paper have LFC ~5-8 but our results show LFC ~0.3-0.8,")
    print("this indicates one of the following:")
    print("1. Different samples were analyzed")
    print("2. Annotation mismatch (different gene names for same loci)")
    print("3. Fundamental issue with the RNA-seq data or processing")
    print("4. The collections were not properly split by strain")

if __name__ == "__main__":
    main()
