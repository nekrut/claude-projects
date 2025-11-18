#!/usr/bin/env python3
"""
Investigate the gene ID mapping between v2 and v3
to understand why protein sequences don't match
"""

import pandas as pd
from Bio import SeqIO

print("="*80)
print("INVESTIGATING GENE ID MAPPING ISSUES")
print("="*80)

# Load DEG lists
print("\nLoading DEG lists...")
paper_vitro = pd.read_csv('paper_vitro_degs.tsv', sep='\t')
our_vitro = pd.read_csv('our_vitro_degs.tsv', sep='\t')

print(f"  Paper in_vitro: {len(paper_vitro)} DEGs")
print(f"  Our in_vitro: {len(our_vitro)} DEGs")

# Show sample gene IDs
print("\n" + "-"*80)
print("Sample gene IDs from PAPER's in_vitro DEGs:")
print("-"*80)
for i in range(min(5, len(paper_vitro))):
    row = paper_vitro.iloc[i]
    print(f"  v2: {row['Gene_ID_v2']:15s} → v3: {row['Gene_ID_v3']}")

print("\n" + "-"*80)
print("Sample gene IDs from OUR in_vitro DEGs:")
print("-"*80)
for i in range(min(5, len(our_vitro))):
    row = our_vitro.iloc[i]
    print(f"  v2: {row['Gene_ID_v2']:15s} → v3: {row['Gene_ID_v3']}")

# Load the actual protein sequences to see what we extracted
print("\n" + "="*80)
print("CHECKING EXTRACTED PROTEIN SEQUENCES")
print("="*80)

print("\nPaper in_vitro v2 FASTA (first 3 entries):")
for i, rec in enumerate(SeqIO.parse('paper_vitro_degs_v2.fasta', 'fasta')):
    if i >= 3:
        break
    print(f"  >{rec.id}")
    print(f"    Description: {rec.description}")
    print(f"    Seq length: {len(rec.seq)} aa")

print("\nPaper in_vitro v3 FASTA (first 3 entries):")
for i, rec in enumerate(SeqIO.parse('paper_vitro_degs_v3.fasta', 'fasta')):
    if i >= 3:
        break
    print(f"  >{rec.id}")
    print(f"    Description: {rec.description}")
    print(f"    Seq length: {len(rec.seq)} aa")

# Check if the mapping used for protein extraction is correct
print("\n" + "="*80)
print("CHECKING LOCUS_TAG CONSISTENCY")
print("="*80)
print("\nThe question: Does the same locus_tag in v2 and v3 refer to the same gene?")
print("Let me check if B9J08_005317 (v2) should map to B9J08_05317 (v3) or B9J08_04200 (v3)...")

# Load GFF mappings to see what we actually did
import re

def parse_gff_sample(gff_file, target_locus_tags):
    """Parse GFF to show what protein_id each locus_tag maps to"""
    results = {}
    with open(gff_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue
            if parts[2] != 'CDS':
                continue

            attributes = parts[8]
            locus_tag_match = re.search(r'locus_tag=([^;]+)', attributes)
            protein_id_match = re.search(r'protein_id=([^;]+)', attributes)

            if locus_tag_match and protein_id_match:
                locus_tag = locus_tag_match.group(1)
                protein_id = protein_id_match.group(1)
                if locus_tag in target_locus_tags:
                    results[locus_tag] = protein_id

    return results

# Check some specific genes
test_genes_v2 = ['B9J08_005317', 'B9J08_003657', 'B9J08_002550']
test_genes_v3 = ['B9J08_05317', 'B9J08_03657', 'B9J08_02550', 'B9J08_04200', 'B9J08_01515']

print("\n Checking v2 annotation:")
v2_mapping = parse_gff_sample('GCA_002759435.2_genomic.gff', test_genes_v2)
for lt, pid in v2_mapping.items():
    print(f"  {lt} → {pid}")

print("\n Checking v3 annotation:")
v3_mapping = parse_gff_sample('GCA_002759435.3_genomic.gff', test_genes_v3)
for lt, pid in v3_mapping.items():
    print(f"  {lt} → {pid}")

print("\n" + "="*80)
print("HYPOTHESIS TEST")
print("="*80)
print("\nTwo possible scenarios:")
print("1. Gene IDs were simply reformatted: B9J08_005317 (v2) = B9J08_05317 (v3)")
print("   -> Same gene, just removed leading zeros")
print("2. Genes were renumbered: B9J08_005317 (v2) ≠ B9J08_05317 (v3)")
print("   -> Different genes entirely")
print("\nBased on the 2-5% sequence overlap, scenario 2 seems likely.")
print("This means the mapping I created by normalizing IDs (removing zeros)")
print("is INCORRECT - it's mapping different genes together!")
