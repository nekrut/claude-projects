#!/usr/bin/env python3
"""
Compare our DESeq2 results with the paper's supplementary data
Also check if the comparison direction is reversed
"""

import pandas as pd
import numpy as np

# Thresholds
LFC_THRESHOLD = 1.0
PADJ_THRESHOLD = 0.01

# Key genes from paper
KEY_GENES = ['B9J08_01458', 'B9J08_04112', 'B9J08_04109']  # SCF1, ALS4112, IFF4109

def load_paper_data(file_path, sheet_name=0):
    """Load supplementary data from Excel file"""
    print(f"\nLoading: {file_path}")
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    print(f"Columns: {list(df.columns)}")
    print(f"Shape: {df.shape}")
    print(f"\nFirst few rows:")
    print(df.head())
    return df

def check_reversed_comparison(our_results_file, experiment_name):
    """Check if comparison is reversed by looking at key genes"""
    print(f"\n{'='*80}")
    print(f"Checking if comparison is REVERSED: {experiment_name}")
    print(f"{'='*80}")

    df = pd.read_csv(our_results_file, sep='\t', header=None,
                     names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])

    print(f"\nKey genes (paper says should be upregulated in AR0382):")
    print(f"If comparison is NORMAL (82 vs 87): genes should have POSITIVE LFC")
    print(f"If comparison is REVERSED (87 vs 82): genes should have NEGATIVE LFC")
    print()

    for gene_id in KEY_GENES:
        gene_data = df[df['GeneID'] == gene_id]
        if len(gene_data) > 0:
            row = gene_data.iloc[0]
            direction = "NEGATIVE" if row['log2FoldChange'] < 0 else "POSITIVE"
            print(f"{gene_id}: LFC = {row['log2FoldChange']:6.2f} ({direction})")

    # Also check top genes by absolute LFC
    print(f"\nTop 10 genes by absolute LFC:")
    df_sorted = df.sort_values('log2FoldChange', key=abs, ascending=False).head(10)
    for idx, row in df_sorted.iterrows():
        direction = "↓ AR0382" if row['log2FoldChange'] < 0 else "↑ AR0382 (if reversed)"
        print(f"{row['GeneID']:15s} | LFC: {row['log2FoldChange']:7.2f} | {direction}")

    return df

def compare_with_paper(our_df, paper_df, experiment_name, comparison_reversed=False):
    """Compare our results with paper's supplementary data"""
    print(f"\n{'='*80}")
    print(f"Comparing with Paper: {experiment_name}")
    print(f"Comparison reversed: {comparison_reversed}")
    print(f"{'='*80}")

    # Adjust our LFC if comparison is reversed
    our_df_adj = our_df.copy()
    if comparison_reversed:
        our_df_adj['log2FoldChange'] = -our_df_adj['log2FoldChange']
        print("\n⚠️  REVERSING LFC SIGN in our results for comparison")

    # Filter for significant DEGs
    our_sig = our_df_adj[
        (our_df_adj['padj'] < PADJ_THRESHOLD) &
        (np.abs(our_df_adj['log2FoldChange']) >= LFC_THRESHOLD)
    ].copy()

    print(f"\nOur significant DEGs: {len(our_sig)}")

    # Check key genes again
    print(f"\nKey adhesin genes (after accounting for reversal):")
    for gene_id in KEY_GENES:
        # Our data
        our_gene = our_df_adj[our_df_adj['GeneID'] == gene_id]
        if len(our_gene) > 0:
            our_row = our_gene.iloc[0]
            is_sig = (our_row['padj'] < PADJ_THRESHOLD) and (abs(our_row['log2FoldChange']) >= LFC_THRESHOLD)
            status = "✓ SIGNIFICANT" if is_sig else "✗ Not significant"
            print(f"\n{gene_id}:")
            print(f"  Our LFC: {our_row['log2FoldChange']:6.2f} | padj: {our_row['padj']:.2e} | {status}")

def main():
    print("="*80)
    print("Comprehensive Comparison with Paper")
    print("="*80)

    # First, check if comparison is reversed
    print("\n" + "="*80)
    print("STEP 1: Check if comparison direction is reversed")
    print("="*80)

    in_vitro_df = check_reversed_comparison(
        "deseq2_in_vitro_results.tsv",
        "In Vitro"
    )

    in_vivo_df = check_reversed_comparison(
        "deseq2_in_vivo_results.tsv",
        "In Vivo"
    )

    # Load paper's supplementary data
    print("\n" + "="*80)
    print("STEP 2: Load Paper's Supplementary Data")
    print("="*80)

    try:
        paper_in_vitro = load_paper_data("41467_2024_53588_MOESM3_ESM.xlsx")
    except Exception as e:
        print(f"Error loading MOESM3 (in vitro): {e}")
        paper_in_vitro = None

    try:
        paper_in_vivo = load_paper_data("41467_2024_53588_MOESM4_ESM.xlsx")
    except Exception as e:
        print(f"Error loading MOESM4 (in vivo): {e}")
        paper_in_vivo = None

    # Ask user if comparison is reversed
    print("\n" + "="*80)
    print("STEP 3: Analyze with comparison direction")
    print("="*80)
    print("\nBased on the LFC signs above, determine if comparison is reversed.")
    print("If key genes have NEGATIVE LFC, comparison is likely REVERSED.")
    print("\nAnalyzing with REVERSED comparison (87 vs 82)...")

    if paper_in_vitro is not None:
        compare_with_paper(in_vitro_df, paper_in_vitro, "In Vitro", comparison_reversed=True)

    if paper_in_vivo is not None:
        compare_with_paper(in_vivo_df, paper_in_vivo, "In Vivo", comparison_reversed=True)

if __name__ == "__main__":
    main()
