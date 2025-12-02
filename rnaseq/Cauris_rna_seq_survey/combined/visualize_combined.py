#!/usr/bin/env python3
"""
Generate comprehensive visualizations for combined Candida auris RNA-seq literature survey.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Circle
from matplotlib_venn import venn3, venn3_circles

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

# Load data
df = pd.read_csv('/home/anton/git/claude-projects/rnaseq/Cauris_rna_seq_survey/combined/combined_data.csv')

# ============================================================================
# Figure 1: Comprehensive 6-panel overview
# ============================================================================

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Panel 1: Papers by year
ax1 = fig.add_subplot(gs[0, 0])
year_counts = df['year'].value_counts().sort_index()
ax1.bar(year_counts.index, year_counts.values, color='steelblue', edgecolor='black', linewidth=1.5)
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Papers', fontsize=12, fontweight='bold')
ax1.set_title('A. Publications by Year (2018-2025)', fontsize=13, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)
for i, v in enumerate(year_counts.values):
    ax1.text(year_counts.index[i], v + 0.2, str(v), ha='center', fontweight='bold')

# Panel 2: Papers by source (pie chart)
ax2 = fig.add_subplot(gs[0, 1])
source_summary = {
    'Claude\n(16 papers)': 16,
    'ChatGPT\n(9 papers)': 9,
    'GEO unique\n(7 papers)': 7
}
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
explode = (0.05, 0.05, 0.05)
wedges, texts, autotexts = ax2.pie(source_summary.values(), labels=source_summary.keys(),
                                     autopct='%1.1f%%', startangle=90, colors=colors,
                                     explode=explode, textprops={'fontsize': 11, 'fontweight': 'bold'})
ax2.set_title('B. Papers by Source\n(32 total unique papers)', fontsize=13, fontweight='bold')

# Panel 3: Genome references
ax3 = fig.add_subplot(gs[0, 2])
genome_counts = df['genome'].value_counts()
# Group small categories
genome_display = {}
for genome, count in genome_counts.items():
    if genome.startswith('B8441') or genome.startswith('GCA_002759435'):
        genome_display['B8441/GCA_002759435'] = genome_display.get('B8441/GCA_002759435', 0) + count
    elif genome == 'B11221':
        genome_display['B11221'] = count
    elif genome == 'N/A':
        genome_display['N/A'] = count
    else:
        genome_display['Other'] = genome_display.get('Other', 0) + count

genome_series = pd.Series(genome_display).sort_values(ascending=True)
ax3.barh(range(len(genome_series)), genome_series.values, color='darkorange', edgecolor='black', linewidth=1.5)
ax3.set_yticks(range(len(genome_series)))
ax3.set_yticklabels(genome_series.index, fontsize=11)
ax3.set_xlabel('Number of Studies', fontsize=12, fontweight='bold')
ax3.set_title('C. Genome Reference Versions', fontsize=13, fontweight='bold')
ax3.grid(axis='x', alpha=0.3)
for i, v in enumerate(genome_series.values):
    ax3.text(v + 0.3, i, str(v), va='center', fontweight='bold')

# Panel 4: Research focus
ax4 = fig.add_subplot(gs[1, :2])
focus_counts = df['focus'].value_counts().sort_values(ascending=True)
colors_focus = sns.color_palette('Set2', len(focus_counts))
ax4.barh(range(len(focus_counts)), focus_counts.values, color=colors_focus, edgecolor='black', linewidth=1.5)
ax4.set_yticks(range(len(focus_counts)))
ax4.set_yticklabels(focus_counts.index, fontsize=11)
ax4.set_xlabel('Number of Studies', fontsize=12, fontweight='bold')
ax4.set_title('D. Research Focus Areas', fontsize=13, fontweight='bold')
ax4.grid(axis='x', alpha=0.3)
for i, v in enumerate(focus_counts.values):
    ax4.text(v + 0.2, i, str(v), va='center', fontweight='bold')

# Panel 5: Source overlap Venn diagram
ax5 = fig.add_subplot(gs[1, 2])
# Claude: 16, ChatGPT: 9, GEO: 11
# Claude-ChatGPT overlap: 0
# Claude-GEO overlap: 2
# ChatGPT-GEO overlap: 2
# All three: 0
venn = venn3(subsets=(14, 7, 2, 7, 0, 2, 0),
             set_labels=('Claude\n(16)', 'ChatGPT\n(9)', 'GEO\n(11)'),
             set_colors=('#FF6B6B', '#4ECDC4', '#45B7D1'),
             alpha=0.6, ax=ax5)
for text in venn.set_labels:
    if text:
        text.set_fontsize(11)
        text.set_fontweight('bold')
for text in venn.subset_labels:
    if text:
        text.set_fontsize(10)
        text.set_fontweight('bold')
ax5.set_title('E. Survey Source Overlap\n(32 unique papers)', fontsize=13, fontweight='bold')

# Panel 6: Timeline with focus markers
ax6 = fig.add_subplot(gs[2, :])
# Create timeline plot
for idx, row in df.iterrows():
    year = row['year']
    focus = row['focus']
    source = row['source']

    # Assign y-position based on source
    if 'Claude' in source:
        y_pos = 3
        color = '#FF6B6B'
    elif 'ChatGPT' in source:
        y_pos = 2
        color = '#4ECDC4'
    else:  # GEO
        y_pos = 1
        color = '#45B7D1'

    # Add jitter to avoid overlap
    y_jitter = y_pos + np.random.uniform(-0.15, 0.15)

    ax6.scatter(year, y_jitter, s=100, c=[color], edgecolor='black', linewidth=1.5, alpha=0.7, zorder=3)

ax6.set_xlabel('Year', fontsize=12, fontweight='bold')
ax6.set_ylabel('Source', fontsize=12, fontweight='bold')
ax6.set_yticks([1, 2, 3])
ax6.set_yticklabels(['GEO', 'ChatGPT', 'Claude'], fontsize=11)
ax6.set_title('F. Publication Timeline by Source', fontsize=13, fontweight='bold')
ax6.grid(axis='both', alpha=0.3)
ax6.set_xlim(2017.5, 2025.5)
ax6.set_ylim(0.5, 3.5)

plt.tight_layout()
plt.savefig('/home/anton/git/claude-projects/rnaseq/Cauris_rna_seq_survey/combined/combined_overview.png',
            bbox_inches='tight', dpi=300)
print("Saved: combined_overview.png")
plt.close()

# ============================================================================
# Figure 2: Detailed comparison charts
# ============================================================================

fig2, axes = plt.subplots(2, 2, figsize=(16, 12))

# Chart 1: Cumulative papers over time by source
ax = axes[0, 0]
years = sorted(df['year'].unique())
claude_cumsum = []
chatgpt_cumsum = []
geo_cumsum = []

for year in years:
    claude_cumsum.append(len(df[(df['source'].str.contains('Claude')) & (df['year'] <= year)]))
    chatgpt_cumsum.append(len(df[(df['source'] == 'ChatGPT') & (df['year'] <= year)]))
    geo_cumsum.append(len(df[(df['in_geo'] == True) & (df['year'] <= year)]))

ax.plot(years, claude_cumsum, marker='o', linewidth=3, markersize=8, label='Claude', color='#FF6B6B')
ax.plot(years, chatgpt_cumsum, marker='s', linewidth=3, markersize=8, label='ChatGPT', color='#4ECDC4')
ax.plot(years, geo_cumsum, marker='^', linewidth=3, markersize=8, label='GEO', color='#45B7D1')
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Cumulative Papers', fontsize=12, fontweight='bold')
ax.set_title('A. Cumulative Papers Over Time', fontsize=13, fontweight='bold')
ax.legend(fontsize=11, frameon=True, shadow=True)
ax.grid(True, alpha=0.3)

# Chart 2: Drug resistance papers by year
ax = axes[0, 1]
drug_by_year = df[df['focus'] == 'Drug resistance'].groupby('year').size()
years_drug = drug_by_year.index
ax.bar(years_drug, drug_by_year.values, color='crimson', edgecolor='black', linewidth=1.5, alpha=0.7)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Papers', fontsize=12, fontweight='bold')
ax.set_title('B. Drug Resistance Studies by Year\n(11 papers, 34.4% of total)', fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.3)
for i, v in enumerate(drug_by_year.values):
    ax.text(years_drug[i], v + 0.1, str(v), ha='center', fontweight='bold')

# Chart 3: Source composition by year
ax = axes[1, 0]
year_source_data = []
for year in sorted(df['year'].unique()):
    year_df = df[df['year'] == year]
    claude_count = len(year_df[year_df['source'].str.contains('Claude')])
    chatgpt_count = len(year_df[year_df['source'] == 'ChatGPT'])
    geo_count = len(year_df[year_df['source'] == 'GEO'])
    year_source_data.append([year, claude_count, chatgpt_count, geo_count])

year_source_df = pd.DataFrame(year_source_data, columns=['Year', 'Claude', 'ChatGPT', 'GEO'])
x = np.arange(len(year_source_df))
width = 0.6
ax.bar(x, year_source_df['Claude'], width, label='Claude', color='#FF6B6B', edgecolor='black', linewidth=1)
ax.bar(x, year_source_df['ChatGPT'], width, bottom=year_source_df['Claude'],
       label='ChatGPT', color='#4ECDC4', edgecolor='black', linewidth=1)
ax.bar(x, year_source_df['GEO'], width,
       bottom=year_source_df['Claude'] + year_source_df['ChatGPT'],
       label='GEO', color='#45B7D1', edgecolor='black', linewidth=1)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Number of Papers', fontsize=12, fontweight='bold')
ax.set_title('C. Source Composition by Year', fontsize=13, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(year_source_df['Year'])
ax.legend(fontsize=11, frameon=True, shadow=True)
ax.grid(axis='y', alpha=0.3)

# Chart 4: Research focus distribution by source
ax = axes[1, 1]
focus_source_data = []
for focus in df['focus'].unique():
    focus_df = df[df['focus'] == focus]
    claude_count = len(focus_df[focus_df['source'].str.contains('Claude')])
    chatgpt_count = len(focus_df[focus_df['source'] == 'ChatGPT'])
    geo_count = len(focus_df[focus_df['source'] == 'GEO'])
    focus_source_data.append([focus, claude_count, chatgpt_count, geo_count])

focus_source_df = pd.DataFrame(focus_source_data, columns=['Focus', 'Claude', 'ChatGPT', 'GEO'])
focus_source_df = focus_source_df.sort_values('Claude', ascending=True)
x = np.arange(len(focus_source_df))
width = 0.25
ax.barh(x - width, focus_source_df['Claude'], width, label='Claude', color='#FF6B6B', edgecolor='black', linewidth=1)
ax.barh(x, focus_source_df['ChatGPT'], width, label='ChatGPT', color='#4ECDC4', edgecolor='black', linewidth=1)
ax.barh(x + width, focus_source_df['GEO'], width, label='GEO', color='#45B7D1', edgecolor='black', linewidth=1)
ax.set_yticks(x)
ax.set_yticklabels(focus_source_df['Focus'], fontsize=10)
ax.set_xlabel('Number of Papers', fontsize=12, fontweight='bold')
ax.set_title('D. Research Focus by Source', fontsize=13, fontweight='bold')
ax.legend(fontsize=11, frameon=True, shadow=True)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('/home/anton/git/claude-projects/rnaseq/Cauris_rna_seq_survey/combined/combined_analysis.png',
            bbox_inches='tight', dpi=300)
print("Saved: combined_analysis.png")
plt.close()

# ============================================================================
# Figure 3: Summary statistics table
# ============================================================================

fig3, ax = plt.subplots(figsize=(12, 10))
ax.axis('tight')
ax.axis('off')

# Create summary statistics
stats_data = [
    ['Metric', 'Value'],
    ['', ''],
    ['DATASET OVERVIEW', ''],
    ['Total unique papers', '32'],
    ['Date range', '2018-2025'],
    ['Average papers per year', '4.0'],
    ['', ''],
    ['PAPERS BY SOURCE', ''],
    ['Claude survey (PubMed + Europe PMC + Repository)', '16 (50.0%)'],
    ['ChatGPT survey (PubMed + Europe PMC)', '9 (28.1%)'],
    ['GEO database survey', '11 (34.4%)'],
    ['Unique papers (after deduplication)', '32'],
    ['', ''],
    ['SOURCE OVERLAP', ''],
    ['Claude-ChatGPT overlap', '0 (0.0%)'],
    ['Claude-GEO overlap', '2 (6.2%)'],
    ['ChatGPT-GEO overlap', '2 (6.2%)'],
    ['Three-way overlap', '0 (0.0%)'],
    ['', ''],
    ['GENOME REFERENCES', ''],
    ['B8441/GCA_002759435 family', '24 (75.0%)'],
    ['B11221', '3 (9.4%)'],
    ['Other/N/A', '5 (15.6%)'],
    ['', ''],
    ['RESEARCH FOCUS', ''],
    ['Drug resistance', '11 (34.4%)'],
    ['Stress response', '6 (18.8%)'],
    ['Biofilm formation', '4 (12.5%)'],
    ['Host-pathogen interactions', '4 (12.5%)'],
    ['Adhesin function', '3 (9.4%)'],
    ['Morphotype variation', '2 (6.2%)'],
    ['Other', '2 (6.2%)'],
    ['', ''],
    ['PUBLICATION TRENDS', ''],
    ['Peak year', '2021 (11 papers)'],
    ['Most recent papers', '2025 (2 papers)'],
    ['Earliest papers', '2018 (2 papers)'],
]

table = ax.table(cellText=stats_data, cellLoc='left', loc='center',
                colWidths=[0.6, 0.4])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header row
for i in range(2):
    cell = table[(0, i)]
    cell.set_facecolor('#4A90E2')
    cell.set_text_props(weight='bold', color='white', fontsize=13)

# Style section headers
section_rows = [2, 7, 12, 17, 23, 30]
for row in section_rows:
    cell = table[(row, 0)]
    cell.set_facecolor('#E8F4F8')
    cell.set_text_props(weight='bold', fontsize=12)
    cell = table[(row, 1)]
    cell.set_facecolor('#E8F4F8')

# Color alternating rows
for i in range(len(stats_data)):
    if i not in [0] + section_rows and i % 2 == 0:
        for j in range(2):
            table[(i, j)].set_facecolor('#F5F5F5')

plt.title('Combined RNA-seq Literature Survey: Summary Statistics\nCandida auris (2018-2025)',
          fontsize=16, fontweight='bold', pad=20)
plt.savefig('/home/anton/git/claude-projects/rnaseq/Cauris_rna_seq_survey/combined/combined_statistics.png',
            bbox_inches='tight', dpi=300)
print("Saved: combined_statistics.png")
plt.close()

print("\nAll visualizations generated successfully!")
print("Files created:")
print("  - combined_overview.png")
print("  - combined_analysis.png")
print("  - combined_statistics.png")
