#!/usr/bin/env python3
"""
Analyze DESeq2 results and compare with paper expectations
"""

import pandas as pd
import numpy as np

# Thresholds from paper
LFC_THRESHOLD = 1.0
PADJ_THRESHOLD = 0.01

# Expected DEG counts from paper
EXPECTED_IN_VITRO = 76
EXPECTED_IN_VIVO = 259

# Key genes to verify (from paper)
# Note: IDs in results don't have leading zeros
KEY_GENES = {
    'SCF1': 'B9J08_01458',
    'ALS4112': 'B9J08_04112',
    'IFF4109': 'B9J08_04109'
}

def analyze_results(file_path, experiment_name, expected_degs):
    """Analyze a single DESeq2 results file"""
    print(f"\n{'='*80}")
    print(f"Analysis: {experiment_name}")
    print(f"{'='*80}")

    # Load results - DESeq2 output from Galaxy doesn't have headers
    df = pd.read_csv(file_path, sep='\t', header=None,
                     names=['GeneID', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])
    print(f"\nTotal genes analyzed: {len(df)}")

    # Show column names
    print(f"\nColumns in results: {list(df.columns)}")

    # Filter for significant DEGs
    significant = df[
        (df['padj'] < PADJ_THRESHOLD) &
        (np.abs(df['log2FoldChange']) >= LFC_THRESHOLD)
    ].copy()

    print(f"\n--- Significant DEGs (|LFC| ≥ {LFC_THRESHOLD}, padj < {PADJ_THRESHOLD}) ---")
    print(f"Found: {len(significant)} DEGs")
    print(f"Expected (from paper): {expected_degs} DEGs")
    print(f"Difference: {len(significant) - expected_degs} ({(len(significant)/expected_degs - 1)*100:.1f}% from expected)")

    # Separate upregulated and downregulated
    upregulated = significant[significant['log2FoldChange'] > 0]
    downregulated = significant[significant['log2FoldChange'] < 0]

    print(f"\nUpregulated in AR0382 (aggregative): {len(upregulated)}")
    print(f"Downregulated in AR0382 (aggregative): {len(downregulated)}")

    # Show top 10 upregulated genes
    print(f"\n--- Top 10 Upregulated Genes in AR0382 ---")
    top_up = upregulated.sort_values('log2FoldChange', ascending=False).head(10)
    for idx, row in top_up.iterrows():
        print(f"{row['GeneID']:15s} | LFC: {row['log2FoldChange']:6.2f} | padj: {row['padj']:.2e}")

    # Show top 10 downregulated genes
    print(f"\n--- Top 10 Downregulated Genes in AR0382 ---")
    top_down = downregulated.sort_values('log2FoldChange', ascending=True).head(10)
    for idx, row in top_down.iterrows():
        print(f"{row['GeneID']:15s} | LFC: {row['log2FoldChange']:6.2f} | padj: {row['padj']:.2e}")

    # Check for key adhesin genes
    print(f"\n--- Key Adhesin Genes from Paper ---")
    for gene_name, gene_id in KEY_GENES.items():
        gene_data = df[df['GeneID'] == gene_id]
        if len(gene_data) > 0:
            row = gene_data.iloc[0]
            is_sig = (row['padj'] < PADJ_THRESHOLD) and (abs(row['log2FoldChange']) >= LFC_THRESHOLD)
            status = "✓ SIGNIFICANT" if is_sig else "✗ Not significant"
            print(f"{gene_name} ({gene_id}):")
            print(f"  LFC: {row['log2FoldChange']:6.2f} | padj: {row['padj']:.2e} | {status}")
        else:
            print(f"{gene_name} ({gene_id}): NOT FOUND in results")

    return significant

def main():
    print("="*80)
    print("DESeq2 Results Analysis - PRJNA1086003")
    print("Comparing with Wang et al. (2024)")
    print("="*80)

    # Analyze in vitro results
    in_vitro_degs = analyze_results(
        "deseq2_in_vitro_results.tsv",
        "In Vitro Biofilm Formation (AR0382 vs AR0387)",
        EXPECTED_IN_VITRO
    )

    # Analyze in vivo results
    in_vivo_degs = analyze_results(
        "deseq2_in_vivo_results.tsv",
        "In Vivo Catheter Infection (AR0382 vs AR0387)",
        EXPECTED_IN_VIVO
    )

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"\nIn vitro:  {len(in_vitro_degs)} DEGs found (expected: {EXPECTED_IN_VITRO})")
    print(f"In vivo:   {len(in_vivo_degs)} DEGs found (expected: {EXPECTED_IN_VIVO})")

    # Save filtered results
    in_vitro_degs.to_csv('deseq2_in_vitro_significant.tsv', sep='\t', index=False)
    in_vivo_degs.to_csv('deseq2_in_vivo_significant.tsv', sep='\t', index=False)

    print(f"\n✓ Filtered significant DEGs saved to:")
    print(f"  - deseq2_in_vitro_significant.tsv")
    print(f"  - deseq2_in_vivo_significant.tsv")

if __name__ == "__main__":
    main()
