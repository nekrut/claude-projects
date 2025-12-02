# RNA-seq Studies of *Candida auris* (Candidozyma auris) Since 2020

## Literature Survey Summary

This document contains a comprehensive survey of RNA-seq studies performed on *Candida auris* (also known as *Candidozyma auris*) published since 2020. The table below summarizes key information about each study including the genome version used, type of RNA-seq analysis performed, and bioinformatics tools employed.

## RNA-seq Studies Table

| PubMed ID | Genome Version | Type of RNA-seq | Tools Used |
|-----------|----------------|-----------------|------------|
| [32581078](https://pubmed.ncbi.nlm.nih.gov/32581078/) | N/A | Differential expression analysis of biofilm vs. planktonic cells | N/A (not specified in abstract) |
| [33937102](https://pubmed.ncbi.nlm.nih.gov/33937102/) | B11221 (GCF_002775015.1) | Differential expression analysis comparing clinical isolates | FastQC, cutadapt, NextGenMap, Picard, HTseq, edgeR, clusterProfiler |
| [34354695](https://pubmed.ncbi.nlm.nih.gov/34354695/) | N/A (specific reference genome) | Differential expression analysis: drug-sensitive vs. resistant strains | HISAT2, Cufflinks, HTSeq-count, DEseq, Trimmomatic, pheatmap, STRING database |
| [34485470](https://pubmed.ncbi.nlm.nih.gov/34485470/) | GCA_002759435 (Ensembl Fungi) | Differential expression analysis: farnesol response | DESeq (StrandNGS software), Agilent BioAnalyzer, NEBNext Ultra II kit, Candida Genome Database |
| [34788438](https://pubmed.ncbi.nlm.nih.gov/34788438/) | B8441 (GCA_002759435.2 V2) | Small RNA sequencing of cellular and extracellular vesicles | CLC Genomics Workbench v20, TMM normalization, TruSeq small RNA kit, qRT-PCR |
| [35652307](https://pubmed.ncbi.nlm.nih.gov/35652307/) | B8441 (Candida Genome Database) | Comparative transcriptomics: AmB-resistant vs. sensitive isolates | HISAT2, HTSeq, DESeq2, Orange3, BioVenn, Fungifun2, Gene Ontology Term Finder |
| [37350781](https://pubmed.ncbi.nlm.nih.gov/37350781/) | B11221 | Transcriptomic profiling: rough vs. smooth morphotypes | Bowtie2, HISAT2, HTSeq, DESeq, topGO, KOBAS, Pheatmap |
| [38990436](https://pubmed.ncbi.nlm.nih.gov/38990436/) | N/A | Comparative transcriptomics: host dermal cells infected with *C. auris* | qRT-PCR, flow cytometry, KEGG, Reactome analyses |
| N/A (2024) | B11221 | Differential expression analysis: reduced AmB sensitivity | DESeq2, KEGG, Gene Ontology, STRING database, qPCR |

## Key Findings

### 1. Most Common Genome Reference Versions

- **B8441 (GCA_002759435)** - Clade I reference strain, widely used
- **B11221 (GCF_002775015.1)** - Clade III reference strain
- Several studies did not specify genome version in accessible materials

### 2. Types of RNA-seq Analysis

The predominant type of analysis across all studies was **differential expression analysis**, with various experimental contexts:

- **Drug resistance mechanisms**: Comparing antifungal-resistant vs. sensitive strains (azoles, amphotericin B)
- **Biofilm formation**: Biofilm vs. planktonic cell gene expression
- **Morphological variations**: Rough vs. smooth morphotypes, aggregative vs. non-aggregative phenotypes
- **Stress responses**: Response to farnesol and other compounds
- **Small RNA profiling**: Cellular and extracellular vesicle RNA content
- **Host-pathogen interactions**: Transcriptomic changes in host cells during infection

### 3. Most Commonly Used Bioinformatics Tools

#### Alignment/Mapping:
- HISAT2 (most common)
- Bowtie2
- NextGenMap
- CLC Genomics Workbench

#### Quantification:
- HTSeq (most common)
- Cufflinks
- Kallisto
- FPKM calculation

#### Statistical Analysis:
- **DESeq2** (most common)
- DESeq
- edgeR

#### Quality Control:
- FastQC
- Trimmomatic
- cutadapt
- Agilent BioAnalyzer

#### Functional Annotation:
- Gene Ontology Term Finder
- KEGG pathway analysis
- STRING database (protein-protein interactions)
- Fungifun2
- topGO
- KOBAS
- clusterProfiler

#### Visualization:
- Pheatmap (heatmaps)
- Orange3
- BioVenn

### 4. Common Analysis Thresholds

Most studies used similar statistical cutoffs for identifying differentially expressed genes (DEGs):

- **Fold change**: ≥1.5-fold or ≥2-fold (log2FC ≥ 0.585 or 1)
- **Statistical significance**: FDR/adjusted p-value < 0.05
- **Some studies**: Padj < 0.05

## Study Details

### PMID: 32581078 (2020)
**Title**: Candida auris Phenotypic Heterogeneity Determines Pathogenicity In Vitro

**Focus**: Transcriptional responses during biofilm formation in nonaggregative vs. aggregative isolates (NCPF 8973 and NCPF 8978)

**Key Finding**: Unique transcriptional profiles with genes related to adhesion and invasion showing differential expression

---

### PMID: 33937102 (2021)
**Title**: Transcriptome Signatures Predict Phenotypic Variations of Candida auris

**Focus**: Genome-wide transcript profiling of clinical isolates from different clades

**Key Finding**: Large gene expression differences between clade I isolates; transcriptional signatures predict phenotypic variations

**Full PMC**: [PMC8079977](https://pmc.ncbi.nlm.nih.gov/articles/PMC8079977/)

---

### PMID: 34354695 (2021)
**Title**: A Comparative Transcriptome Between Anti-drug Sensitive and Resistant Candida auris in China

**Focus**: Transcriptomic comparison of drug-sensitive (CX1) vs. resistant (CX2) isolates

**Key Finding**: 541 upregulated and 453 downregulated genes in resistant strain; protein interaction networks identified

**Full text**: [Frontiers](https://www.frontiersin.org/articles/10.3389/fmicb.2021.708009/full)

---

### PMID: 34485470 (2021)
**Title**: Transcriptional Profiling of the Candida auris Response to Exogenous Farnesol Exposure

**Focus**: Response to farnesol, a quorum-sensing molecule

**Key Finding**: Identified genes differentially expressed in response to farnesol treatment

**Full PMC**: [PMC8513684](https://pmc.ncbi.nlm.nih.gov/articles/PMC8513684/)

---

### PMID: 34788438 (2021)
**Title**: Cellular and Extracellular Vesicle RNA Analysis in the Global Threat Fungus Candida auris

**Focus**: Small RNA sequencing of cellular and extracellular vesicle (EV) content

**Key Finding**: Comparison of RNA cargo between cells and EVs; response to caspofungin treatment

**Full PMC**: [PMC8672890](https://pmc.ncbi.nlm.nih.gov/articles/PMC8672890/)

---

### PMID: 35652307 (2022)
**Title**: Comparative Transcriptomics Reveal Possible Mechanisms of Amphotericin B Resistance in Candida auris

**Focus**: Amphotericin B (AmB)-resistant vs. sensitive isolates

**Key Finding**: AmB-resistant strains show enrichment of genes in lipid/ergosterol biosynthesis, adhesion, drug transport, and chromatin remodeling

**Full PMC**: [PMC9211394](https://pmc.ncbi.nlm.nih.gov/articles/PMC9211394/)

---

### PMID: 37350781 (2023)
**Title**: Phenotypic and genetic features of a novel clinically isolated rough morphotype Candida auris

**Focus**: RNA-seq comparison of rough morphotype vs. smooth morphotype strains

**Key Finding**: IFF2/HYR3, DAL5, PSA31, and SIT1 notably upregulated in rough morphotype; cell wall-associated genes downregulated

**Full text**: [Frontiers](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2023.1174878/full)

---

### PMID: 38990436 (2024)
**Title**: Transcriptome Analysis of Human Dermal Cells Infected with Candida auris Identified Unique Pathogenesis/Defensive Mechanisms Particularly Ferroptosis

**Focus**: Host cell transcriptomic response to *C. auris* infection

**Key Finding**: Identified ferroptosis as a unique pathogenesis/defense mechanism in host dermal cells

---

### 2024 Study (PMC11385638)
**Title**: Genetic microevolution of clinical Candida auris with reduced Amphotericin B sensitivity in China

**Focus**: Microevolution and reduced AmB sensitivity across patient isolates

**Key Finding**: Transcriptomic analysis revealed DEGs associated with AmB resistance development

**Full PMC**: [PMC11385638](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385638/)

---

## Additional Studies (2018-2019, Pre-2020 Baseline)

### PMID: 29997121 (2018)
**Title**: Transcriptome Assembly and Profiling of Candida auris Reveals Novel Insights into Biofilm-Mediated Resistance

**Focus**: De novo transcriptome assembly and temporal biofilm development analysis

**Key Finding**: First transcriptomic analysis of temporally developing *C. auris* biofilms; assembled ~11.5-Mb transcriptome with 5,848 genes

**Tools**: Trinity, HISAT2, Kallisto, DESeq2, TransDecoder, Trinotate, BUSCO, BLAST2GO

**Genome**: RefSeq B8441

**Full PMC**: [PMC6041501](https://pmc.ncbi.nlm.nih.gov/articles/PMC6041501/)

---

## Research Trends and Observations

1. **Drug resistance is the dominant research focus**, particularly:
   - Azole resistance (fluconazole)
   - Amphotericin B resistance
   - Multi-drug resistance mechanisms

2. **Biofilm formation** is a recurring theme across multiple studies

3. **Phenotypic heterogeneity** including aggregative vs. non-aggregative and rough vs. smooth morphotypes

4. **Standardization**: Most studies converge on similar bioinformatics pipelines (HISAT2 → HTSeq → DESeq2)

5. **Reference genome usage**: B8441 (Clade I) and B11221 (Clade III) are the most common reference strains

6. **Emerging areas**:
   - Host-pathogen interaction transcriptomics
   - Small RNA and extracellular vesicle studies
   - Epigenetic regulation (chromatin remodeling)

---

## Data Sources

All information compiled from PubMed and PubMed Central searches conducted on December 2, 2025.

Search terms included:
- "Candida auris RNA-seq"
- "Candidozyma auris transcriptome"
- "Candida auris differential expression"
- Various combinations with specific years (2020-2025)

---

**Document created**: December 2, 2025
**Last updated**: December 2, 2025
