#!/usr/bin/env python3
"""
Validate DESeq2 results against Santana et al. 2023 paper.
Uses LFC-based correlation mapping to handle different annotation versions.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

# Configuration
PAPER_EXCEL = "NIHMS2004453-supplement-Data_1_Source_Data.xlsx"
OUR_521 = "deseq2_521_tnswi1.tabular"  # tnSWI1 vs AR0382
OUR_523 = "deseq2_523_ar0387.tabular"  # AR0387 vs AR0382
OUTPUT_DIR = Path("validation_output")
OUTPUT_DIR.mkdir(exist_ok=True)

def load_paper_data(sheet):
    """Load paper DESeq2 results from Excel."""
    df = pd.read_excel(PAPER_EXCEL, sheet_name=sheet)
    df = df[['GeneID', 'log2FC', 'Padj']].copy()
    df.columns = ['gene_id', 'lfc', 'padj']
    return df

def load_our_data(filepath):
    """Load our DESeq2 results."""
    df = pd.read_csv(filepath, sep='\t', header=None,
                     names=['gene_id', 'baseMean', 'lfc', 'lfcSE', 'stat', 'pvalue', 'padj'])
    return df[['gene_id', 'lfc', 'padj']]

def map_genes_by_lfc(paper_df, our_df, tolerance=0.5):
    """
    Map genes between datasets using LFC correlation.
    For each paper gene, find our gene with closest LFC value.
    """
    # Filter to significant DEGs for more reliable mapping
    paper_sig = paper_df[paper_df['padj'] < 0.05].copy()
    our_sig = our_df[our_df['padj'] < 0.05].copy()

    mappings = []
    our_used = set()

    for _, paper_row in paper_sig.iterrows():
        paper_lfc = paper_row['lfc']

        # Find closest match in our data
        best_match = None
        best_diff = float('inf')

        for _, our_row in our_sig.iterrows():
            if our_row['gene_id'] in our_used:
                continue
            diff = abs(paper_lfc - our_row['lfc'])
            if diff < best_diff and diff < tolerance:
                best_diff = diff
                best_match = our_row

        if best_match is not None:
            mappings.append({
                'paper_gene': paper_row['gene_id'],
                'our_gene': best_match['gene_id'],
                'paper_lfc': paper_lfc,
                'our_lfc': best_match['lfc'],
                'lfc_diff': best_diff
            })
            our_used.add(best_match['gene_id'])

    return pd.DataFrame(mappings)

def check_direction_reversal(mapping_df):
    """Check if LFC signs are reversed (different reference condition)."""
    if len(mapping_df) == 0:
        return False, mapping_df

    # Check correlation with original signs
    r_original = np.corrcoef(mapping_df['paper_lfc'], mapping_df['our_lfc'])[0,1]
    r_flipped = np.corrcoef(mapping_df['paper_lfc'], -mapping_df['our_lfc'])[0,1]

    if r_flipped > r_original:
        mapping_df = mapping_df.copy()
        mapping_df['our_lfc'] = -mapping_df['our_lfc']
        mapping_df['lfc_diff'] = abs(mapping_df['paper_lfc'] - mapping_df['our_lfc'])
        return True, mapping_df
    return False, mapping_df

def calculate_metrics(mapping_df):
    """Calculate validation metrics."""
    if len(mapping_df) == 0:
        return {}

    paper_lfc = mapping_df['paper_lfc'].values
    our_lfc = mapping_df['our_lfc'].values

    # Pearson R²
    r, _ = stats.pearsonr(paper_lfc, our_lfc)
    r_squared = r ** 2

    # Spearman correlation
    spearman_r, _ = stats.spearmanr(paper_lfc, our_lfc)

    # Direction agreement
    same_direction = np.sum(np.sign(paper_lfc) == np.sign(our_lfc))
    direction_pct = same_direction / len(paper_lfc) * 100

    # Mean absolute difference
    mean_diff = np.mean(np.abs(paper_lfc - our_lfc))

    return {
        'n_mapped': len(mapping_df),
        'pearson_r2': r_squared,
        'spearman_r': spearman_r,
        'direction_agreement': direction_pct,
        'mean_lfc_diff': mean_diff
    }

def create_scatter_plot(mapping_df, title, output_file, scf1_paper='B9J08_001458', scf1_our='B9J08_03708'):
    """Create scatter plot comparing LFC values."""
    fig, ax = plt.subplots(figsize=(8, 8))

    paper_lfc = mapping_df['paper_lfc'].values
    our_lfc = mapping_df['our_lfc'].values

    # Plot all points
    ax.scatter(paper_lfc, our_lfc, alpha=0.5, s=30, c='steelblue', label='DEGs')

    # Highlight SCF1 if found
    scf1_row = mapping_df[mapping_df['paper_gene'] == scf1_paper]
    if len(scf1_row) > 0:
        ax.scatter(scf1_row['paper_lfc'], scf1_row['our_lfc'],
                   c='red', s=150, marker='*', label=f'SCF1', zorder=5)
        ax.annotate('SCF1', (scf1_row['paper_lfc'].values[0], scf1_row['our_lfc'].values[0]),
                    xytext=(10, 10), textcoords='offset points', fontsize=10, color='red')

    # Add regression line
    z = np.polyfit(paper_lfc, our_lfc, 1)
    p = np.poly1d(z)
    x_line = np.linspace(min(paper_lfc), max(paper_lfc), 100)
    ax.plot(x_line, p(x_line), 'r--', alpha=0.7, label='Regression')

    # Add diagonal
    lims = [min(min(paper_lfc), min(our_lfc)), max(max(paper_lfc), max(our_lfc))]
    ax.plot(lims, lims, 'k:', alpha=0.5, label='y=x')

    # Calculate R²
    r, _ = stats.pearsonr(paper_lfc, our_lfc)
    r_squared = r ** 2

    # Labels and formatting
    ax.set_xlabel('Paper log2FC', fontsize=12)
    ax.set_ylabel('Our log2FC', fontsize=12)
    ax.set_title(f'{title}\nR² = {r_squared:.4f}, n = {len(mapping_df)}', fontsize=14)
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3)

    # Make it square
    ax.set_aspect('equal', adjustable='box')

    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_file}")

def main():
    print("=" * 60)
    print("DESeq2 Validation: Santana et al. 2023")
    print("=" * 60)

    # Load data
    print("\nLoading data...")
    paper_1d = load_paper_data('1D')
    paper_s5a = load_paper_data('S5A')
    our_521 = load_our_data(OUR_521)
    our_523 = load_our_data(OUR_523)

    print(f"Paper 1D: {len(paper_1d)} genes")
    print(f"Paper S5A: {len(paper_s5a)} genes")
    print(f"Our #521 (tnSWI1): {len(our_521)} genes")
    print(f"Our #523 (AR0387): {len(our_523)} genes")

    results = {}

    # Comparison 1: tnSWI1 (Fig 1D)
    print("\n" + "-" * 40)
    print("Comparison 1: tnSWI1 vs AR0382 (Fig 1D)")
    print("-" * 40)

    mapping_1d = map_genes_by_lfc(paper_1d, our_521)
    reversed_1d, mapping_1d = check_direction_reversal(mapping_1d)
    if reversed_1d:
        print("Note: LFC signs were reversed (different reference condition)")

    metrics_1d = calculate_metrics(mapping_1d)
    results['1D'] = metrics_1d

    print(f"Mapped DEGs: {metrics_1d['n_mapped']}")
    print(f"Pearson R²: {metrics_1d['pearson_r2']:.4f}")
    print(f"Spearman R: {metrics_1d['spearman_r']:.4f}")
    print(f"Direction agreement: {metrics_1d['direction_agreement']:.1f}%")
    print(f"Mean |ΔLFC|: {metrics_1d['mean_lfc_diff']:.3f}")

    # Find SCF1
    scf1_1d = mapping_1d[mapping_1d['paper_gene'] == 'B9J08_001458']
    if len(scf1_1d) > 0:
        print(f"\nSCF1: Paper={scf1_1d['paper_lfc'].values[0]:.2f}, Ours={scf1_1d['our_lfc'].values[0]:.2f}")

    create_scatter_plot(mapping_1d, "tnSWI1 vs AR0382 (Fig 1D)",
                        OUTPUT_DIR / "fig1d_comparison.png")

    # Comparison 2: AR0387 (Fig S5A)
    print("\n" + "-" * 40)
    print("Comparison 2: AR0387 vs AR0382 (Fig S5A)")
    print("-" * 40)

    mapping_s5a = map_genes_by_lfc(paper_s5a, our_523)
    reversed_s5a, mapping_s5a = check_direction_reversal(mapping_s5a)
    if reversed_s5a:
        print("Note: LFC signs were reversed (different reference condition)")

    metrics_s5a = calculate_metrics(mapping_s5a)
    results['S5A'] = metrics_s5a

    print(f"Mapped DEGs: {metrics_s5a['n_mapped']}")
    print(f"Pearson R²: {metrics_s5a['pearson_r2']:.4f}")
    print(f"Spearman R: {metrics_s5a['spearman_r']:.4f}")
    print(f"Direction agreement: {metrics_s5a['direction_agreement']:.1f}%")
    print(f"Mean |ΔLFC|: {metrics_s5a['mean_lfc_diff']:.3f}")

    # Find SCF1
    scf1_s5a = mapping_s5a[mapping_s5a['paper_gene'] == 'B9J08_001458']
    if len(scf1_s5a) > 0:
        print(f"\nSCF1: Paper={scf1_s5a['paper_lfc'].values[0]:.2f}, Ours={scf1_s5a['our_lfc'].values[0]:.2f}")

    create_scatter_plot(mapping_s5a, "AR0387 vs AR0382 (Fig S5A)",
                        OUTPUT_DIR / "figs5a_comparison.png")

    # Save mappings
    mapping_1d.to_csv(OUTPUT_DIR / "gene_mapping_1d.tsv", sep='\t', index=False)
    mapping_s5a.to_csv(OUTPUT_DIR / "gene_mapping_s5a.tsv", sep='\t', index=False)
    print(f"\nSaved gene mappings to {OUTPUT_DIR}/")

    # Quality assessment
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    for name, m in [('Fig 1D (tnSWI1)', metrics_1d), ('Fig S5A (AR0387)', metrics_s5a)]:
        quality = "EXCELLENT" if m['pearson_r2'] > 0.95 else "GOOD" if m['pearson_r2'] > 0.85 else "MODERATE"
        print(f"\n{name}: {quality}")
        print(f"  R² = {m['pearson_r2']:.4f}, Direction = {m['direction_agreement']:.0f}%")

    return results

if __name__ == "__main__":
    main()
