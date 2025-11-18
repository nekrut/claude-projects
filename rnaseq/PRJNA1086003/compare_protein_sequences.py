#!/usr/bin/env python3
"""
Compare protein sequences between v2 and v3 annotations to test if
the same proteins have different gene IDs
"""

from Bio import SeqIO
from collections import defaultdict
import pandas as pd

print("="*80)
print("COMPARING PROTEIN SEQUENCES BETWEEN ANNOTATION VERSIONS")
print("="*80)

def load_sequences(fasta_file):
    """Load sequences into dict by gene_id and by sequence"""
    by_id = {}
    by_seq = defaultdict(list)

    for rec in SeqIO.parse(fasta_file, "fasta"):
        gene_id = rec.id
        seq_str = str(rec.seq)
        by_id[gene_id] = seq_str
        by_seq[seq_str].append(gene_id)

    return by_id, by_seq

def compare_versions(v2_file, v3_file, description):
    """Compare sequences between v2 and v3 annotations"""
    print(f"\n{description}")
    print("-" * 80)

    v2_by_id, v2_by_seq = load_sequences(v2_file)
    v3_by_id, v3_by_seq = load_sequences(v3_file)

    print(f"  v2 sequences: {len(v2_by_id)}")
    print(f"  v3 sequences: {len(v3_by_id)}")

    # Find sequence overlaps
    v2_seqs = set(v2_by_seq.keys())
    v3_seqs = set(v3_by_seq.keys())

    common_seqs = v2_seqs & v3_seqs
    v2_only = v2_seqs - v3_seqs
    v3_only = v3_seqs - v2_seqs

    print(f"\n  Sequence overlap:")
    print(f"    Common sequences: {len(common_seqs)} ({len(common_seqs)/len(v2_seqs)*100:.1f}% of v2)")
    print(f"    v2-only sequences: {len(v2_only)}")
    print(f"    v3-only sequences: {len(v3_only)}")

    # Check if gene IDs changed for common sequences
    gene_id_changes = []
    for seq in list(common_seqs)[:10]:  # Sample first 10
        v2_ids = v2_by_seq[seq]
        v3_ids = v3_by_seq[seq]
        if v2_ids != v3_ids:
            gene_id_changes.append((v2_ids[0], v3_ids[0]))

    if gene_id_changes:
        print(f"\n  Sample gene ID changes for identical sequences:")
        for v2_id, v3_id in gene_id_changes[:5]:
            print(f"    {v2_id} (v2) → {v3_id} (v3)")

    return {
        'common_seqs': len(common_seqs),
        'v2_only': len(v2_only),
        'v3_only': len(v3_only),
        'v2_total': len(v2_by_id),
        'v3_total': len(v3_by_id),
        'overlap_pct': len(common_seqs)/len(v2_seqs)*100 if v2_seqs else 0
    }

# Compare all 4 combinations
results = []

print("\n" + "="*80)
print("PAPER'S DEGs")
print("="*80)

res = compare_versions(
    'paper_vitro_degs_v2.fasta',
    'paper_vitro_degs_v3.fasta',
    '1. PAPER IN VITRO: Comparing v2 vs v3'
)
results.append(('Paper in_vitro', res))

res = compare_versions(
    'paper_vivo_degs_v2.fasta',
    'paper_vivo_degs_v3.fasta',
    '2. PAPER IN VIVO: Comparing v2 vs v3'
)
results.append(('Paper in_vivo', res))

print("\n" + "="*80)
print("OUR DEGs")
print("="*80)

res = compare_versions(
    'our_vitro_degs_v2.fasta',
    'our_vitro_degs_v3.fasta',
    '3. OUR IN VITRO: Comparing v2 vs v3'
)
results.append(('Our in_vitro', res))

res = compare_versions(
    'our_vivo_degs_v2.fasta',
    'our_vivo_degs_v3.fasta',
    '4. OUR IN VIVO: Comparing v2 vs v3'
)
results.append(('Our in_vivo', res))

print("\n" + "="*80)
print("SUMMARY")
print("="*80)

for name, res in results:
    print(f"\n{name}:")
    print(f"  Sequence overlap: {res['overlap_pct']:.1f}%")
    print(f"  Common: {res['common_seqs']}, v2-only: {res['v2_only']}, v3-only: {res['v3_only']}")
