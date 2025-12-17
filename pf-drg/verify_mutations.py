#!/usr/bin/env python3
"""Verify drug resistance mutation coordinates against protein sequences."""

import re

# Standard genetic code
CODON_TABLE = {
    'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L',
    'TCT': 'S', 'TCC': 'S', 'TCA': 'S', 'TCG': 'S',
    'TAT': 'Y', 'TAC': 'Y', 'TAA': '*', 'TAG': '*',
    'TGT': 'C', 'TGC': 'C', 'TGA': '*', 'TGG': 'W',
    'CTT': 'L', 'CTC': 'L', 'CTA': 'L', 'CTG': 'L',
    'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAT': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'ATT': 'I', 'ATC': 'I', 'ATA': 'I', 'ATG': 'M',
    'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V',
    'GCT': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGT': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}


def translate(cds):
    """Translate CDS to protein."""
    protein = []
    cds = cds.upper()
    for i in range(0, len(cds) - 2, 3):
        codon = cds[i:i+3]
        aa = CODON_TABLE.get(codon, 'X')
        if aa == '*':
            break
        protein.append(aa)
    return ''.join(protein)


def read_fasta(filepath):
    """Read FASTA file, return dict of gene_name -> sequence."""
    sequences = {}
    current_gene = None
    current_seq = []

    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_gene:
                    sequences[current_gene] = ''.join(current_seq)
                # Extract gene name from header (first field before |)
                current_gene = line[1:].split('|')[0]
                current_seq = []
            else:
                current_seq.append(line)
        if current_gene:
            sequences[current_gene] = ''.join(current_seq)

    return sequences


def parse_mutation(mutation_str):
    """Parse mutation string like K76T -> (wt_aa, position, mut_aa)."""
    # Handle special cases
    if mutation_str in ('Multiple_SNPs', 'Various'):
        return None, None, None

    match = re.match(r'^([A-Z])(\d+)([A-Z])$', mutation_str)
    if match:
        wt_aa = match.group(1)
        position = int(match.group(2))
        mut_aa = match.group(3)
        return wt_aa, position, mut_aa
    return None, None, None


def main():
    # Read CDS sequences
    cds_seqs = read_fasta('pf_drug_resistance_cds.fasta')

    # Translate to protein
    proteins = {gene: translate(seq) for gene, seq in cds_seqs.items()}

    # Print protein lengths for reference
    print("Protein lengths:")
    for gene, prot in proteins.items():
        print(f"  {gene}: {len(prot)} aa")
    print()

    # Read mutations
    results = []
    with open('pf_drug_resistance_mutations.tsv') as f:
        header = f.readline()  # skip header
        for line in f:
            fields = line.strip().split('\t')
            gene = fields[0]
            mutation = fields[2]
            pos_str = fields[3]

            # Handle non-numeric positions
            if not pos_str.isdigit():
                results.append((gene, mutation, pos_str, 'N/A', 'N/A', 'SKIP'))
                continue

            position = int(pos_str)
            wt_aa, pos, mut_aa = parse_mutation(mutation)

            if wt_aa is None:
                results.append((gene, mutation, position, 'N/A', 'N/A', 'SKIP'))
                continue

            # Get protein sequence
            if gene not in proteins:
                results.append((gene, mutation, position, wt_aa, 'NOT_FOUND', 'FAIL'))
                continue

            prot = proteins[gene]

            # Check position (1-indexed)
            if position < 1 or position > len(prot):
                results.append((gene, mutation, position, wt_aa, 'OUT_OF_RANGE', 'FAIL'))
                continue

            actual_aa = prot[position - 1]  # Convert to 0-indexed

            if actual_aa == wt_aa:
                status = 'PASS'
            else:
                status = 'FAIL'

            results.append((gene, mutation, position, wt_aa, actual_aa, status))

    # Write report
    with open('mutation_verification_report.tsv', 'w') as f:
        f.write('Gene\tMutation\tPosition\tExpected_AA\tActual_AA\tStatus\n')
        for row in results:
            f.write('\t'.join(str(x) for x in row) + '\n')

    # Summary
    passed = sum(1 for r in results if r[5] == 'PASS')
    failed = sum(1 for r in results if r[5] == 'FAIL')
    skipped = sum(1 for r in results if r[5] == 'SKIP')

    print(f"Results: {passed} PASS, {failed} FAIL, {skipped} SKIP")

    if failed > 0:
        print("\nFailed mutations:")
        for r in results:
            if r[5] == 'FAIL':
                print(f"  {r[0]} {r[1]}: expected {r[3]}, got {r[4]}")


if __name__ == '__main__':
    main()
