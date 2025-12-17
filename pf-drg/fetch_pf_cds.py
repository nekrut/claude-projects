#!/usr/bin/env python3
"""Fetch P. falciparum drug resistance gene CDS sequences from NCBI."""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import time
import re

GENES = [
    ("Pfk13", "PF3D7_1343700"),
    ("pfmdr1", "PF3D7_0523000"),
    ("Pfcrt", "PF3D7_0709000"),
    ("Pfdhfr", "PF3D7_0417200"),
    ("Pfdhps", "PF3D7_0810800"),
    ("Pfubp1", "PF3D7_0104300"),
    ("PfATP6", "PF3D7_0106300"),
    ("MRP1", "PF3D7_0112200"),
    ("MRP2", "PF3D7_1229100"),
]

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
EMAIL = "user@example.com"


def esearch(db, term):
    """Search NCBI database and return list of IDs."""
    params = urllib.parse.urlencode({
        "db": db,
        "term": term,
        "retmode": "xml",
        "email": EMAIL
    })
    url = f"{BASE_URL}/esearch.fcgi?{params}"
    with urllib.request.urlopen(url) as resp:
        root = ET.parse(resp).getroot()
    return [id_elem.text for id_elem in root.findall(".//Id")]


def elink(dbfrom, dbto, ids):
    """Link records between NCBI databases."""
    params = urllib.parse.urlencode({
        "dbfrom": dbfrom,
        "db": dbto,
        "id": ",".join(ids) if isinstance(ids, list) else ids,
        "retmode": "xml",
        "email": EMAIL
    })
    url = f"{BASE_URL}/elink.fcgi?{params}"
    with urllib.request.urlopen(url) as resp:
        root = ET.parse(resp).getroot()
    return [id_elem.text for id_elem in root.findall(".//Link/Id")]


def get_cds_for_gene(gene_name, plasmodb_id):
    """Fetch CDS sequence for a gene using its PlasmoDB ID."""
    print(f"Fetching {gene_name} ({plasmodb_id})...")

    # Search Gene database for this gene
    gene_ids = esearch("gene", f"{plasmodb_id}[Gene Name] AND Plasmodium falciparum[Organism]")

    if not gene_ids:
        print(f"  WARNING: No gene found for {plasmodb_id}")
        return None

    time.sleep(0.34)

    # Get linked protein records (RefSeq: XP_)
    prot_ids = elink("gene", "protein", gene_ids[:1])

    if not prot_ids:
        print(f"  WARNING: No protein records linked for {plasmodb_id}")
        return None

    time.sleep(0.34)

    # Filter to get RefSeq protein (XP_) - first one is usually the primary
    # Fetch CDS nucleotide sequence from protein record
    params = urllib.parse.urlencode({
        "db": "protein",
        "id": prot_ids[0],
        "rettype": "fasta_cds_na",
        "retmode": "text",
        "email": EMAIL
    })
    url = f"{BASE_URL}/efetch.fcgi?{params}"
    with urllib.request.urlopen(url) as resp:
        fasta = resp.read().decode("utf-8")

    if fasta.strip() and not fasta.startswith("Error") and fasta.startswith(">"):
        lines = fasta.strip().split("\n")
        # Extract accession from original header
        match = re.search(r"protein_id=(\S+)\]", lines[0])
        prot_acc = match.group(1) if match else prot_ids[0]
        new_header = f">{gene_name}|{plasmodb_id}|{prot_acc}"
        lines[0] = new_header
        return "\n".join(lines)

    print(f"  WARNING: Could not retrieve CDS for {plasmodb_id}")
    return None


def main():
    output_file = "pf_drug_resistance_cds.fasta"
    sequences = []

    for gene_name, plasmodb_id in GENES:
        time.sleep(0.34)
        seq = get_cds_for_gene(gene_name, plasmodb_id)
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
