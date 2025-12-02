#!/usr/bin/env python3
"""
Analyze combined Candida auris RNA-seq literature from three sources:
1. Claude survey (PubMed + Europe PMC + Repository)
2. ChatGPT survey (PubMed + Europe PMC)
3. GEO database survey

Generate statistics and prepare data for comprehensive report.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter
import re

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Combined dataset from all three surveys
combined_data = [
    # Claude survey (16 papers)
    {'pmid': '32581078', 'year': 2020, 'source': 'Claude (PubMed)', 'genome': 'N/A', 'focus': 'Biofilm', 'in_geo': False},
    {'pmid': '33937102', 'year': 2021, 'source': 'Claude (PubMed)', 'genome': 'B11221', 'focus': 'Drug resistance', 'in_geo': True},
    {'pmid': '34354695', 'year': 2021, 'source': 'Claude (PubMed)', 'genome': 'N/A', 'focus': 'Drug resistance', 'in_geo': False},
    {'pmid': '34485470', 'year': 2021, 'source': 'Claude (PubMed)', 'genome': 'GCA_002759435', 'focus': 'Stress response', 'in_geo': False},
    {'pmid': '34630944', 'year': 2021, 'source': 'Claude (Europe PMC)', 'genome': 'B8441', 'focus': 'Drug resistance', 'in_geo': False},
    {'pmid': '34788438', 'year': 2021, 'source': 'Claude (PubMed)', 'genome': 'B8441', 'focus': 'Small RNA', 'in_geo': False},
    {'pmid': '35652307', 'year': 2022, 'source': 'Claude (PubMed)', 'genome': 'B8441', 'focus': 'Drug resistance', 'in_geo': True},
    {'pmid': '35968956', 'year': 2022, 'source': 'Claude (Europe PMC)', 'genome': 'B8441', 'focus': 'Drug resistance', 'in_geo': False},
    {'pmid': '36913408', 'year': 2023, 'source': 'Claude (Europe PMC)', 'genome': 'GCA_002759435.2', 'focus': 'Biofilm', 'in_geo': False},
    {'pmid': '37350781', 'year': 2023, 'source': 'Claude (PubMed)', 'genome': 'B11221', 'focus': 'Morphotype', 'in_geo': False},
    {'pmid': '37769084', 'year': 2023, 'source': 'Claude (Repository)', 'genome': 'GCA_002759435.3', 'focus': 'Adhesin', 'in_geo': False},
    {'pmid': '38562758', 'year': 2024, 'source': 'Claude (Repository)', 'genome': 'GCA_002759435', 'focus': 'Adhesin', 'in_geo': False},
    {'pmid': '38990436', 'year': 2024, 'source': 'Claude (PubMed)', 'genome': 'N/A', 'focus': 'Host-pathogen', 'in_geo': False},
    {'pmid': 'PMC11385638', 'year': 2024, 'source': 'Claude (PubMed)', 'genome': 'B11221', 'focus': 'Drug resistance', 'in_geo': False},
    {'pmid': 'PMC11459930', 'year': 2024, 'source': 'Claude (Europe PMC)', 'genome': 'B8441', 'focus': 'Drug resistance', 'in_geo': False},
    {'pmid': '40099908', 'year': 2025, 'source': 'Claude (Europe PMC)', 'genome': 'B8441', 'focus': 'Drug resistance', 'in_geo': False},

    # ChatGPT survey (9 papers, all unique from Claude)
    {'pmid': '33983315', 'year': 2021, 'source': 'ChatGPT', 'genome': 'B8441', 'focus': 'Stress response', 'in_geo': False},
    {'pmid': '33995473', 'year': 2021, 'source': 'ChatGPT', 'genome': 'B8441', 'focus': 'Phenotype', 'in_geo': False},
    {'pmid': '34462177', 'year': 2021, 'source': 'ChatGPT', 'genome': 'B8441', 'focus': 'Stress response', 'in_geo': False},
    {'pmid': '34778924', 'year': 2021, 'source': 'ChatGPT', 'genome': 'B8441', 'focus': 'Drug resistance', 'in_geo': False},
    {'pmid': '35649081', 'year': 2022, 'source': 'ChatGPT', 'genome': 'B8441', 'focus': 'Adhesin', 'in_geo': False},
    {'pmid': '37548469', 'year': 2023, 'source': 'ChatGPT', 'genome': 'Isolate 12', 'focus': 'Stress response', 'in_geo': True},
    {'pmid': '37925028', 'year': 2025, 'source': 'ChatGPT', 'genome': 'B8441', 'focus': 'Morphotype', 'in_geo': False},
    {'pmid': '38537618', 'year': 2024, 'source': 'ChatGPT', 'genome': 'B8441', 'focus': 'Biofilm', 'in_geo': True},
    {'pmid': '38745637', 'year': 2024, 'source': 'ChatGPT', 'genome': 'B8441', 'focus': 'Host-pathogen', 'in_geo': False},

    # GEO survey (11 papers, 2 overlap with Claude, 2 overlap with ChatGPT = 7 unique)
    # Overlaps already counted above with in_geo=True
    {'pmid': '33077664', 'year': 2020, 'source': 'GEO', 'genome': 'B8441', 'focus': 'Drug resistance', 'in_geo': True},
    {'pmid': '35142597', 'year': 2022, 'source': 'GEO', 'genome': 'B8441', 'focus': 'Host-pathogen', 'in_geo': True},
    {'pmid': '32839538', 'year': 2020, 'source': 'GEO', 'genome': 'Human', 'focus': 'Host-pathogen', 'in_geo': True},
    {'pmid': '34083769', 'year': 2021, 'source': 'GEO', 'genome': 'B8441', 'focus': 'Stress response', 'in_geo': True},
    {'pmid': '34643421', 'year': 2021, 'source': 'GEO', 'genome': 'B8441', 'focus': 'Stress response', 'in_geo': True},
    {'pmid': '29997121', 'year': 2018, 'source': 'GEO', 'genome': 'B8441', 'focus': 'Biofilm', 'in_geo': True},
    {'pmid': '30559369', 'year': 2018, 'source': 'GEO', 'genome': 'B8441', 'focus': 'Drug resistance', 'in_geo': True},
]

df = pd.DataFrame(combined_data)

# Calculate statistics
total_papers = len(df)
unique_papers = len(df['pmid'].unique())
date_range = f"{df['year'].min()}-{df['year'].max()}"

# Count by source
claude_total = len(df[df['source'].str.contains('Claude')])
chatgpt_total = len(df[df['source'] == 'ChatGPT'])
geo_total = len(df[df['in_geo'] == True])

# Overlap calculations
claude_chatgpt_overlap = 0  # Zero as documented
claude_geo_overlap = len(df[(df['source'].str.contains('Claude')) & (df['in_geo'] == True)])
chatgpt_geo_overlap = len(df[(df['source'] == 'ChatGPT') & (df['in_geo'] == True)])

print("=" * 70)
print("COMBINED CANDIDA AURIS RNA-SEQ LITERATURE SURVEY STATISTICS")
print("=" * 70)
print(f"\nTotal papers in dataset: {total_papers}")
print(f"Unique papers (accounting for overlaps): {unique_papers}")
print(f"Date range: {date_range}")
print(f"\nPapers by source:")
print(f"  Claude survey: {claude_total}")
print(f"  ChatGPT survey: {chatgpt_total}")
print(f"  GEO survey: {geo_total}")
print(f"\nOverlap statistics:")
print(f"  Claude-ChatGPT overlap: {claude_chatgpt_overlap} papers (0%)")
print(f"  Claude-GEO overlap: {claude_geo_overlap} papers")
print(f"  ChatGPT-GEO overlap: {chatgpt_geo_overlap} papers")

# Genome statistics
genome_counts = df['genome'].value_counts()
print(f"\n{'Genome Reference':<30} {'Count':<10} {'Percentage'}")
print("-" * 50)
for genome, count in genome_counts.items():
    pct = (count / total_papers) * 100
    print(f"{genome:<30} {count:<10} {pct:.1f}%")

# Research focus
focus_counts = df['focus'].value_counts()
print(f"\n{'Research Focus':<30} {'Count':<10} {'Percentage'}")
print("-" * 50)
for focus, count in focus_counts.items():
    pct = (count / total_papers) * 100
    print(f"{focus:<30} {count:<10} {pct:.1f}%")

# Year distribution
year_counts = df['year'].value_counts().sort_index()
print(f"\n{'Year':<10} {'Papers'}")
print("-" * 20)
for year, count in year_counts.items():
    print(f"{year:<10} {count}")

print("\n" + "=" * 70)

# Save processed data
df.to_csv('/home/anton/git/claude-projects/rnaseq/Cauris_rna_seq_survey/combined/combined_data.csv', index=False)
print("\nData saved to: combined_data.csv")
