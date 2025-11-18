#!/usr/bin/env python3
"""
Create gene ID mapping between v2 and v3 based on genomic coordinates
"""

import re
from collections import defaultdict

print("="*80)
print("CREATING COORDINATE-BASED GENE MAPPING")
print("="*80)

def parse_gff_coordinates(gff_file):
    """Extract gene coordinates and locus_tags from GFF"""
    genes = []

    with open(gff_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue

            # We want CDS features
            feature_type = parts[2]
            if feature_type != 'CDS':
                continue

            seqid = parts[0]  # chromosome/contig
            start = int(parts[3])
            end = int(parts[4])
            strand = parts[6]
            attributes = parts[8]

            # Extract locus_tag
            locus_tag_match = re.search(r'locus_tag=([^;]+)', attributes)
            if locus_tag_match:
                locus_tag = locus_tag_match.group(1)
                genes.append({
                    'locus_tag': locus_tag,
                    'seqid': seqid,
                    'start': start,
                    'end': end,
                    'strand': strand,
                    'midpoint': (start + end) // 2
                })

    return genes

print("\nParsing v2 annotation...")
v2_genes = parse_gff_coordinates('GCA_002759435.2_genomic.gff')
print(f"  Found {len(v2_genes)} CDS features")

print("\nParsing v3 annotation...")
v3_genes = parse_gff_coordinates('GCA_002759435.3_genomic.gff')
print(f"  Found {len(v3_genes)} CDS features")

# Group by chromosome for faster matching
print("\nGrouping genes by chromosome...")
v2_by_chr = defaultdict(list)
for gene in v2_genes:
    v2_by_chr[gene['seqid']].append(gene)

v3_by_chr = defaultdict(list)
for gene in v3_genes:
    v3_by_chr[gene['seqid']].append(gene)

print(f"  v2 chromosomes: {list(v2_by_chr.keys())[:5]}...")
print(f"  v3 chromosomes: {list(v3_by_chr.keys())[:5]}...")

# Match genes based on overlapping coordinates
print("\nMatching genes by coordinates...")
mapping_v2_to_v3 = {}
mapping_v3_to_v2 = {}
matched = 0
unmatched_v2 = 0

for v2_gene in v2_genes:
    chr = v2_gene['seqid']
    v2_start = v2_gene['start']
    v2_end = v2_gene['end']
    v2_strand = v2_gene['strand']

    # Find overlapping v3 genes on same chromosome and strand
    best_match = None
    best_overlap = 0

    if chr in v3_by_chr:
        for v3_gene in v3_by_chr[chr]:
            # Must be on same strand
            if v3_gene['strand'] != v2_strand:
                continue

            # Calculate overlap
            overlap_start = max(v2_start, v3_gene['start'])
            overlap_end = min(v2_end, v3_gene['end'])
            overlap = max(0, overlap_end - overlap_start + 1)

            if overlap > best_overlap:
                best_overlap = overlap
                best_match = v3_gene

    # Consider it a match if there's significant overlap (>50% of shorter gene)
    if best_match:
        v2_len = v2_end - v2_start + 1
        v3_len = best_match['end'] - best_match['start'] + 1
        min_len = min(v2_len, v3_len)

        if best_overlap / min_len > 0.5:  # At least 50% overlap
            mapping_v2_to_v3[v2_gene['locus_tag']] = best_match['locus_tag']
            mapping_v3_to_v2[best_match['locus_tag']] = v2_gene['locus_tag']
            matched += 1
        else:
            unmatched_v2 += 1
    else:
        unmatched_v2 += 1

print(f"  Matched: {matched} genes")
print(f"  Unmatched v2: {unmatched_v2} genes")

# Show some examples
print("\n" + "-"*80)
print("Sample mappings:")
print("-"*80)
for i, (v2_id, v3_id) in enumerate(list(mapping_v2_to_v3.items())[:10]):
    print(f"  {v2_id} → {v3_id}")

# Save mapping to file
print("\nSaving mapping to file...")
with open('coordinate_based_mapping_v2_to_v3.tsv', 'w') as f:
    f.write("Gene_ID_v2\tGene_ID_v3\n")
    for v2_id, v3_id in sorted(mapping_v2_to_v3.items()):
        f.write(f"{v2_id}\t{v3_id}\n")

print(f"✓ Saved to: coordinate_based_mapping_v2_to_v3.tsv")

# Test with our known genes
print("\n" + "="*80)
print("TESTING WITH KNOWN GENES")
print("="*80)

test_genes = ['B9J08_001458', 'B9J08_004451', 'B9J08_000592', 'B9J08_005317']
print("\nChecking if my old mapping was correct:")
for gene_v2 in test_genes:
    # My old (wrong) mapping
    old_v3 = gene_v2.replace('B9J08_', 'B9J08_').split('_')[1].lstrip('0')
    old_v3 = f"B9J08_{old_v3.zfill(5)}"

    # Coordinate-based mapping
    new_v3 = mapping_v2_to_v3.get(gene_v2, 'NOT FOUND')

    print(f"  {gene_v2}")
    print(f"    Old mapping: {old_v3}")
    print(f"    Coordinate-based: {new_v3}")
    print(f"    Match: {'✓' if old_v3 == new_v3 else '✗'}")
