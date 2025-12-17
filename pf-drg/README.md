# P. falciparum Drug Resistance Genes

Analysis of *Plasmodium falciparum* drug resistance genes: CDS sequences, known mutations, and coordinate verification.

## Target Genes

| Gene | PlasmoDB ID | Description | Drug Association |
|------|-------------|-------------|------------------|
| Pfk13 | PF3D7_1343700 | kelch protein K13 | Artemisinin |
| pfmdr1 | PF3D7_0523000 | multidrug resistance protein 1 | CQ, MQ, LMF |
| Pfcrt | PF3D7_0709000 | chloroquine resistance transporter | Chloroquine |
| Pfdhfr | PF3D7_0417200 | dihydrofolate reductase-thymidylate synthase | Pyrimethamine |
| Pfdhps | PF3D7_0810800 | dihydropteroate synthase | Sulfadoxine |
| Pfubp1 | PF3D7_0104300 | ubiquitin carboxyl-terminal hydrolase 1 | Artemisinin |
| PfATP6 | PF3D7_0106300 | calcium-transporting ATPase (SERCA) | Artemisinin |
| MRP1 | PF3D7_0112200 | multidrug resistance-associated protein 1 | Multiple |
| MRP2 | PF3D7_1229100 | multidrug resistance-associated protein 2 | Multiple |

## Workflow

### Step 1: Fetch CDS Sequences from NCBI

`fetch_pf_cds.py` retrieves coding sequences for all 9 genes from NCBI using E-utilities API.

**Method:**
1. Search NCBI Gene database using PlasmoDB ID
2. Link to protein records (RefSeq XP_ accessions)
3. Fetch CDS nucleotide sequence via `fasta_cds_na` return type
4. Output multi-FASTA with standardized headers

```bash
python3 fetch_pf_cds.py
```

**Output:** `pf_drug_resistance_cds.fasta`

Header format: `>GeneName|PlasmoDB_ID|Protein_Accession`

### Step 2: Compile Drug Resistance Mutations

`pf_drug_resistance_mutations.tsv` contains 45 known resistance mutations compiled from literature.

**Columns:**
- `Gene` - Gene name
- `PlasmoDB_ID` - PlasmoDB identifier
- `Mutation` - Amino acid change (e.g., K76T)
- `Position` - Codon position (1-indexed)
- `Drug_Resistance` - Associated drug(s)
- `PubMed_IDs` - Supporting references

**Key references:**
- K13 artemisinin mutations: [PMID:29378723](https://pubmed.ncbi.nlm.nih.gov/29378723/)
- Pfcrt K76T chloroquine: [PMID:15944738](https://pubmed.ncbi.nlm.nih.gov/15944738/)
- pfmdr1 N86Y/Y184F: [PMID:27189525](https://pubmed.ncbi.nlm.nih.gov/27189525/)
- Pfdhfr/Pfdhps antifolates: [PMID:22314533](https://pubmed.ncbi.nlm.nih.gov/22314533/)
- Pfubp1 artemisinin: [PMID:31636063](https://pubmed.ncbi.nlm.nih.gov/31636063/)
- MRP proteins: [PMID:34790129](https://pubmed.ncbi.nlm.nih.gov/34790129/)

### Step 3: Verify Mutation Coordinates

`verify_mutations.py` validates that mutation positions match actual amino acids in 3D7 reference sequences.

**Method:**
1. Translate CDS sequences to protein (standard genetic code)
2. For each mutation (e.g., K76T), check that position 76 contains K
3. Report PASS/FAIL for each mutation

```bash
python3 verify_mutations.py
```

**Output:** `mutation_verification_report.tsv`

**Results:** 43 PASS, 1 FAIL, 1 SKIP

## Files

| File | Description |
|------|-------------|
| `fetch_pf_cds.py` | Script to fetch CDS from NCBI |
| `pf_drug_resistance_cds.fasta` | CDS sequences (9 genes, 3D7 strain) |
| `pf_drug_resistance_mutations.tsv` | Drug resistance mutations (45 entries) |
| `verify_mutations.py` | Mutation coordinate verification script |
| `mutation_verification_report.tsv` | Verification results |

## Dependencies

Python 3.6+ (standard library only—no external packages required)

## Notes

### 3D7 Reference Strain Caveat

The Pfdhps A437G mutation shows FAIL in verification because 3D7 already carries the resistant G437 allele. The 3D7 strain was isolated from a patient with likely African origin where sulfadoxine resistance was prevalent. This is expected behavior, not an error in coordinates.

### Sequence Source

All sequences are from *P. falciparum* 3D7 reference genome via NCBI RefSeq.
