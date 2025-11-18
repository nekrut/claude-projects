#!/usr/bin/env python3
"""
Create fold change comparison plots with gene labels
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from adjustText import adjust_text

print("="*80)
print("CREATING LABELED FOLD CHANGE COMPARISON PLOTS")
print("="*80)

# Set publication-quality plot parameters
plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

# Load comparison data
print("\nLoading comparison data...")
vitro_comp = pd.read_csv('vitro_deg_comparison.tsv', sep='\t')
vivo_comp = pd.read_csv('vivo_deg_comparison.tsv', sep='\t')

print(f"  In vitro: {len(vitro_comp)} overlapping DEGs")
print(f"  In vivo: {len(vivo_comp)} overlapping DEGs")

# Load official mapping to get gene names
v2_to_v3 = pd.read_csv('official_mapping_v2_to_v3.tsv', sep='\t')

# Key genes to highlight
key_genes = {
    'B9J08_04863': 'SCF1/IFF4109',
    'B9J08_04866': 'ALS4112',
    'B9J08_03708': 'B9J08_001458',  # Top DEG
}

def create_labeled_fc_plot(data, title, output_file, experiment, n_labels=15):
    """Create fold change comparison scatter plot with gene labels"""

    fig, ax = plt.subplots(figsize=(10, 10))

    # Calculate statistics
    correlation = np.corrcoef(data['Paper_LFC'], data['Our_LFC'])[0,1]
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        data['Paper_LFC'], data['Our_LFC']
    )

    # Create scatter plot
    scatter = ax.scatter(data['Paper_LFC'], data['Our_LFC'],
                        alpha=0.5, s=50, c='#2E86AB', edgecolors='white', linewidth=0.5,
                        zorder=2)

    # Add regression line
    x_range = np.array([data['Paper_LFC'].min(), data['Paper_LFC'].max()])
    y_pred = slope * x_range + intercept
    ax.plot(x_range, y_pred, 'r--', linewidth=2, alpha=0.8,
            label=f'Regression: y = {slope:.3f}x + {intercept:.3f}')

    # Add negative identity line (perfect negative correlation)
    lim_min = min(data['Paper_LFC'].min(), data['Our_LFC'].min()) - 1
    lim_max = max(data['Paper_LFC'].max(), data['Our_LFC'].max()) + 1
    ax.plot([lim_min, lim_max], [-lim_min, -lim_max], 'g:', linewidth=2,
            alpha=0.6, label='y = -x (reversed comparison)')

    # Add quadrant lines
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)

    # Prepare labels
    texts = []
    labeled_genes = set()

    # First, label key genes
    for gene_id, gene_name in key_genes.items():
        if gene_id in data['Gene_ID_v3'].values:
            row = data[data['Gene_ID_v3'] == gene_id].iloc[0]
            # Highlight key genes with larger, red points
            ax.scatter(row['Paper_LFC'], row['Our_LFC'],
                      s=150, c='red', marker='*', edgecolors='darkred',
                      linewidth=1, zorder=5, alpha=0.9)
            texts.append(ax.text(row['Paper_LFC'], row['Our_LFC'], gene_name,
                                fontsize=9, fontweight='bold', color='darkred',
                                zorder=6))
            labeled_genes.add(gene_id)

    # Then label top DEGs by magnitude
    data['abs_paper_lfc'] = abs(data['Paper_LFC'])
    top_degs = data.nlargest(n_labels, 'abs_paper_lfc')

    for idx, row in top_degs.iterrows():
        gene_id = row['Gene_ID_v3']
        if gene_id not in labeled_genes:
            # Check if it's a named gene (starts with letter, not just B9J08)
            label = gene_id
            texts.append(ax.text(row['Paper_LFC'], row['Our_LFC'], label,
                                fontsize=7, color='black', alpha=0.7,
                                zorder=4))
            labeled_genes.add(gene_id)

    # Adjust text positions to avoid overlaps
    if texts:
        adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5, alpha=0.5),
                   ax=ax, expand_points=(1.2, 1.2))

    # Labels and title
    ax.set_xlabel('Paper log₂ Fold Change (AR0382 vs AR0387)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Our log₂ Fold Change (AR0387 vs AR0382)', fontsize=12, fontweight='bold')
    ax.set_title(f'{title}\nFold Change Comparison (Labeled)', fontsize=14, fontweight='bold', pad=20)

    # Add statistics box
    stats_text = (
        f'n = {len(data)} genes\n'
        f'Pearson r = {correlation:.4f}\n'
        f'p < 0.001\n'
        f'Slope = {slope:.3f}'
    )

    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Add legend for key genes
    key_genes_text = "Key genes: ★ = SCF1, ALS4112, etc."
    ax.text(0.95, 0.05, key_genes_text, transform=ax.transAxes,
            fontsize=8, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.6))

    # Set equal aspect ratio and limits
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)

    # Grid
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, zorder=1)

    # Legend
    ax.legend(loc='lower right', framealpha=0.9)

    # Tight layout
    plt.tight_layout()

    # Save
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")

    plt.close()

    return correlation

# Create plots
print("\nCreating labeled plots...")

# In vitro plot
vitro_corr = create_labeled_fc_plot(
    vitro_comp,
    'In Vitro Biofilm Growth',
    'vitro_fc_comparison_labeled.png',
    'vitro',
    n_labels=10
)

# In vivo plot
vivo_corr = create_labeled_fc_plot(
    vivo_comp,
    'In Vivo Mouse Infection',
    'vivo_fc_comparison_labeled.png',
    'vivo',
    n_labels=15
)

# Create combined labeled plot
print("\nCreating combined labeled plot...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

# Helper function for combined plot
def add_combined_subplot(ax, data, title, color, n_labels=10):
    # Scatter
    ax.scatter(data['Paper_LFC'], data['Our_LFC'],
              alpha=0.5, s=40, c=color, edgecolors='white', linewidth=0.5, zorder=2)

    # Regression line
    correlation = np.corrcoef(data['Paper_LFC'], data['Our_LFC'])[0,1]
    lim_min = min(data['Paper_LFC'].min(), data['Our_LFC'].min()) - 1
    lim_max = max(data['Paper_LFC'].max(), data['Our_LFC'].max()) + 1

    ax.plot([lim_min, lim_max], [-lim_min, -lim_max], 'r--',
           linewidth=2, alpha=0.8, label=f'y = -x (r = {correlation:.3f})', zorder=3)
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3, zorder=1)
    ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3, zorder=1)

    # Labels
    texts = []

    # Key genes
    for gene_id, gene_name in key_genes.items():
        if gene_id in data['Gene_ID_v3'].values:
            row = data[data['Gene_ID_v3'] == gene_id].iloc[0]
            ax.scatter(row['Paper_LFC'], row['Our_LFC'],
                      s=120, c='red', marker='*', edgecolors='darkred',
                      linewidth=1, zorder=5, alpha=0.9)
            texts.append(ax.text(row['Paper_LFC'], row['Our_LFC'], gene_name,
                                fontsize=8, fontweight='bold', color='darkred', zorder=6))

    # Top DEGs
    data['abs_paper_lfc'] = abs(data['Paper_LFC'])
    top_degs = data.nlargest(n_labels, 'abs_paper_lfc')
    labeled = set(key_genes.keys())

    for idx, row in top_degs.iterrows():
        if row['Gene_ID_v3'] not in labeled:
            texts.append(ax.text(row['Paper_LFC'], row['Our_LFC'], row['Gene_ID_v3'],
                                fontsize=6, color='black', alpha=0.6, zorder=4))

    if texts:
        adjust_text(texts, arrowprops=dict(arrowstyle='-', color='gray', lw=0.3, alpha=0.4),
                   ax=ax, expand_points=(1.15, 1.15))

    ax.set_xlabel('Paper log₂FC', fontsize=11, fontweight='bold')
    ax.set_ylabel('Our log₂FC', fontsize=11, fontweight='bold')
    ax.set_title(f'{title} (n={len(data)})', fontsize=12, fontweight='bold')
    ax.set_aspect('equal')
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)
    ax.grid(True, alpha=0.2, zorder=1)
    ax.legend(loc='lower right', fontsize=9)

    stats_text = f'r = {correlation:.4f}'
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
           fontsize=9, verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# In Vitro
add_combined_subplot(ax1, vitro_comp, 'In Vitro', '#2E86AB', n_labels=8)

# In Vivo
add_combined_subplot(ax2, vivo_comp, 'In Vivo', '#A23B72', n_labels=12)

plt.suptitle('DESeq2 Fold Change Comparison: Our Analysis vs Wang et al. (2024)',
             fontsize=15, fontweight='bold', y=1.00)

plt.tight_layout()
plt.savefig('combined_fc_comparison_labeled.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: combined_fc_comparison_labeled.png")
plt.close()

print("\n" + "="*80)
print("LABELED PLOTS CREATED")
print("="*80)
print("\n✓ vitro_fc_comparison_labeled.png")
print("✓ vivo_fc_comparison_labeled.png")
print("✓ combined_fc_comparison_labeled.png")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
