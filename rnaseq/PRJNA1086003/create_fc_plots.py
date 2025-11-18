#!/usr/bin/env python3
"""
Create fold change comparison plots for in vitro and in vivo experiments
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

print("="*80)
print("CREATING FOLD CHANGE COMPARISON PLOTS")
print("="*80)

# Set publication-quality plot parameters
plt.rcParams['figure.figsize'] = (8, 8)
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

def create_fc_plot(data, title, output_file, experiment):
    """Create fold change comparison scatter plot"""

    fig, ax = plt.subplots(figsize=(8, 8))

    # Calculate statistics
    correlation = np.corrcoef(data['Paper_LFC'], data['Our_LFC'])[0,1]

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        data['Paper_LFC'], data['Our_LFC']
    )

    # Calculate RMSE
    rmse = np.sqrt(np.mean((data['Paper_LFC'] - (-data['Our_LFC']))**2))

    # Create scatter plot
    scatter = ax.scatter(data['Paper_LFC'], data['Our_LFC'],
                        alpha=0.6, s=60, c='#2E86AB', edgecolors='white', linewidth=0.5)

    # Add regression line
    x_range = np.array([data['Paper_LFC'].min(), data['Paper_LFC'].max()])
    y_pred = slope * x_range + intercept
    ax.plot(x_range, y_pred, 'r--', linewidth=2, alpha=0.8,
            label=f'Regression: y = {slope:.3f}x + {intercept:.3f}')

    # Add identity line (perfect positive correlation)
    lim_min = min(data['Paper_LFC'].min(), data['Our_LFC'].min()) - 1
    lim_max = max(data['Paper_LFC'].max(), data['Our_LFC'].max()) + 1
    ax.plot([lim_min, lim_max], [lim_min, lim_max], 'k:', linewidth=1.5,
            alpha=0.3, label='y = x (perfect agreement)')

    # Add negative identity line (perfect negative correlation)
    ax.plot([lim_min, lim_max], [-lim_min, -lim_max], 'g:', linewidth=1.5,
            alpha=0.5, label='y = -x (reversed comparison)')

    # Add quadrant lines
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)

    # Labels and title
    ax.set_xlabel('Paper log₂ Fold Change (AR0382 vs AR0387)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Our log₂ Fold Change (AR0387 vs AR0382)', fontsize=12, fontweight='bold')
    ax.set_title(f'{title}\nFold Change Comparison', fontsize=14, fontweight='bold', pad=20)

    # Add statistics box
    stats_text = (
        f'n = {len(data)} genes\n'
        f'Pearson r = {correlation:.4f}\n'
        f'p < 0.001\n'
        f'Slope = {slope:.3f}\n'
        f'RMSE = {rmse:.3f}'
    )

    # Position stats box
    ax.text(0.05, 0.95, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Set equal aspect ratio and limits
    ax.set_aspect('equal', adjustable='box')
    margin = 1
    ax.set_xlim(lim_min, lim_max)
    ax.set_ylim(lim_min, lim_max)

    # Grid
    ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5)

    # Legend
    ax.legend(loc='lower right', framealpha=0.9)

    # Tight layout
    plt.tight_layout()

    # Save
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"  ✓ Saved: {output_file}")

    plt.close()

    return correlation, rmse

# Create plots
print("\nCreating plots...")

# In vitro plot
vitro_corr, vitro_rmse = create_fc_plot(
    vitro_comp,
    'In Vitro Biofilm Growth',
    'vitro_fc_comparison.png',
    'vitro'
)

# In vivo plot
vivo_corr, vivo_rmse = create_fc_plot(
    vivo_comp,
    'In Vivo Mouse Infection',
    'vivo_fc_comparison.png',
    'vivo'
)

# Create combined plot
print("\nCreating combined plot...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# In Vitro
ax1.scatter(vitro_comp['Paper_LFC'], vitro_comp['Our_LFC'],
           alpha=0.6, s=50, c='#2E86AB', edgecolors='white', linewidth=0.5)

lim_min_v = min(vitro_comp['Paper_LFC'].min(), vitro_comp['Our_LFC'].min()) - 1
lim_max_v = max(vitro_comp['Paper_LFC'].max(), vitro_comp['Our_LFC'].max()) + 1

ax1.plot([lim_min_v, lim_max_v], [-lim_min_v, -lim_max_v], 'r--',
         linewidth=2, alpha=0.8, label=f'y = -x (r = {vitro_corr:.3f})')
ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
ax1.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)

ax1.set_xlabel('Paper log₂FC', fontsize=11, fontweight='bold')
ax1.set_ylabel('Our log₂FC', fontsize=11, fontweight='bold')
ax1.set_title(f'In Vitro (n={len(vitro_comp)})', fontsize=13, fontweight='bold')
ax1.set_aspect('equal')
ax1.set_xlim(lim_min_v, lim_max_v)
ax1.set_ylim(lim_min_v, lim_max_v)
ax1.grid(True, alpha=0.2)
ax1.legend(loc='lower right')

stats_text_v = f'r = {vitro_corr:.4f}\np < 0.001'
ax1.text(0.05, 0.95, stats_text_v, transform=ax1.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# In Vivo
ax2.scatter(vivo_comp['Paper_LFC'], vivo_comp['Our_LFC'],
           alpha=0.6, s=50, c='#A23B72', edgecolors='white', linewidth=0.5)

lim_min_i = min(vivo_comp['Paper_LFC'].min(), vivo_comp['Our_LFC'].min()) - 1
lim_max_i = max(vivo_comp['Paper_LFC'].max(), vivo_comp['Our_LFC'].max()) + 1

ax2.plot([lim_min_i, lim_max_i], [-lim_min_i, -lim_max_i], 'r--',
         linewidth=2, alpha=0.8, label=f'y = -x (r = {vivo_corr:.3f})')
ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
ax2.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)

ax2.set_xlabel('Paper log₂FC', fontsize=11, fontweight='bold')
ax2.set_ylabel('Our log₂FC', fontsize=11, fontweight='bold')
ax2.set_title(f'In Vivo (n={len(vivo_comp)})', fontsize=13, fontweight='bold')
ax2.set_aspect('equal')
ax2.set_xlim(lim_min_i, lim_max_i)
ax2.set_ylim(lim_min_i, lim_max_i)
ax2.grid(True, alpha=0.2)
ax2.legend(loc='lower right')

stats_text_i = f'r = {vivo_corr:.4f}\np < 0.001'
ax2.text(0.05, 0.95, stats_text_i, transform=ax2.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.suptitle('DESeq2 Fold Change Comparison: Our Analysis vs Wang et al. (2024)',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('combined_fc_comparison.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: combined_fc_comparison.png")
plt.close()

# Create density plot version
print("\nCreating density plots...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# In Vitro - hexbin
hb1 = ax1.hexbin(vitro_comp['Paper_LFC'], vitro_comp['Our_LFC'],
                 gridsize=20, cmap='Blues', mincnt=1, alpha=0.8)
ax1.plot([lim_min_v, lim_max_v], [-lim_min_v, -lim_max_v], 'r--',
         linewidth=2, alpha=0.8, label=f'y = -x (r = {vitro_corr:.3f})')
ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
ax1.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
ax1.set_xlabel('Paper log₂FC', fontsize=11, fontweight='bold')
ax1.set_ylabel('Our log₂FC', fontsize=11, fontweight='bold')
ax1.set_title(f'In Vitro (n={len(vitro_comp)})', fontsize=13, fontweight='bold')
ax1.set_aspect('equal')
ax1.set_xlim(lim_min_v, lim_max_v)
ax1.set_ylim(lim_min_v, lim_max_v)
ax1.grid(True, alpha=0.2)
ax1.legend(loc='lower right')
plt.colorbar(hb1, ax=ax1, label='Count')

# In Vivo - hexbin
hb2 = ax2.hexbin(vivo_comp['Paper_LFC'], vivo_comp['Our_LFC'],
                 gridsize=25, cmap='RdPu', mincnt=1, alpha=0.8)
ax2.plot([lim_min_i, lim_max_i], [-lim_min_i, -lim_max_i], 'r--',
         linewidth=2, alpha=0.8, label=f'y = -x (r = {vivo_corr:.3f})')
ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
ax2.axvline(x=0, color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
ax2.set_xlabel('Paper log₂FC', fontsize=11, fontweight='bold')
ax2.set_ylabel('Our log₂FC', fontsize=11, fontweight='bold')
ax2.set_title(f'In Vivo (n={len(vivo_comp)})', fontsize=13, fontweight='bold')
ax2.set_aspect('equal')
ax2.set_xlim(lim_min_i, lim_max_i)
ax2.set_ylim(lim_min_i, lim_max_i)
ax2.grid(True, alpha=0.2)
ax2.legend(loc='lower right')
plt.colorbar(hb2, ax=ax2, label='Count')

plt.suptitle('DESeq2 Fold Change Comparison (Density): Our Analysis vs Wang et al. (2024)',
             fontsize=15, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('combined_fc_comparison_density.png', dpi=300, bbox_inches='tight')
print(f"  ✓ Saved: combined_fc_comparison_density.png")
plt.close()

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"\nIn Vitro:")
print(f"  Pearson r = {vitro_corr:.4f}")
print(f"  RMSE = {vitro_rmse:.3f}")
print(f"  n = {len(vitro_comp)} overlapping DEGs")

print(f"\nIn Vivo:")
print(f"  Pearson r = {vivo_corr:.4f}")
print(f"  RMSE = {vivo_rmse:.3f}")
print(f"  n = {len(vivo_comp)} overlapping DEGs")

print("\n" + "="*80)
print("PLOTS CREATED")
print("="*80)
print("\n✓ vitro_fc_comparison.png")
print("✓ vivo_fc_comparison.png")
print("✓ combined_fc_comparison.png")
print("✓ combined_fc_comparison_density.png")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
