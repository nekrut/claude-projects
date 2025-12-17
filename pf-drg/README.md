# *P. falciparum* Drug Resistance Genes

CDS sequences and validated resistance mutations for 9 *Plasmodium falciparum* drug resistance genes from the 3D7 reference genome.

## Genes

| Gene | PlasmoDB ID | NCBI Gene ID | Function | Drug |
|------|-------------|--------------|----------|------|
| Pfk13 | PF3D7_1343700 | 814205 | kelch protein K13 | Artemisinin |
| pfmdr1 | PF3D7_0523000 | 813045 | multidrug resistance protein 1 | CQ, MQ, LMF |
| Pfcrt | PF3D7_0709000 | 2655199 | chloroquine resistance transporter | Chloroquine |
| Pfdhfr | PF3D7_0417200 | 9221804 | dihydrofolate reductase | Pyrimethamine |
| Pfdhps | PF3D7_0810800 | 2655294 | dihydropteroate synthase | Sulfadoxine |
| Pfubp1 | PF3D7_0104300 | 813181 | ubiquitin hydrolase 1 | Artemisinin |
| PfATP6 | PF3D7_0106300 | 813199 | SERCA-type ATPase | Artemisinin |
| MRP1 | PF3D7_0112200 | 813255 | MRP transporter 1 | Multiple |
| MRP2 | PF3D7_1229100 | 811334 | MRP transporter 2 | Multiple |

## Files

| File | Description |
|------|-------------|
| `pf_drug_resistance_cds.fasta` | CDS sequences (9 genes) |
| `pf_drug_resistance_mutations.tsv` | 45 resistance mutations with coordinates and PubMed refs |
| `mutation_verification_report.tsv` | Coordinate validation results |
| `fetch_pf_cds.py` | Fetch CDS via NCBI datasets CLI |
| `verify_mutations.py` | Validate mutation coordinates against translated CDS |

## Usage

```bash
# Fetch CDS sequences
python3 fetch_pf_cds.py

# Verify mutation coordinates
python3 verify_mutations.py
```

## Mutations Table Format

`pf_drug_resistance_mutations.tsv` columns:
- **Gene** — gene name
- **PlasmoDB_ID** — PlasmoDB identifier
- **Mutation** — amino acid change (e.g., K76T)
- **Position** — codon position (1-indexed)
- **Drug_Resistance** — associated drug(s)
- **PubMed_IDs** — literature references

## Coordinate Verification

`verify_mutations.py` translates CDS to protein and checks that wild-type residues match mutation notation. For K76T, position 76 should contain K.

**Results:** 43 PASS, 1 FAIL, 1 SKIP

The single FAIL (Pfdhps A437G) is expected—3D7 carries the resistant G437 allele because it was isolated from a region with historical sulfadoxine use.

## Dependencies

- Python 3.6+
- NCBI datasets CLI: `conda install -c conda-forge ncbi-datasets-cli`

## References

| Topic | PMID |
|-------|------|
| K13 artemisinin mutations | [29378723](https://pubmed.ncbi.nlm.nih.gov/29378723/) |
| Pfcrt K76T | [15944738](https://pubmed.ncbi.nlm.nih.gov/15944738/) |
| pfmdr1 N86Y/Y184F | [27189525](https://pubmed.ncbi.nlm.nih.gov/27189525/) |
| Pfdhfr/Pfdhps antifolates | [22314533](https://pubmed.ncbi.nlm.nih.gov/22314533/) |
| Pfubp1 artemisinin | [31636063](https://pubmed.ncbi.nlm.nih.gov/31636063/) |
| MRP proteins | [34790129](https://pubmed.ncbi.nlm.nih.gov/34790129/) |
