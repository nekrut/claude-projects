#!/usr/bin/env python3
"""
Extract protein sequences for DEGs and create 4 FASTA files
"""

import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

print("="*80)
print("EXTRACTING PROTEIN SEQUENCES FOR DEGs")
print("="*80)

# Load protein sequences
print("\nLoading protein sequences...")
v2_proteins = {rec.id.split()[0]: rec for rec in SeqIO.parse("GCA_002759435.2_protein.faa", "fasta")}
v3_proteins = {rec.id.split()[0]: rec for rec in SeqIO.parse("GCA_002759435.3_protein.faa", "fasta")}

print(f"  v2 proteins loaded: {len(v2_proteins)}")
print(f"  v3 proteins loaded: {len(v3_proteins)}")

# Check ID formats in the files
print("\nSample v2 IDs:")
for i, key in enumerate(list(v2_proteins.keys())[:5]):
    print(f"  {key}")

print("\nSample v3 IDs:")
for i, key in enumerate(list(v3_proteins.keys())[:5]):
    print(f"  {key}")

# Load DEG lists
paper_vitro = pd.read_csv('paper_vitro_degs.tsv', sep='\t')
paper_vivo = pd.read_csv('paper_vivo_degs.tsv', sep='\t')
our_vitro = pd.read_csv('our_vitro_degs.tsv', sep='\t')
our_vivo = pd.read_csv('our_vivo_degs.tsv', sep='\t')

def extract_protein_id_v2(gene_id):
    """Extract protein ID for v2 annotation"""
    # v2 format might be like: lcl|NW_017263849.1_prot_PFK23863.1_1
    # We need to find which format matches our gene IDs
    # Try exact match first
    if gene_id in v2_proteins:
        return gene_id
    # Try with different prefixes
    for prot_id in v2_proteins.keys():
        if gene_id in prot_id:
            return prot_id
    return None

def extract_protein_id_v3(gene_id):
    """Extract protein ID for v3 annotation"""
    # Similar approach for v3
    if gene_id in v3_proteins:
        return gene_id
    for prot_id in v3_proteins.keys():
        if gene_id in prot_id:
            return prot_id
    return None

def create_fasta_files(deg_df, protein_dict, gene_id_col, output_file, version):
    """Create FASTA file for DEGs"""
    sequences = []
    found = 0
    not_found = []

    for idx, row in deg_df.iterrows():
        gene_id = row[gene_id_col]

        # Try to find the protein
        prot_id = None
        if version == 'v2':
            prot_id = extract_protein_id_v2(gene_id)
        else:
            prot_id = extract_protein_id_v3(gene_id)

        if prot_id and prot_id in protein_dict:
            rec = protein_dict[prot_id]
            # Create new record with gene ID in header
            new_rec = SeqRecord(
                rec.seq,
                id=gene_id,
                description=f"{rec.description} | orig_id={prot_id}"
            )
            sequences.append(new_rec)
            found += 1
        else:
            not_found.append(gene_id)

    # Write FASTA file
    SeqIO.write(sequences, output_file, "fasta")

    return found, not_found

print("\n" + "="*80)
print("CREATING FASTA FILES")
print("="*80)

# 1. Paper's in vitro DEGs with v2 gene IDs
print("\n1. Paper in vitro DEGs (v2 IDs)...")
found, not_found = create_fasta_files(
    paper_vitro, v2_proteins, 'Gene_ID_v2',
    'paper_vitro_degs_v2.fasta', 'v2'
)
print(f"   Found: {found}/{len(paper_vitro)}")
if not_found:
    print(f"   Not found: {len(not_found)} genes")

# 2. Paper's in vitro DEGs with v3 gene IDs
print("\n2. Paper in vitro DEGs (v3 IDs)...")
found, not_found = create_fasta_files(
    paper_vitro, v3_proteins, 'Gene_ID_v3',
    'paper_vitro_degs_v3.fasta', 'v3'
)
print(f"   Found: {found}/{len(paper_vitro)}")
if not_found:
    print(f"   Not found: {len(not_found)} genes")

# 3. Our in vitro DEGs with v2 gene IDs
print("\n3. Our in vitro DEGs (v2 IDs)...")
found, not_found = create_fasta_files(
    our_vitro, v2_proteins, 'Gene_ID_v2',
    'our_vitro_degs_v2.fasta', 'v2'
)
print(f"   Found: {found}/{len(our_vitro)}")
if not_found:
    print(f"   Not found: {len(not_found)} genes")

# 4. Our in vitro DEGs with v3 gene IDs
print("\n4. Our in vitro DEGs (v3 IDs)...")
found, not_found = create_fasta_files(
    our_vitro, v3_proteins, 'Gene_ID_v3',
    'our_vitro_degs_v3.fasta', 'v3'
)
print(f"   Found: {found}/{len(our_vitro)}")
if not_found:
    print(f"   Not found: {len(not_found)} genes")

# 5-8. Same for in vivo
print("\n5. Paper in vivo DEGs (v2 IDs)...")
found, not_found = create_fasta_files(
    paper_vivo, v2_proteins, 'Gene_ID_v2',
    'paper_vivo_degs_v2.fasta', 'v2'
)
print(f"   Found: {found}/{len(paper_vivo)}")

print("\n6. Paper in vivo DEGs (v3 IDs)...")
found, not_found = create_fasta_files(
    paper_vivo, v3_proteins, 'Gene_ID_v3',
    'paper_vivo_degs_v3.fasta', 'v3'
)
print(f"   Found: {found}/{len(paper_vivo)}")

print("\n7. Our in vivo DEGs (v2 IDs)...")
found, not_found = create_fasta_files(
    our_vivo, v2_proteins, 'Gene_ID_v2',
    'our_vivo_degs_v2.fasta', 'v2'
)
print(f"   Found: {found}/{len(our_vivo)}")

print("\n8. Our in vivo DEGs (v3 IDs)...")
found, not_found = create_fasta_files(
    our_vivo, v3_proteins, 'Gene_ID_v3',
    'our_vivo_degs_v3.fasta', 'v3'
)
print(f"   Found: {found}/{len(our_vivo)}")

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
