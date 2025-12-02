#!/usr/bin/env python3
"""
Visualizations for Candida auris RNA-seq Literature Survey

This script creates comprehensive visualizations summarizing the survey findings.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
from matplotlib.patches import Rectangle
import re

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Survey data (16 papers including repository analysis)
survey_data = [
    {'pmid': '32581078', 'year': 2020, 'source': 'PubMed',
     'genome': 'N/A', 'type': 'Biofilm vs planktonic',
     'tools': 'N/A', 'focus': 'biofilm'},

    {'pmid': '33937102', 'year': 2021, 'source': 'PubMed',
     'genome': 'B11221', 'type': 'Clinical isolate comparison',
     'tools': 'FastQC, cutadapt, NextGenMap, Picard, HTseq, edgeR, clusterProfiler',
     'focus': 'clinical_variation'},

    {'pmid': '34354695', 'year': 2021, 'source': 'PubMed',
     'genome': 'N/A', 'type': 'Drug resistance',
     'tools': 'HISAT2, Cufflinks, HTSeq-count, DEseq, Trimmomatic, pheatmap, STRING',
     'focus': 'drug_resistance'},

    {'pmid': '34485470', 'year': 2021, 'source': 'PubMed',
     'genome': 'GCA_002759435', 'type': 'Farnesol response',
     'tools': 'DESeq, StrandNGS, Agilent BioAnalyzer, NEBNext Ultra II',
     'focus': 'stress_response'},

    {'pmid': '34630944', 'year': 2021, 'source': 'Europe PMC',
     'genome': 'B8441', 'type': 'Caspofungin response',
     'tools': 'CLC Genomics Workbench, TMM, EdgeR, DAVID, BLASTp, qRT-PCR',
     'focus': 'drug_resistance'},

    {'pmid': '34788438', 'year': 2021, 'source': 'PubMed',
     'genome': 'B8441', 'type': 'Small RNA / EV',
     'tools': 'CLC Genomics Workbench, TMM, TruSeq small RNA, qRT-PCR',
     'focus': 'small_rna'},

    {'pmid': '35652307', 'year': 2022, 'source': 'PubMed',
     'genome': 'B8441', 'type': 'AmB resistance',
     'tools': 'HISAT2, HTSeq, DESeq2, Orange3, BioVenn, Fungifun2',
     'focus': 'drug_resistance'},

    {'pmid': '35968956', 'year': 2022, 'source': 'Europe PMC',
     'genome': 'B8441', 'type': 'Echinocandin resistance',
     'tools': 'FastQC, cutadapt, NextGenMap, Picard, HTseq, edgeR, clusterProfiler, VennDiagram',
     'focus': 'drug_resistance'},

    {'pmid': '36913408', 'year': 2023, 'source': 'Europe PMC',
     'genome': 'GCA_002759435', 'type': 'Biofilm / aggregation',
     'tools': 'HiSat2, Stringtie, DESeq2, Illumina NovaSeq',
     'focus': 'biofilm'},

    {'pmid': '37350781', 'year': 2023, 'source': 'PubMed',
     'genome': 'B11221', 'type': 'Morphotype variation',
     'tools': 'Bowtie2, HISAT2, HTSeq, DESeq, topGO, KOBAS, Pheatmap',
     'focus': 'morphology'},

    {'pmid': '37769084', 'year': 2023, 'source': 'Repository Analysis',
     'genome': 'GCA_002759435.3', 'type': 'SCF1 adhesin',
     'tools': 'FastQC, fastp, STAR, featureCounts, DESeq2',
     'focus': 'biofilm'},

    {'pmid': '38562758', 'year': 2024, 'source': 'Repository Analysis',
     'genome': 'GCA_002759435', 'type': 'Adhesin redundancy',
     'tools': 'DESeq2, Galaxy pipeline, STAR, featureCounts',
     'focus': 'biofilm'},

    {'pmid': '38990436', 'year': 2024, 'source': 'PubMed',
     'genome': 'N/A', 'type': 'Host-pathogen',
     'tools': 'qRT-PCR, flow cytometry, KEGG, Reactome',
     'focus': 'host_response'},

    {'pmid': 'PMC11385638', 'year': 2024, 'source': 'PubMed',
     'genome': 'B11221', 'type': 'AmB sensitivity',
     'tools': 'DESeq2, KEGG, Gene Ontology, STRING, qPCR, Illumina NovaSeq',
     'focus': 'drug_resistance'},

    {'pmid': 'PMC11459930', 'year': 2024, 'source': 'Europe PMC',
     'genome': 'B8441', 'type': 'Pan-drug resistance',
     'tools': 'HISAT2, StringTie, Ballgown, BiNGO, HMMER, CLC Genomics Server',
     'focus': 'drug_resistance'},

    {'pmid': '40099908', 'year': 2025, 'source': 'Europe PMC',
     'genome': 'B8441', 'type': 'Flucytosine resistance',
     'tools': 'STAR, drc R package, IGV, enrichGO, clusterProfiler, Sanger sequencing',
     'focus': 'drug_resistance'},
]

df = pd.DataFrame(survey_data)

# Extract individual tools
def extract_tools(tools_str):
    """Extract individual tools from comma-separated string."""
    if tools_str == 'N/A':
        return []
    tools = [t.strip() for t in tools_str.split(',')]
    # Clean up version numbers and extra text
    cleaned = []
    for tool in tools:
        # Remove version numbers
        tool = re.sub(r'v?\d+\.\d+[\.\d]*', '', tool)
        # Remove extra descriptors
        tool = re.sub(r'\([^)]*\)', '', tool)
        tool = tool.strip()
        if tool:
            cleaned.append(tool)
    return cleaned

df['tool_list'] = df['tools'].apply(extract_tools)

# Create figure with multiple subplots
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Color palette
colors = sns.color_palette("husl", 8)

# ============================================================================
# 1. Papers by Year (Top Left)
# ============================================================================
ax1 = fig.add_subplot(gs[0, 0])
year_counts = df['year'].value_counts().sort_index()
bars = ax1.bar(year_counts.index, year_counts.values, color=colors[0],
               edgecolor='black', linewidth=1.5)
ax1.set_xlabel('Publication Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Number of Papers', fontsize=12, fontweight='bold')
ax1.set_title('Publications by Year', fontsize=14, fontweight='bold', pad=15)
ax1.grid(axis='y', alpha=0.3)
ax1.set_xticks(year_counts.index)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# ============================================================================
# 2. Papers by Data Source (Top Middle)
# ============================================================================
ax2 = fig.add_subplot(gs[0, 1])
source_counts = df['source'].value_counts()
colors_pie = [colors[1], colors[2], colors[3]]
wedges, texts, autotexts = ax2.pie(source_counts.values,
                                     labels=source_counts.index,
                                     autopct='%1.1f%%',
                                     colors=colors_pie,
                                     startangle=90,
                                     explode=[0.05]*len(source_counts),
                                     textprops={'fontsize': 11, 'fontweight': 'bold'})
ax2.set_title('Papers by Data Source', fontsize=14, fontweight='bold', pad=15)

# ============================================================================
# 3. Genome Reference Versions (Top Right)
# ============================================================================
ax3 = fig.add_subplot(gs[0, 2])
genome_clean = df['genome'].replace('N/A', 'Not Specified')
# Extract base genome ID
genome_base = genome_clean.str.extract(r'(B\d+|GCA_\d+)', expand=False).fillna('Not Specified')
genome_counts = genome_base.value_counts()

bars = ax3.barh(range(len(genome_counts)), genome_counts.values, color=colors[4],
                edgecolor='black', linewidth=1.5)
ax3.set_yticks(range(len(genome_counts)))
ax3.set_yticklabels(genome_counts.index, fontsize=11)
ax3.set_xlabel('Number of Papers', fontsize=12, fontweight='bold')
ax3.set_title('Genome Reference Versions', fontsize=14, fontweight='bold', pad=15)
ax3.grid(axis='x', alpha=0.3)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, genome_counts.values)):
    ax3.text(val + 0.1, i, f'{val}', va='center', fontsize=10, fontweight='bold')

# ============================================================================
# 4. Research Focus Areas (Middle Left)
# ============================================================================
ax4 = fig.add_subplot(gs[1, 0])
focus_counts = df['focus'].value_counts()
focus_labels = {
    'drug_resistance': 'Drug Resistance',
    'biofilm': 'Biofilm Formation',
    'morphology': 'Morphology',
    'host_response': 'Host Response',
    'clinical_variation': 'Clinical Variation',
    'stress_response': 'Stress Response',
    'small_rna': 'Small RNA/EV'
}
focus_counts.index = [focus_labels.get(x, x) for x in focus_counts.index]

bars = ax4.barh(range(len(focus_counts)), focus_counts.values, color=colors[5],
                edgecolor='black', linewidth=1.5)
ax4.set_yticks(range(len(focus_counts)))
ax4.set_yticklabels(focus_counts.index, fontsize=11)
ax4.set_xlabel('Number of Papers', fontsize=12, fontweight='bold')
ax4.set_title('Research Focus Areas', fontsize=14, fontweight='bold', pad=15)
ax4.grid(axis='x', alpha=0.3)

for i, (bar, val) in enumerate(zip(bars, focus_counts.values)):
    ax4.text(val + 0.1, i, f'{val}', va='center', fontsize=10, fontweight='bold')

# ============================================================================
# 5. Most Common Tools (Middle Center and Right - spanning 2 columns)
# ============================================================================
ax5 = fig.add_subplot(gs[1, 1:])
all_tools = []
for tool_list in df['tool_list']:
    all_tools.extend(tool_list)
tool_counts = Counter(all_tools)
top_tools = dict(tool_counts.most_common(15))

y_pos = np.arange(len(top_tools))
bars = ax5.barh(y_pos, list(top_tools.values()), color=colors[6],
                edgecolor='black', linewidth=1.5)
ax5.set_yticks(y_pos)
ax5.set_yticklabels(list(top_tools.keys()), fontsize=10)
ax5.set_xlabel('Frequency', fontsize=12, fontweight='bold')
ax5.set_title('Top 15 Most Common Bioinformatics Tools', fontsize=14, fontweight='bold', pad=15)
ax5.grid(axis='x', alpha=0.3)

for i, (bar, val) in enumerate(zip(bars, top_tools.values())):
    ax5.text(val + 0.1, i, f'{val}', va='center', fontsize=9, fontweight='bold')

# ============================================================================
# 6. Timeline of Publications (Bottom - spanning all columns)
# ============================================================================
ax6 = fig.add_subplot(gs[2, :])

# Create timeline
years = sorted(df['year'].unique())
y_positions = {'PubMed': 2, 'Europe PMC': 1, 'Repository Analysis': 0}
colors_timeline = {'PubMed': colors[1], 'Europe PMC': colors[2],
                   'Repository Analysis': colors[3]}

for _, row in df.iterrows():
    y = y_positions[row['source']]
    x = row['year']

    # Determine color by focus
    if row['focus'] == 'drug_resistance':
        marker = 'D'
        size = 150
    elif row['focus'] == 'biofilm':
        marker = 's'
        size = 150
    else:
        marker = 'o'
        size = 120

    ax6.scatter(x, y, s=size, c=[colors_timeline[row['source']]],
               marker=marker, edgecolors='black', linewidth=1.5, alpha=0.8)

ax6.set_yticks([0, 1, 2])
ax6.set_yticklabels(['Repository\nAnalysis', 'Europe PMC', 'PubMed'], fontsize=11)
ax6.set_xlabel('Year', fontsize=12, fontweight='bold')
ax6.set_title('Publication Timeline by Data Source', fontsize=14, fontweight='bold', pad=15)
ax6.set_xlim(2019.5, 2025.5)
ax6.set_xticks(years)
ax6.grid(True, alpha=0.3)

# Add legend for shapes
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='D', color='w', markerfacecolor='gray',
           markersize=10, label='Drug Resistance', markeredgecolor='black'),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='gray',
           markersize=10, label='Biofilm', markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='gray',
           markersize=10, label='Other', markeredgecolor='black')
]
ax6.legend(handles=legend_elements, loc='upper left', fontsize=10, framealpha=0.9)

# Add overall title
fig.suptitle('Candida auris RNA-seq Literature Survey (2020-2025)\n16 Papers Total',
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig('survey_visualizations.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: survey_visualizations.png")

# ============================================================================
# Create separate detailed figures
# ============================================================================

# Figure 2: Tool Categories
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Categorize tools
tool_categories = {
    'Alignment': ['HISAT2', 'STAR', 'Bowtie2', 'NextGenMap'],
    'Quantification': ['HTSeq', 'featureCounts', 'Stringtie', 'Cufflinks'],
    'Statistical Analysis': ['DESeq2', 'DESeq', 'edgeR', 'Ballgown'],
    'Quality Control': ['FastQC', 'fastp', 'cutadapt', 'Trimmomatic'],
    'Functional Annotation': ['KEGG', 'Gene Ontology', 'topGO', 'KOBAS', 'DAVID',
                               'Fungifun2', 'clusterProfiler', 'BiNGO', 'enrichGO'],
    'Visualization': ['Pheatmap', 'pheatmap', 'Orange3', 'BioVenn', 'VennDiagram', 'IGV'],
    'Other': ['STRING', 'CLC Genomics Workbench', 'StrandNGS', 'Galaxy pipeline',
              'TMM', 'qRT-PCR', 'Agilent BioAnalyzer', 'Illumina NovaSeq']
}

# Count tools by category
category_counts = {cat: 0 for cat in tool_categories.keys()}
for tool_list in df['tool_list']:
    for tool in tool_list:
        for category, tools in tool_categories.items():
            if any(t.lower() in tool.lower() for t in tools):
                category_counts[category] += 1
                break

# Plot 1: Tool categories
bars = ax1.bar(range(len(category_counts)), list(category_counts.values()),
               color=sns.color_palette("Set2", len(category_counts)),
               edgecolor='black', linewidth=1.5)
ax1.set_xticks(range(len(category_counts)))
ax1.set_xticklabels(list(category_counts.keys()), rotation=45, ha='right', fontsize=11)
ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax1.set_title('Bioinformatics Tools by Category', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3)

for bar, val in zip(bars, category_counts.values()):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             f'{val}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Plot 2: Research trends over time
trend_data = df.groupby(['year', 'focus']).size().unstack(fill_value=0)
trend_data.plot(kind='bar', stacked=True, ax=ax2,
                color=sns.color_palette("tab10", len(trend_data.columns)),
                edgecolor='black', linewidth=1)
ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Number of Papers', fontsize=12, fontweight='bold')
ax2.set_title('Research Focus Trends Over Time', fontsize=14, fontweight='bold')
ax2.legend(title='Focus Area', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=0)
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('survey_tools_trends.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: survey_tools_trends.png")

# ============================================================================
# Figure 3: Summary Statistics Table
# ============================================================================
fig3, ax = plt.subplots(figsize=(12, 10))
ax.axis('tight')
ax.axis('off')

# Calculate statistics
stats = {
    'Metric': [
        'Total Papers',
        'Date Range',
        'Most Common Genome',
        'Most Common Tool (Alignment)',
        'Most Common Tool (Statistical)',
        'Dominant Research Focus',
        'Papers on Drug Resistance',
        'Papers on Biofilm',
        'PubMed Papers',
        'Europe PMC Papers',
        'Repository Analysis Papers',
        'Average Papers/Year',
        'Peak Publication Year',
    ],
    'Value': [
        len(df),
        '2020-2025',
        genome_base.value_counts().index[0] if len(genome_base.value_counts()) > 0 else 'N/A',
        'HISAT2',
        'DESeq2',
        'Drug Resistance',
        len(df[df['focus'] == 'drug_resistance']),
        len(df[df['focus'] == 'biofilm']),
        len(df[df['source'] == 'PubMed']),
        len(df[df['source'] == 'Europe PMC']),
        len(df[df['source'] == 'Repository Analysis']),
        f"{len(df) / len(years):.1f}",
        year_counts.idxmax(),
    ]
}

stats_df = pd.DataFrame(stats)

# Create table
table = ax.table(cellText=stats_df.values, colLabels=stats_df.columns,
                cellLoc='left', loc='center',
                colWidths=[0.6, 0.4])

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2.5)

# Style header
for i in range(len(stats_df.columns)):
    table[(0, i)].set_facecolor('#4C72B0')
    table[(0, i)].set_text_props(weight='bold', color='white', fontsize=13)

# Alternate row colors
for i in range(1, len(stats_df) + 1):
    if i % 2 == 0:
        for j in range(len(stats_df.columns)):
            table[(i, j)].set_facecolor('#E8E8E8')

# Add title
ax.text(0.5, 0.95, 'Survey Summary Statistics',
        ha='center', va='top', transform=ax.transAxes,
        fontsize=16, fontweight='bold')

plt.savefig('survey_statistics_table.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Saved: survey_statistics_table.png")

print("\n✓ All visualizations created successfully!")
print(f"\nFiles created:")
print("  - survey_visualizations.png (comprehensive overview)")
print("  - survey_tools_trends.png (tools and trends)")
print("  - survey_statistics_table.png (summary table)")
