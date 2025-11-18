#!/usr/bin/env python3
"""
Extract protein sequences for DEGs using GFF mapping
"""

import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import re

print("="*80)
print("EXTRACTING PROTEIN SEQUENCES FOR DEGs (with GFF mapping)")
print("="*80)

# Parse GFF to get locus_tag -> protein_id mapping
def parse_gff_mapping(gff_file):
    """Extract locus_tag to protein_id mapping from GFF"""
    mapping = {}
    print(f"\nParsing {gff_file}...")

    with open(gff_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue

            feature_type = parts[2]
            if feature_type != 'CDS':
                continue

            attributes = parts[8]

            # Extract locus_tag and protein_id
            locus_tag_match = re.search(r'locus_tag=([^;]+)', attributes)
            protein_id_match = re.search(r'protein_id=([^;]+)', attributes)

            if locus_tag_match and protein_id_match:
                locus_tag = locus_tag_match.group(1)
                protein_id = protein_id_match.group(1)
                mapping[locus_tag] = protein_id

    print(f"  Found {len(mapping)} locus_tag -> protein_id mappings")
    if len(mapping) > 0:
        sample = list(mapping.items())[:3]
        print(f"  Sample mappings:")
        for lt, pi in sample:
            print(f"    {lt} -> {pi}")

    return mapping

# Load mappings
v2_mapping = parse_gff_mapping("GCA_002759435.2_genomic.gff")
v3_mapping = parse_gff_mapping("GCA_002759435.3_genomic.gff")

# Load protein sequences
print("\nLoading protein sequences...")
v2_proteins = {rec.id: rec for rec in SeqIO.parse("GCA_002759435.2_protein.faa", "fasta")}
v3_proteins = {rec.id: rec for rec in SeqIO.parse("GCA_002759435.3_protein.faa", "fasta")}
print(f"  v2 proteins: {len(v2_proteins)}")
print(f"  v3 proteins: {len(v3_proteins)}")

# Load CORRECTED DEG lists (with official NCBI mapping)
paper_vitro = pd.read_csv('paper_vitro_degs_corrected.tsv', sep='\t')
paper_vivo = pd.read_csv('paper_vivo_degs_corrected.tsv', sep='\t')
our_vitro = pd.read_csv('our_vitro_degs_corrected.tsv', sep='\t')
our_vivo = pd.read_csv('our_vivo_degs_corrected.tsv', sep='\t')

def create_fasta_with_mapping(deg_df, gene_id_col, mapping, protein_dict, output_file, desc):
    """Create FASTA file using GFF mapping"""
    sequences = []
    found = 0
    not_found = []

    for idx, row in deg_df.iterrows():
        gene_id = row[gene_id_col]

        # Get protein ID from mapping
        if gene_id in mapping:
            protein_id = mapping[gene_id]

            # Get protein sequence
            if protein_id in protein_dict:
                rec = protein_dict[protein_id]
                # Create new record with gene ID
                new_rec = SeqRecord(
                    rec.seq,
                    id=gene_id,
                    description=f"protein_id={protein_id} | {rec.description}"
                )
                sequences.append(new_rec)
                found += 1
            else:
                not_found.append(f"{gene_id} (protein_id={protein_id} not in FASTA)")
        else:
            not_found.append(f"{gene_id} (no mapping)")

    # Write FASTA
    SeqIO.write(sequences, output_file, "fasta")

    print(f"\n{desc}")
    print(f"  Found: {found}/{len(deg_df)}")
    if not_found and len(not_found) <= 10:
        print(f"  Not found:")
        for nf in not_found:
            print(f"    - {nf}")
    elif not_found:
        print(f"  Not found: {len(not_found)} genes")

    return found, len(not_found)

print("\n" + "="*80)
print("CREATING FASTA FILES")
print("="*80)

# Create all 8 FASTA files
results = []

# IN VITRO
results.append(create_fasta_with_mapping(
    paper_vitro, 'Gene_ID_v2', v2_mapping, v2_proteins,
    'paper_vitro_degs_v2.fasta', '1. Paper in vitro DEGs (v2)'
))

results.append(create_fasta_with_mapping(
    paper_vitro, 'Gene_ID_v3', v3_mapping, v3_proteins,
    'paper_vitro_degs_v3.fasta', '2. Paper in vitro DEGs (v3)'
))

results.append(create_fasta_with_mapping(
    our_vitro, 'Gene_ID_v2', v2_mapping, v2_proteins,
    'our_vitro_degs_v2.fasta', '3. Our in vitro DEGs (v2)'
))

results.append(create_fasta_with_mapping(
    our_vitro, 'Gene_ID_v3', v3_mapping, v3_proteins,
    'our_vitro_degs_v3.fasta', '4. Our in vitro DEGs (v3)'
))

# IN VIVO
results.append(create_fasta_with_mapping(
    paper_vivo, 'Gene_ID_v2', v2_mapping, v2_proteins,
    'paper_vivo_degs_v2.fasta', '5. Paper in vivo DEGs (v2)'
))

results.append(create_fasta_with_mapping(
    paper_vivo, 'Gene_ID_v3', v3_mapping, v3_proteins,
    'paper_vivo_degs_v3.fasta', '6. Paper in vivo DEGs (v3)'
))

results.append(create_fasta_with_mapping(
    our_vivo, 'Gene_ID_v2', v2_mapping, v2_proteins,
    'our_vivo_degs_v2.fasta', '7. Our in vivo DEGs (v2)'
))

results.append(create_fasta_with_mapping(
    our_vivo, 'Gene_ID_v3', v3_mapping, v3_proteins,
    'our_vivo_degs_v3.fasta', '8. Our in vivo DEGs (v3)'
))

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print("\n✓ All FASTA files created!")
print("\nFiles created:")
print("  IN VITRO:")
print("    - paper_vitro_degs_v2.fasta")
print("    - paper_vitro_degs_v3.fasta")
print("    - our_vitro_degs_v2.fasta")
print("    - our_vitro_degs_v3.fasta")
print("  IN VIVO:")
print("    - paper_vivo_degs_v2.fasta")
print("    - paper_vivo_degs_v3.fasta")
print("    - our_vivo_degs_v2.fasta")
print("    - our_vivo_degs_v3.fasta")
