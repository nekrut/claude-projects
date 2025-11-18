#!/usr/bin/env python3
"""
Final comprehensive comparison between our DEGs and paper's DEGs
using corrected gene ID mappings
"""

import pandas as pd
import numpy as np

print("="*80)
print("FINAL DEG COMPARISON: OUR DATA vs PAPER")
print("="*80)

# Load corrected DEG lists
print("\nLoading corrected DEG lists...")
paper_vitro = pd.read_csv('paper_vitro_degs_corrected.tsv', sep='\t')
paper_vivo = pd.read_csv('paper_vivo_degs_corrected.tsv', sep='\t')
our_vitro = pd.read_csv('our_vitro_degs_corrected.tsv', sep='\t')
our_vivo = pd.read_csv('our_vivo_degs_corrected.tsv', sep='\t')

print(f"  Paper in_vitro: {len(paper_vitro)} DEGs")
print(f"  Paper in_vivo: {len(paper_vivo)} DEGs")
print(f"  Our in_vitro: {len(our_vitro)} DEGs")
print(f"  Our in_vivo: {len(our_vivo)} DEGs")

def compare_degs(paper_df, our_df, comparison_name):
    """Compare DEG lists using both v2 and v3 gene IDs"""
    print("\n" + "="*80)
    print(f"{comparison_name}")
    print("="*80)

    # Get gene sets (use both v2 and v3 for matching)
    paper_v2 = set(paper_df['Gene_ID_v2'].dropna())
    paper_v3 = set(paper_df['Gene_ID_v3'].dropna())
    our_v2 = set(our_df['Gene_ID_v2'].dropna())
    our_v3 = set(our_df['Gene_ID_v3'].dropna())

    # Find overlaps (genes found as DEGs in both analyses)
    overlap_v2 = paper_v2 & our_v2
    overlap_v3 = paper_v3 & our_v3

    # Union of overlaps (in case some genes only match in one annotation)
    all_overlap_genes = overlap_v2 | overlap_v3

    # Genes unique to each
    paper_only = (paper_v2 | paper_v3) - (our_v2 | our_v3)
    our_only = (our_v2 | our_v3) - (paper_v2 | paper_v3)

    print(f"\nOverlap:")
    print(f"  Common DEGs (v2): {len(overlap_v2)}")
    print(f"  Common DEGs (v3): {len(overlap_v3)}")
    print(f"  Total common: {len(all_overlap_genes)}")
    print(f"\nUnique DEGs:")
    print(f"  Paper only: {len(paper_only)}")
    print(f"  Our only: {len(our_only)}")
    print(f"\nPercentages:")
    print(f"  Overlap: {len(all_overlap_genes)}/{len(paper_df)} ({len(all_overlap_genes)/len(paper_df)*100:.1f}%) of paper's DEGs")
    print(f"  Overlap: {len(all_overlap_genes)}/{len(our_df)} ({len(all_overlap_genes)/len(our_df)*100:.1f}%) of our DEGs")

    # Compare fold changes for overlapping genes
    if len(overlap_v2) > 0 or len(overlap_v3) > 0:
        print(f"\n{'-'*80}")
        print("Fold Change Comparison for Overlapping DEGs:")
        print(f"{'-'*80}")

        # Merge on v3 gene IDs (more complete)
        paper_merged = paper_df[['Gene_ID_v3', 'log2FoldChange']].copy()
        paper_merged.columns = ['Gene_ID_v3', 'Paper_LFC']
        our_merged = our_df[['Gene_ID_v3', 'log2FoldChange']].copy()
        our_merged.columns = ['Gene_ID_v3', 'Our_LFC']

        merged = paper_merged.merge(our_merged, on='Gene_ID_v3', how='inner')
        merged = merged.dropna()

        if len(merged) > 0:
            # Calculate correlation
            correlation = np.corrcoef(merged['Paper_LFC'], merged['Our_LFC'])[0,1]
            print(f"\nPearson correlation: {correlation:.3f}")

            # Direction agreement
            same_direction = ((merged['Paper_LFC'] > 0) == (merged['Our_LFC'] > 0)).sum()
            print(f"Same direction: {same_direction}/{len(merged)} ({same_direction/len(merged)*100:.1f}%)")

            # Show examples
            print(f"\nSample overlapping DEGs:")
            sample = merged.head(10)
            for idx, row in sample.iterrows():
                gene = row['Gene_ID_v3']
                paper_lfc = row['Paper_LFC']
                our_lfc = row['Our_LFC']
                direction = "✓" if (paper_lfc > 0) == (our_lfc > 0) else "✗"
                print(f"  {gene}: Paper={paper_lfc:6.2f}, Our={our_lfc:6.2f} {direction}")

            return {
                'comparison': comparison_name,
                'paper_degs': len(paper_df),
                'our_degs': len(our_df),
                'overlap': len(all_overlap_genes),
                'paper_only': len(paper_only),
                'our_only': len(our_only),
                'correlation': correlation,
                'same_direction_pct': same_direction/len(merged)*100,
                'merged_data': merged
            }

    return {
        'comparison': comparison_name,
        'paper_degs': len(paper_df),
        'our_degs': len(our_df),
        'overlap': len(all_overlap_genes),
        'paper_only': len(paper_only),
        'our_only': len(our_only),
        'correlation': None,
        'same_direction_pct': None,
        'merged_data': None
    }

# Compare in vitro
vitro_results = compare_degs(paper_vitro, our_vitro, "IN VITRO COMPARISON")

# Compare in vivo
vivo_results = compare_degs(paper_vivo, our_vivo, "IN VIVO COMPARISON")

# Check key genes from the paper
print("\n" + "="*80)
print("KEY GENES FROM PAPER")
print("="*80)

# Load official mappings
v2_to_v3 = pd.read_csv('official_mapping_v2_to_v3.tsv', sep='\t')
mapping_dict = dict(zip(v2_to_v3['Gene_ID_v2'], v2_to_v3['Gene_ID_v3']))

# Key genes mentioned in paper (v2 IDs)
key_genes = {
    'SCF1': 'B9J08_004109',
    'ALS4112': 'B9J08_004112',
    'IFF4109': 'B9J08_004109',  # Same as SCF1?
    'B9J08_001458': 'B9J08_001458',  # Top DEG from paper
}

print("\nChecking if key genes are DEGs in our analysis:")
for name, gene_v2 in key_genes.items():
    gene_v3 = mapping_dict.get(gene_v2, 'NOT_MAPPED')

    # Check in our DEG lists
    in_our_vitro = gene_v3 in our_vitro['Gene_ID_v3'].values
    in_our_vivo = gene_v3 in our_vivo['Gene_ID_v3'].values

    # Check in paper's DEG lists
    in_paper_vitro = gene_v2 in paper_vitro['Gene_ID_v2'].values
    in_paper_vivo = gene_v2 in paper_vivo['Gene_ID_v2'].values

    print(f"\n{name} ({gene_v2} / {gene_v3}):")
    print(f"  Paper in_vitro: {'YES ✓' if in_paper_vitro else 'NO'}")
    print(f"  Paper in_vivo:  {'YES ✓' if in_paper_vivo else 'NO'}")
    print(f"  Our in_vitro:   {'YES ✓' if in_our_vitro else 'NO'}")
    print(f"  Our in_vivo:    {'YES ✓' if in_our_vivo else 'NO'}")

    # Get fold changes if DEG
    if in_our_vitro:
        our_lfc = our_vitro[our_vitro['Gene_ID_v3'] == gene_v3]['log2FoldChange'].values[0]
        print(f"    Our in_vitro LFC: {our_lfc:.2f}")
    if in_our_vivo:
        our_lfc = our_vivo[our_vivo['Gene_ID_v3'] == gene_v3]['log2FoldChange'].values[0]
        print(f"    Our in_vivo LFC: {our_lfc:.2f}")
    if in_paper_vitro:
        paper_lfc = paper_vitro[paper_vitro['Gene_ID_v2'] == gene_v2]['log2FoldChange'].values[0]
        print(f"    Paper in_vitro LFC: {paper_lfc:.2f}")
    if in_paper_vivo:
        paper_lfc = paper_vivo[paper_vivo['Gene_ID_v2'] == gene_v2]['log2FoldChange'].values[0]
        print(f"    Paper in_vivo LFC: {paper_lfc:.2f}")

# Summary
print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

print("\nIN VITRO:")
print(f"  Paper found: {vitro_results['paper_degs']} DEGs")
print(f"  We found: {vitro_results['our_degs']} DEGs")
print(f"  Overlap: {vitro_results['overlap']} genes ({vitro_results['overlap']/vitro_results['paper_degs']*100:.1f}% of paper)")
if vitro_results['correlation'] is not None:
    print(f"  Correlation: {vitro_results['correlation']:.3f}")
    print(f"  Agreement: {vitro_results['same_direction_pct']:.1f}% same direction")

print("\nIN VIVO:")
print(f"  Paper found: {vivo_results['paper_degs']} DEGs")
print(f"  We found: {vivo_results['our_degs']} DEGs")
print(f"  Overlap: {vivo_results['overlap']} genes ({vivo_results['overlap']/vivo_results['paper_degs']*100:.1f}% of paper)")
if vivo_results['correlation'] is not None:
    print(f"  Correlation: {vivo_results['correlation']:.3f}")
    print(f"  Agreement: {vivo_results['same_direction_pct']:.1f}% same direction")

# Export detailed comparison
print("\n" + "="*80)
print("EXPORTING DETAILED COMPARISONS")
print("="*80)

if vitro_results['merged_data'] is not None:
    vitro_results['merged_data'].to_csv('vitro_deg_comparison.tsv', sep='\t', index=False)
    print("✓ Saved: vitro_deg_comparison.tsv")

if vivo_results['merged_data'] is not None:
    vivo_results['merged_data'].to_csv('vivo_deg_comparison.tsv', sep='\t', index=False)
    print("✓ Saved: vivo_deg_comparison.tsv")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
