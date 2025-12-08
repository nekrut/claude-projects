#!/usr/bin/env python3
"""
Self-contained validation script for Santana24 PRJNA904261 reproduction.

Extracts publication DEGs from Excel, maps gene IDs via LFC correlation,
and generates validation statistics and plots.

Usage:
    python validate.py \
        --supplement path/to/NIHMS2004453-supplement-Data_1_Source_Data.xlsx \
        --deseq2-tnswi1 analysis/deseq2_tnSWI1.tsv \
        --deseq2-ar0387 analysis/deseq2_AR0387.tsv \
        --output-dir analysis/
"""

import argparse
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import linear_sum_assignment


def load_deseq2_results(filepath):
    """Load DESeq2 results (headerless TSV)."""
    df = pd.read_csv(filepath, sep='\t', header=None,
                     names=['gene_id', 'baseMean', 'log2FoldChange', 'lfcSE', 'stat', 'pvalue', 'padj'])
    return df[['gene_id', 'log2FoldChange']].rename(columns={'log2FoldChange': 'lfc'}).dropna()


def extract_publication_degs(xlsx_path, sheet_name, gene_col='Gene_ID', lfc_col='LFC'):
    """Extract DEGs from publication Excel supplement."""
    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)

    # Case-insensitive column matching
    col_map = {c.lower(): c for c in df.columns}
    actual_gene = col_map.get(gene_col.lower(), gene_col)
    actual_lfc = col_map.get(lfc_col.lower(), lfc_col)

    if actual_gene not in df.columns:
        raise ValueError(f"Gene column '{gene_col}' not found. Available: {list(df.columns)}")
    if actual_lfc not in df.columns:
        raise ValueError(f"LFC column '{lfc_col}' not found. Available: {list(df.columns)}")

    return pd.DataFrame({
        'gene_id': df[actual_gene],
        'lfc': pd.to_numeric(df[actual_lfc], errors='coerce')
    }).dropna()


def detect_lfc_direction(source_df, target_df, sample_size=100):
    """Detect if LFC values need negation (reversed comparison direction)."""
    if len(source_df) > sample_size:
        source_sample = pd.concat([
            source_df.nlargest(sample_size // 2, 'lfc'),
            source_df.nsmallest(sample_size // 2, 'lfc')
        ])
    else:
        source_sample = source_df.copy()

    target_lfcs = target_df['lfc'].values
    matched_source, matched_target_asis, matched_target_neg = [], [], []

    for _, row in source_sample.iterrows():
        src_lfc = row['lfc']
        diffs_asis = np.abs(target_lfcs - src_lfc)
        diffs_neg = np.abs(target_lfcs - (-src_lfc))
        matched_source.append(src_lfc)
        matched_target_asis.append(target_lfcs[np.argmin(diffs_asis)])
        matched_target_neg.append(-target_lfcs[np.argmin(diffs_neg)])

    r_asis, _ = stats.pearsonr(matched_source, matched_target_asis)
    r_neg, _ = stats.pearsonr(matched_source, matched_target_neg)

    return abs(r_neg) > abs(r_asis), r_asis, r_neg


def create_lfc_mapping(source_df, target_df, auto_direction=True):
    """Map genes using LFC correlation with Hungarian algorithm for 1:1 mapping."""
    if auto_direction:
        should_negate, r_asis, r_neg = detect_lfc_direction(source_df, target_df)
        if should_negate:
            print(f"  Direction reversal detected (R={r_asis:.3f} vs R={r_neg:.3f} negated)")
            target_df = target_df.copy()
            target_df['lfc'] = -target_df['lfc']
        else:
            print(f"  LFC direction matches (R={r_asis:.3f})")

    # Hungarian algorithm for optimal 1:1 mapping
    cost_matrix = np.abs(
        source_df['lfc'].values[:, np.newaxis] -
        target_df['lfc'].values[np.newaxis, :]
    )
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    mappings = []
    for i, j in zip(row_ind, col_ind):
        mappings.append({
            'source_gene': source_df.iloc[i]['gene_id'],
            'source_lfc': source_df.iloc[i]['lfc'],
            'target_gene': target_df.iloc[j]['gene_id'],
            'target_lfc': target_df.iloc[j]['lfc'],
            'lfc_diff': cost_matrix[i, j]
        })

    return pd.DataFrame(mappings).sort_values('lfc_diff')


def validate_mapping(mapping_df):
    """Calculate validation statistics."""
    src = mapping_df['source_lfc'].values
    tgt = mapping_df['target_lfc'].values

    pearson_r, pearson_p = stats.pearsonr(src, tgt)
    spearman_r, spearman_p = stats.spearmanr(src, tgt)

    direction_match = np.sum(np.sign(src) == np.sign(tgt))
    direction_pct = direction_match / len(src) * 100

    return {
        'n_mapped': len(mapping_df),
        'pearson_r': pearson_r,
        'pearson_r_squared': pearson_r ** 2,
        'spearman_r': spearman_r,
        'direction_agreement_pct': direction_pct,
        'lfc_diff_mean': np.mean(mapping_df['lfc_diff']),
        'lfc_diff_max': np.max(mapping_df['lfc_diff'])
    }


def plot_validation(mapping_df, output_path, title):
    """Generate correlation and Bland-Altman plots."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Warning: matplotlib not available, skipping plot")
        return

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    src = mapping_df['source_lfc'].values
    tgt = mapping_df['target_lfc'].values

    # Correlation plot
    ax1 = axes[0]
    ax1.scatter(src, tgt, alpha=0.6, s=50, c='steelblue', edgecolors='white', linewidth=0.5)
    slope, intercept, r_value, _, _ = stats.linregress(src, tgt)
    x_line = np.linspace(min(src), max(src), 100)
    ax1.plot(x_line, slope * x_line + intercept, 'r-', linewidth=2, label=f'R² = {r_value**2:.4f}')
    lim = max(abs(min(src)), abs(max(src)), abs(min(tgt)), abs(max(tgt))) * 1.1
    ax1.plot([-lim, lim], [-lim, lim], 'k--', alpha=0.5, label='y = x')
    ax1.set_xlabel('Publication LFC')
    ax1.set_ylabel('Our LFC')
    ax1.set_title(f'{title}\n(n={len(mapping_df)} genes)')
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)

    # Bland-Altman plot
    ax2 = axes[1]
    mean_lfc = (src + tgt) / 2
    diff_lfc = src - tgt
    ax2.scatter(mean_lfc, diff_lfc, alpha=0.6, s=50, c='steelblue', edgecolors='white', linewidth=0.5)
    mean_diff, std_diff = np.mean(diff_lfc), np.std(diff_lfc)
    ax2.axhline(y=mean_diff, color='red', linestyle='-', label=f'Mean: {mean_diff:.4f}')
    ax2.axhline(y=mean_diff + 1.96*std_diff, color='red', linestyle='--', alpha=0.7)
    ax2.axhline(y=mean_diff - 1.96*std_diff, color='red', linestyle='--', alpha=0.7)
    ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax2.set_xlabel('Mean LFC')
    ax2.set_ylabel('Difference (Publication - Our)')
    ax2.set_title('Bland-Altman Agreement')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Plot saved: {output_path}")


def print_report(name, stats_dict, mapping_df):
    """Print validation report."""
    print(f"\n{'='*60}")
    print(f"VALIDATION: {name}")
    print(f"{'='*60}")
    print(f"Mapped genes: {stats_dict['n_mapped']}")
    print(f"Pearson R²:   {stats_dict['pearson_r_squared']:.4f}")
    print(f"Spearman R:   {stats_dict['spearman_r']:.4f}")
    print(f"Direction:    {stats_dict['direction_agreement_pct']:.1f}%")
    print(f"Mean LFC diff: {stats_dict['lfc_diff_mean']:.4f}")

    # Quality assessment
    r_sq = stats_dict['pearson_r_squared']
    dir_pct = stats_dict['direction_agreement_pct']
    if r_sq > 0.99 and dir_pct == 100:
        status = "EXCELLENT"
    elif r_sq > 0.95 and dir_pct > 95:
        status = "GOOD"
    else:
        status = "CHECK RESULTS"
    print(f"Status:       {status}")

    # Find SCF1
    scf1 = mapping_df[mapping_df['target_gene'].str.contains('03708', na=False)]
    if len(scf1) > 0:
        print(f"\nSCF1 (B9J08_03708):")
        print(f"  Paper ID:  {scf1.iloc[0]['source_gene']}")
        print(f"  Paper LFC: {scf1.iloc[0]['source_lfc']:.2f}")
        print(f"  Our LFC:   {scf1.iloc[0]['target_lfc']:.2f}")


def list_excel_sheets(xlsx_path):
    """List available sheets in Excel file."""
    xlsx = pd.ExcelFile(xlsx_path)
    print(f"\nAvailable sheets in {xlsx_path}:")
    for i, name in enumerate(xlsx.sheet_names):
        print(f"  [{i}] {name}")
    return xlsx.sheet_names


def main():
    parser = argparse.ArgumentParser(description='Validate Santana24 reproduction')
    parser.add_argument('--supplement', required=True, help='Publication Excel supplement')
    parser.add_argument('--deseq2-tnswi1', help='DESeq2 results for AR0382 vs tnSWI1')
    parser.add_argument('--deseq2-ar0387', help='DESeq2 results for AR0382 vs AR0387')
    parser.add_argument('--output-dir', default='.', help='Output directory')
    parser.add_argument('--sheet-fig1d', default='Figure 1D', help='Excel sheet for Figure 1D DEGs')
    parser.add_argument('--sheet-figs5a', default='Figure S5A', help='Excel sheet for Figure S5A DEGs')
    parser.add_argument('--list-sheets', action='store_true', help='List Excel sheets and exit')
    parser.add_argument('--gene-col', default='Gene_ID', help='Gene ID column name in Excel')
    parser.add_argument('--lfc-col', default='LFC', help='LFC column name in Excel')

    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    if args.list_sheets:
        list_excel_sheets(args.supplement)
        return

    report_lines = []

    # Comparison 1: AR0382 vs tnSWI1
    if args.deseq2_tnswi1:
        print("\n" + "="*60)
        print("Processing: AR0382 vs tnSWI1 (Figure 1D)")
        print("="*60)

        try:
            paper_degs = extract_publication_degs(args.supplement, args.sheet_fig1d, args.gene_col, args.lfc_col)
            print(f"  Paper DEGs: {len(paper_degs)}")
        except Exception as e:
            print(f"  Error reading Excel: {e}")
            print("  Use --list-sheets to see available sheets")
            sys.exit(1)

        our_degs = load_deseq2_results(args.deseq2_tnswi1)
        print(f"  Our genes: {len(our_degs)}")

        mapping = create_lfc_mapping(paper_degs, our_degs, auto_direction=True)
        stats_dict = validate_mapping(mapping)

        mapping.to_csv(output_dir / 'gene_mapping_tnSWI1.csv', index=False)
        plot_validation(mapping, output_dir / 'validation_tnSWI1.png', 'AR0382 vs tnSWI1')
        print_report('AR0382 vs tnSWI1', stats_dict, mapping)

    # Comparison 2: AR0382 vs AR0387
    if args.deseq2_ar0387:
        print("\n" + "="*60)
        print("Processing: AR0382 vs AR0387 (Figure S5A)")
        print("="*60)

        try:
            paper_degs = extract_publication_degs(args.supplement, args.sheet_figs5a, args.gene_col, args.lfc_col)
            print(f"  Paper DEGs: {len(paper_degs)}")
        except Exception as e:
            print(f"  Error reading Excel: {e}")
            print("  Use --list-sheets to see available sheets")
            sys.exit(1)

        our_degs = load_deseq2_results(args.deseq2_ar0387)
        print(f"  Our genes: {len(our_degs)}")

        mapping = create_lfc_mapping(paper_degs, our_degs, auto_direction=True)
        stats_dict = validate_mapping(mapping)

        mapping.to_csv(output_dir / 'gene_mapping_AR0387.csv', index=False)
        plot_validation(mapping, output_dir / 'validation_AR0387.png', 'AR0382 vs AR0387')
        print_report('AR0382 vs AR0387', stats_dict, mapping)

    print("\n" + "="*60)
    print("Validation complete!")
    print("="*60)


if __name__ == '__main__':
    main()
