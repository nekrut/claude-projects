#!/usr/bin/env python3
"""Fetch P. falciparum drug resistance gene CDS sequences using NCBI datasets CLI."""

import subprocess
import tempfile
import zipfile
import os
import re

# Gene name, PlasmoDB ID, NCBI Gene ID
GENES = [
    ("Pfk13", "PF3D7_1343700", 814205),
    ("pfmdr1", "PF3D7_0523000", 813045),
    ("Pfcrt", "PF3D7_0709000", 2655199),
    ("Pfdhfr", "PF3D7_0417200", 9221804),
    ("Pfdhps", "PF3D7_0810800", 2655294),
    ("Pfubp1", "PF3D7_0104300", 813181),
    ("PfATP6", "PF3D7_0106300", 813199),
    ("MRP1", "PF3D7_0112200", 813255),
    ("MRP2", "PF3D7_1229100", 811334),
]


def fetch_cds_with_datasets(gene_name, plasmodb_id, gene_id):
    """Fetch CDS sequence using NCBI datasets CLI."""
    print(f"Fetching {gene_name} ({plasmodb_id}, GeneID:{gene_id})...")

    with tempfile.TemporaryDirectory() as tmpdir:
        zippath = os.path.join(tmpdir, "gene.zip")

        # Download gene data with CDS
        cmd = [
            "datasets", "download", "gene", "gene-id", str(gene_id),
            "--include", "cds",
            "--filename", zippath
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  WARNING: datasets download failed for {plasmodb_id}")
            print(f"  stderr: {result.stderr}")
            return None

        # Extract CDS from zip
        try:
            with zipfile.ZipFile(zippath, 'r') as zf:
                cds_path = "ncbi_dataset/data/cds.fna"
                if cds_path not in zf.namelist():
                    print(f"  WARNING: No CDS file in download for {plasmodb_id}")
                    return None

                cds_content = zf.read(cds_path).decode('utf-8')
        except Exception as e:
            print(f"  WARNING: Failed to extract CDS for {plasmodb_id}: {e}")
            return None

    # Parse and reformat FASTA
    sequences = []
    current_header = None
    current_seq = []

    for line in cds_content.strip().split('\n'):
        if line.startswith('>'):
            if current_header and current_seq:
                sequences.append((current_header, ''.join(current_seq)))
            current_header = line
            current_seq = []
        else:
            current_seq.append(line)

    if current_header and current_seq:
        sequences.append((current_header, ''.join(current_seq)))

    if not sequences:
        print(f"  WARNING: No sequences found for {plasmodb_id}")
        return None

    # Use first sequence, reformat header
    header, seq = sequences[0]

    # Extract accession from original header
    match = re.search(r'>(\S+)', header)
    accession = match.group(1) if match else "unknown"

    new_header = f">{gene_name}|{plasmodb_id}|{accession}"

    # Wrap sequence to 70 chars per line
    wrapped_seq = '\n'.join(seq[i:i+70] for i in range(0, len(seq), 70))

    return f"{new_header}\n{wrapped_seq}"


def main():
    output_file = "pf_drug_resistance_cds.fasta"
    sequences = []

    for gene_name, plasmodb_id, gene_id in GENES:
        seq = fetch_cds_with_datasets(gene_name, plasmodb_id, gene_id)
        if seq:
            sequences.append(seq)
            print(f"  Success: {gene_name}")
        else:
            print(f"  FAILED: {gene_name}")

    with open(output_file, "w") as f:
        f.write("\n\n".join(sequences) + "\n")

    print(f"\nWrote {len(sequences)}/{len(GENES)} sequences to {output_file}")


if __name__ == "__main__":
    main()
