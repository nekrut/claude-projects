#!/usr/bin/env python3
"""
Detailed comparison with paper's supplementary data
"""

import pandas as pd
import numpy as np

# Thresholds
LFC_THRESHOLD = 1.0
PADJ_THRESHOLD = 0.01

def parse_paper_data(file_path, experiment_name):
    """Parse paper's supplementary Excel file"""
    print(f"\n{'='*80}")
    print(f"Parsing Paper's Data: {experiment_name}")
    print(f"{'='*80}")

    # Read Excel, skip header rows
    df = pd.read_excel(file_path)

    # Find the row with "Gene_ID" to identify where data starts
    header_row = None
    for idx, row in df.iterrows():
        if 'Gene_ID' in str(row.values):
            header_row = idx
            break

    if header_row is None:
        print("Could not find header row with 'Gene_ID'")
        return None

    # Re-read with correct header
    df = pd.read_excel(file_path, header=header_row)

    # Clean up column names
    df.columns = df.columns.str.strip()
    print(f"\nColumns: {list(df.columns)}")
    print(f"Total genes in paper: {len(df)}")

    # Show first few rows
    print(f"\nFirst 10 genes:")
    print(df.head(10).to_string())

    return df

def normalize_gene_id(gene_id):
    """Normalize gene ID to 5-digit format"""
    # B9J08_001458 -> B9J08_01458 (5 digits)
    # B9J08_1458 -> B9J08_01458 (pad to 5 digits)
    parts = gene_id.split('_')
    if len(parts) == 2:
        # Ensure 5-digit format (standard for C. auris)
        numeric_part = parts[1].lstrip('0') or '0'  # Remove leading zeros
        return f"{parts[0]}_{numeric_part.zfill(5)}"  # Pad to 5 digits
    return gene_id

def compare_gene_lists(our_results_file, paper_df, experiment_name, reversed_comparison=True):
    """Compare our gene list with paper's gene list"""
    print(f"\n{'='*80}")
    print(f"Detailed Comparison: {experiment_name}")
    print(f"Comparison reversed: {reversed_comparison}")
    print(f"{'='*80}")

    # Load our results
    our_df = pd.read_csv(our_results_file, sep='\t', header=None,
                         names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])

    # Reverse LFC if needed
    if reversed_comparison:
        our_df['log2FoldChange'] = -our_df['log2FoldChange']
        print("✓ Reversed LFC signs")

    # Filter for significant DEGs
    our_sig = our_df[
        (our_df['padj'] < PADJ_THRESHOLD) &
        (np.abs(our_df['log2FoldChange']) >= LFC_THRESHOLD)
    ].copy()

    print(f"\nOur significant DEGs: {len(our_sig)}")
    print(f"Paper's DEGs: {len(paper_df)}")

    # Normalize gene IDs in paper data
    # The first column contains Gene_ID
    gene_id_col = paper_df.columns[0]
    paper_genes_raw = paper_df[gene_id_col].dropna().tolist()
    # Skip the first row if it's 'Gene_ID' (header)
    if paper_genes_raw[0] == 'Gene_ID':
        paper_genes_raw = paper_genes_raw[1:]

    paper_genes = set(normalize_gene_id(str(g)) for g in paper_genes_raw)
    our_genes = set(our_sig['GeneID'])

    print(f"\nOverlap analysis:")
    overlap = our_genes.intersection(paper_genes)
    only_ours = our_genes - paper_genes
    only_paper = paper_genes - our_genes

    print(f"  Genes in both: {len(overlap)} ({len(overlap)/len(paper_genes)*100:.1f}% of paper's list)")
    print(f"  Only in our results: {len(only_ours)}")
    print(f"  Only in paper: {len(only_paper)}")

    if len(only_ours) > 0:
        print(f"\nTop 10 genes only in our results:")
        only_ours_df = our_sig[our_sig['GeneID'].isin(only_ours)].sort_values('padj').head(10)
        for _, row in only_ours_df.iterrows():
            print(f"  {row['GeneID']:15s} | LFC: {row['log2FoldChange']:6.2f} | padj: {row['padj']:.2e}")

    if len(only_paper) > 0:
        print(f"\nFirst 10 genes only in paper (checking our data):")
        count = 0
        for gene_id in list(only_paper)[:10]:
            our_gene = our_df[our_df['GeneID'] == gene_id]
            if len(our_gene) > 0:
                row = our_gene.iloc[0]
                sig_status = "padj too high" if row['padj'] >= PADJ_THRESHOLD else "LFC too low"
                print(f"  {gene_id:15s} | LFC: {row['log2FoldChange']:6.2f} | padj: {row['padj']:.2e} | {sig_status}")
                count += 1
            else:
                print(f"  {gene_id:15s} | NOT FOUND in our results")

    # Check specific key genes
    print(f"\nKey adhesin genes (SCF1, ALS4112, IFF4109):")
    key_genes_normalized = ['B9J08_01458', 'B9J08_04112', 'B9J08_04109']

    for gene_id in key_genes_normalized:
        in_paper = gene_id in paper_genes
        our_gene = our_df[our_df['GeneID'] == gene_id]

        print(f"\n{gene_id}:")
        print(f"  In paper's list: {in_paper}")

        if len(our_gene) > 0:
            row = our_gene.iloc[0]
            is_sig = (row['padj'] < PADJ_THRESHOLD) and (abs(row['log2FoldChange']) >= LFC_THRESHOLD)
            print(f"  Our LFC: {row['log2FoldChange']:6.2f} | padj: {row['padj']:.2e} | Significant: {is_sig}")

    # Show top 10 genes from our results
    print(f"\n{'='*80}")
    print(f"Top 10 upregulated genes in AR0382 (our results, after reversal):")
    print(f"{'='*80}")
    top_up = our_sig[our_sig['log2FoldChange'] > 0].sort_values('log2FoldChange', ascending=False).head(10)
    for idx, row in top_up.iterrows():
        in_paper = row['GeneID'] in paper_genes
        marker = "✓" if in_paper else "✗"
        print(f"{marker} {row['GeneID']:15s} | LFC: {row['log2FoldChange']:6.2f} | padj: {row['padj']:.2e}")

def main():
    print("="*80)
    print("DETAILED COMPARISON WITH PAPER'S SUPPLEMENTARY DATA")
    print("="*80)

    # Parse paper's data
    paper_in_vitro = parse_paper_data("41467_2024_53588_MOESM3_ESM.xlsx", "In Vitro (Supplementary Data 1)")
    paper_in_vivo = parse_paper_data("41467_2024_53588_MOESM4_ESM.xlsx", "In Vivo (Supplementary Data 2)")

    # Compare with reversed comparison (87 vs 82)
    if paper_in_vitro is not None:
        compare_gene_lists("deseq2_in_vitro_results.tsv", paper_in_vitro, "In Vitro", reversed_comparison=True)

    if paper_in_vivo is not None:
        compare_gene_lists("deseq2_in_vivo_results.tsv", paper_in_vivo, "In Vivo", reversed_comparison=True)

if __name__ == "__main__":
    main()
