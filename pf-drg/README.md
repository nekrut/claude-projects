# *P. falciparum* Drug Resistance Genes

This repository contains coding sequences (CDS) and validated drug resistance mutations for 9 *Plasmodium falciparum* genes implicated in antimalarial drug resistance. All sequences derive from the 3D7 reference genome.

## Background

Antimalarial drug resistance poses a major threat to malaria control. Resistance emerges through point mutations in parasite genes encoding drug targets or transporters. Monitoring these mutations is critical for treatment policy and surveillance. This dataset compiles the primary resistance markers for:

- **Artemisinin** — K13 kelch propeller mutations (C580Y, R539T, etc.)
- **Chloroquine** — Pfcrt K76T and pfmdr1 N86Y
- **Sulfadoxine-pyrimethamine** — Pfdhfr/Pfdhps mutations (quintuple mutant)
- **Mefloquine/Lumefantrine** — pfmdr1 copy number and SNPs

## Target Genes

| Gene | PlasmoDB ID | NCBI Gene ID | Description | Drug Association |
|------|-------------|--------------|-------------|------------------|
| Pfk13 | PF3D7_1343700 | 814205 | Kelch protein K13; BTB/POZ and kelch domains | Artemisinin |
| pfmdr1 | PF3D7_0523000 | 813045 | P-glycoprotein homolog; ABC transporter | CQ, MQ, LMF, AQ |
| Pfcrt | PF3D7_0709000 | 2655199 | Chloroquine resistance transporter; digestive vacuole membrane | Chloroquine |
| Pfdhfr | PF3D7_0417200 | 9221804 | Dihydrofolate reductase-thymidylate synthase; folate pathway | Pyrimethamine |
| Pfdhps | PF3D7_0810800 | 2655294 | Dihydropteroate synthase; folate pathway | Sulfadoxine |
| Pfubp1 | PF3D7_0104300 | 813181 | Ubiquitin carboxyl-terminal hydrolase 1; protein turnover | Artemisinin |
| PfATP6 | PF3D7_0106300 | 813199 | SERCA-type calcium ATPase; ER calcium pump | Artemisinin |
| MRP1 | PF3D7_0112200 | 813255 | Multidrug resistance-associated protein 1; ABC transporter | Multiple |
| MRP2 | PF3D7_1229100 | 811334 | Multidrug resistance-associated protein 2; ABC transporter | Multiple |

## Workflow

### Step 1: Retrieve CDS Sequences

`fetch_pf_cds.py` downloads coding sequences from NCBI using the `datasets` CLI tool.

**Process:**
1. For each gene, call `datasets download gene gene-id <ID> --include cds`
2. Extract `cds.fna` from the downloaded zip archive
3. Reformat FASTA headers to `>GeneName|PlasmoDB_ID|Accession`
4. Concatenate all sequences into a single multi-FASTA file

**Run:**
```bash
python3 fetch_pf_cds.py
```

**Output:** `pf_drug_resistance_cds.fasta`

**Example header:**
```
>Pfk13|PF3D7_1343700|XM_001350122.1:1-2181
```

### Step 2: Compile Resistance Mutations

`pf_drug_resistance_mutations.tsv` contains 45 literature-curated mutations across all 9 genes. Each entry includes:

| Column | Description |
|--------|-------------|
| Gene | Gene name |
| PlasmoDB_ID | PlasmoDB gene identifier |
| Mutation | Amino acid substitution (e.g., K76T = Lys→Thr at position 76) |
| Position | Codon position in protein (1-indexed) |
| Drug_Resistance | Associated drug(s) |
| PubMed_IDs | Supporting publication PMIDs |

**Mutation counts by gene:**

| Gene | Mutations | Primary Markers |
|------|-----------|-----------------|
| Pfk13 | 10 | C580Y, R539T, Y493H |
| pfmdr1 | 5 | N86Y, Y184F, D1246Y |
| Pfcrt | 9 | K76T (key marker) |
| Pfdhfr | 4 | N51I, C59R, S108N, I164L |
| Pfdhps | 5 | A437G, K540E, A581G |
| Pfubp1 | 4 | V3275F, D1525E |
| PfATP6 | 3 | L263E, S769N |
| MRP1 | 4 | H191Y, K1466R |
| MRP2 | 1 | Multiple SNPs |

### Step 3: Verify Mutation Coordinates

`verify_mutations.py` validates that mutation positions correspond to the expected wild-type amino acids in the 3D7 reference protein sequences.

**Process:**
1. Read CDS sequences from `pf_drug_resistance_cds.fasta`
2. Translate to protein using standard genetic code
3. For each mutation (e.g., K76T):
   - Parse wild-type residue (K) and position (76)
   - Check that position 76 in the translated protein contains K
4. Report PASS if match, FAIL if mismatch

**Run:**
```bash
python3 verify_mutations.py
```

**Output:** `mutation_verification_report.tsv`

**Results:**
- 43 PASS — coordinate matches expected wild-type residue
- 1 FAIL — Pfdhps A437G (see note below)
- 1 SKIP — MRP2 (complex polymorphisms, no single coordinate)

### Note on Pfdhps A437G

The Pfdhps A437G verification fails because the 3D7 reference strain already carries the resistant **G437** allele rather than wild-type A437. This is expected: 3D7 was isolated from a patient in the Netherlands (likely of African origin) where sulfadoxine-pyrimethamine resistance was prevalent. The mutation coordinate is correct; the reference strain simply carries the mutant allele.

## Files

| File | Description |
|------|-------------|
| `fetch_pf_cds.py` | Python script to fetch CDS from NCBI via datasets CLI |
| `pf_drug_resistance_cds.fasta` | CDS nucleotide sequences for 9 genes |
| `pf_drug_resistance_mutations.tsv` | 45 resistance mutations with positions and PubMed refs |
| `verify_mutations.py` | Python script to validate mutation coordinates |
| `mutation_verification_report.tsv` | Verification results (PASS/FAIL/SKIP) |

## Dependencies

- **Python 3.6+** (standard library only; no pip packages)
- **NCBI datasets CLI** — install via conda:
  ```bash
  conda install -c conda-forge ncbi-datasets-cli
  ```

## References

| Gene/Topic | Key PMID | Citation |
|------------|----------|----------|
| K13 validated mutations | [29378723](https://pubmed.ncbi.nlm.nih.gov/29378723/) | Emergence of K13 mutations in Thailand |
| K13 C580Y | [31563454](https://pubmed.ncbi.nlm.nih.gov/31563454/) | C580Y in Greater Mekong Subregion |
| Pfcrt K76T | [15944738](https://pubmed.ncbi.nlm.nih.gov/15944738/) | Critical role of K76T in CQ resistance |
| Pfcrt haplotypes | [24402147](https://pubmed.ncbi.nlm.nih.gov/24402147/) | Genetics of CQ resistance |
| pfmdr1 N86Y/Y184F | [27189525](https://pubmed.ncbi.nlm.nih.gov/27189525/) | PfMDR1 modulates ACT susceptibility |
| Pfdhfr mutations | [22314533](https://pubmed.ncbi.nlm.nih.gov/22314533/) | Pyrimethamine resistance mutations |
| Pfdhps mutations | [30914041](https://pubmed.ncbi.nlm.nih.gov/30914041/) | SP resistance in Equatorial Guinea |
| Pfubp1 | [31636063](https://pubmed.ncbi.nlm.nih.gov/31636063/) | pfap2μ and pfubp1 in artemisinin resistance |
| PfATP6 | [20566762](https://pubmed.ncbi.nlm.nih.gov/20566762/) | PfATP6 L263E and artemisinin |
| MRP proteins | [34790129](https://pubmed.ncbi.nlm.nih.gov/34790129/) | Review of PfMRP1/MRP2 |

## Sequence Source

All sequences derive from *Plasmodium falciparum* 3D7 (GCF_000002765.6) via NCBI RefSeq.
