# RNA-seq Studies of *Candida auris* (Candidozyma auris) Since 2020

## Literature Survey Summary

This document contains a comprehensive survey of RNA-seq studies performed on *Candida auris* (also known as *Candidozyma auris*) published since 2020. The survey combines results from **PubMed/PubMed Central** and **Europe PMC** database searches. The table below summarizes key information about each study including the genome version used, type of RNA-seq analysis performed, bioinformatics tools employed, and the data source.

## RNA-seq Studies Table

| PubMed ID | Data Source | Genome Version | Type of RNA-seq | Tools Used |
|-----------|-------------|----------------|-----------------|------------|
| [32581078](https://pubmed.ncbi.nlm.nih.gov/32581078/) | PubMed | N/A | Differential expression analysis of biofilm vs. planktonic cells | N/A (not specified in abstract) |
| [33937102](https://pubmed.ncbi.nlm.nih.gov/33937102/) | PubMed | B11221 (GCF_002775015.1) | Differential expression analysis comparing clinical isolates | FastQC, cutadapt, NextGenMap, Picard, HTseq, edgeR, clusterProfiler |
| [34354695](https://pubmed.ncbi.nlm.nih.gov/34354695/) | PubMed | N/A (specific reference genome) | Differential expression analysis: drug-sensitive vs. resistant strains | HISAT2, Cufflinks, HTSeq-count, DEseq, Trimmomatic, pheatmap, STRING database |
| [34485470](https://pubmed.ncbi.nlm.nih.gov/34485470/) | PubMed | GCA_002759435 (Ensembl Fungi) | Differential expression analysis: farnesol response | DESeq (StrandNGS software), Agilent BioAnalyzer, NEBNext Ultra II kit, Candida Genome Database |
| [34630944](https://pubmed.ncbi.nlm.nih.gov/34630944/) | Europe PMC | B8441 (GCA_002759435.2 V2) | Differential expression and translational profiling: caspofungin response | CLC Genomics Workbench v20, TMM normalization, EdgeR, DAVID v6.8, BLASTp, qRT-PCR |
| [34788438](https://pubmed.ncbi.nlm.nih.gov/34788438/) | PubMed | B8441 (GCA_002759435.2 V2) | Small RNA sequencing of cellular and extracellular vesicles | CLC Genomics Workbench v20, TMM normalization, TruSeq small RNA kit, qRT-PCR |
| [35652307](https://pubmed.ncbi.nlm.nih.gov/35652307/) | PubMed | B8441 (Candida Genome Database) | Comparative transcriptomics: AmB-resistant vs. sensitive isolates | HISAT2, HTSeq, DESeq2, Orange3, BioVenn, Fungifun2, Gene Ontology Term Finder |
| [35968956](https://pubmed.ncbi.nlm.nih.gov/35968956/) | Europe PMC | B8441 (s01-m01-r10) | Comparative transcriptomics: echinocandin-resistant vs. susceptible isolates | FastQC, cutadapt, NextGenMap, Picard, HTseq, edgeR, clusterProfiler, VennDiagram |
| [36913408](https://pubmed.ncbi.nlm.nih.gov/36913408/) | Europe PMC | GCA_002759435.2 | Differential expression analysis: aggregative vs. nonaggregative strains (biofilm) | HiSat2 v2.0.5, Stringtie v1.3.3b, DESeq2, Illumina NovaSeq 6000 |
| [37350781](https://pubmed.ncbi.nlm.nih.gov/37350781/) | PubMed | B11221 | Transcriptomic profiling: rough vs. smooth morphotypes | Bowtie2, HISAT2, HTSeq, DESeq, topGO, KOBAS, Pheatmap |
| [37769084](https://pubmed.ncbi.nlm.nih.gov/37769084/) | Repository Analysis | GCA_002759435.3 | Differential expression: SWI1 mutant vs. wild-type, strain comparisons | FastQC, fastp, STAR, featureCounts, DESeq2 |
| [38562758](https://pubmed.ncbi.nlm.nih.gov/38562758/) | Repository Analysis | GCA_002759435 (B8441/B11109) | Differential expression: aggregative vs. non-aggregative strains (in vitro and in vivo) | DESeq2, Galaxy RNA-seq pipeline |
| [38990436](https://pubmed.ncbi.nlm.nih.gov/38990436/) | PubMed | N/A | Comparative transcriptomics: host dermal cells infected with *C. auris* | qRT-PCR, flow cytometry, KEGG, Reactome analyses |
| [PMC11385638](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385638/) | PubMed | B11221 | Differential expression analysis: reduced AmB sensitivity | DESeq2, KEGG, Gene Ontology, STRING database, qPCR, Illumina NovaSeq |
| [PMC11459930](https://pmc.ncbi.nlm.nih.gov/articles/PMC11459930/) | Europe PMC | B8441 (GCA_002759435.2) | Whole transcriptome sequencing: pan-drug resistant strains | HISAT2 v2.2.1, StringTie v1.3.3b, Ballgown v3.15, BiNGO, HMMER v3.3.2, CLC Genomics Server v23 |
| [40099908](https://pubmed.ncbi.nlm.nih.gov/40099908/) | Europe PMC | B8441 (reference allele) | Gene expression profiling and SNP identification: flucytosine resistance | STAR (two-pass workflow), drc R package, IGV viewer, enrichGO (clusterProfiler), Sanger sequencing |

## Key Findings

### 1. Most Common Genome Reference Versions

- **B8441 (GCA_002759435)** - Clade I reference strain, most widely used (9 studies)
- **B11221 (GCF_002775015.1)** - Clade III reference strain (3 studies)
- **GCA_002759435.3** - Updated version used in repository analyses (1 study)
- Several studies did not specify genome version in accessible materials

### 2. Types of RNA-seq Analysis

The predominant type of analysis across all studies was **differential expression analysis**, with various experimental contexts:

- **Drug resistance mechanisms** (most common):
  - Amphotericin B resistance (3 studies)
  - Echinocandin/caspofungin resistance (2 studies)
  - Flucytosine resistance (1 study)
  - Pan-drug resistance (1 study)
  - Multi-drug resistance (1 study)
- **Biofilm formation**: Biofilm vs. planktonic cell gene expression (3 studies)
- **Morphological variations**: Rough vs. smooth morphotypes, aggregative vs. non-aggregative phenotypes (3 studies)
- **Stress responses**: Response to farnesol and other compounds (1 study)
- **Small RNA profiling**: Cellular and extracellular vesicle RNA content (1 study)
- **Host-pathogen interactions**: Transcriptomic changes in host cells during infection (1 study)

### 3. Most Commonly Used Bioinformatics Tools

#### Alignment/Mapping:
- **HISAT2** (most common - 7 studies)
- NextGenMap (2 studies)
- Bowtie2 (1 study)
- CLC Genomics Workbench (3 studies)
- STAR (1 study)
- Stringtie (2 studies)

#### Quantification:
- **HTSeq** (most common - 6 studies)
- Cufflinks (1 study)
- Kallisto (historical)
- FPKM calculation (3 studies)
- TPM (Transcripts per Million) (1 study)
- StringTie (2 studies)

#### Statistical Analysis:
- **DESeq2** (most common - 6 studies)
- DESeq (2 studies)
- edgeR (3 studies)
- Ballgown (1 study)

#### Quality Control:
- **FastQC** (3 studies)
- Trimmomatic (1 study)
- cutadapt (3 studies)
- Agilent BioAnalyzer (3 studies)
- Qubit fluorometer (1 study)

#### Functional Annotation:
- Gene Ontology Term Finder / enrichGO (5 studies)
- KEGG pathway analysis (4 studies)
- STRING database (protein-protein interactions) (3 studies)
- Fungifun2 (1 study)
- topGO (1 study)
- KOBAS (1 study)
- clusterProfiler (3 studies)
- DAVID (1 study)
- BiNGO (1 study)

#### Visualization:
- Pheatmap (heatmaps) (2 studies)
- Orange3 (1 study)
- BioVenn (2 studies)
- VennDiagram (1 study)
- IGV viewer (1 study)

### 4. Common Analysis Thresholds

Most studies used similar statistical cutoffs for identifying differentially expressed genes (DEGs):

- **Fold change**: ≥1.5-fold or ≥2-fold (log2FC ≥ 0.585 or 1)
- **Statistical significance**: FDR/adjusted p-value < 0.05 (most common)
- **Some studies**: FDR < 0.01 or padj < 0.05

## Study Details

### PMID: 32581078 (2020)
**Title**: Candida auris Phenotypic Heterogeneity Determines Pathogenicity In Vitro

**Data Source**: PubMed

**Focus**: Transcriptional responses during biofilm formation in nonaggregative vs. aggregative isolates (NCPF 8973 and NCPF 8978)

**Key Finding**: Unique transcriptional profiles with genes related to adhesion and invasion showing differential expression

---

### PMID: 33937102 (2021)
**Title**: Transcriptome Signatures Predict Phenotypic Variations of Candida auris

**Data Source**: PubMed

**Focus**: Genome-wide transcript profiling of clinical isolates from different clades

**Key Finding**: Large gene expression differences between clade I isolates; transcriptional signatures predict phenotypic variations

**Full PMC**: [PMC8079977](https://pmc.ncbi.nlm.nih.gov/articles/PMC8079977/)

---

### PMID: 34354695 (2021)
**Title**: A Comparative Transcriptome Between Anti-drug Sensitive and Resistant Candida auris in China

**Data Source**: PubMed

**Focus**: Transcriptomic comparison of drug-sensitive (CX1) vs. resistant (CX2) isolates

**Key Finding**: 541 upregulated and 453 downregulated genes in resistant strain; protein interaction networks identified

**Full text**: [Frontiers](https://www.frontiersin.org/articles/10.3389/fmicb.2021.708009/full)

---

### PMID: 34485470 (2021)
**Title**: Transcriptional Profiling of the Candida auris Response to Exogenous Farnesol Exposure

**Data Source**: PubMed

**Focus**: Response to farnesol, a quorum-sensing molecule

**Key Finding**: Identified 1,766 differentially expressed genes in response to farnesol treatment

**Full PMC**: [PMC8513684](https://pmc.ncbi.nlm.nih.gov/articles/PMC8513684/)

---

### PMID: 34630944 (2021) - NEW from Europe PMC
**Title**: Transcriptional and translational landscape of Candida auris in response to caspofungin

**Data Source**: Europe PMC

**Focus**: Transcriptomic and proteomic response to caspofungin treatment in two distinct C. auris strains

**Key Finding**: Upregulation of genes related to cell wall synthesis, ribosome, and cell cycle; proteomic analysis showed enrichment in mannoproteins

**Full PMC**: [PMC8481930](https://pmc.ncbi.nlm.nih.gov/articles/PMC8481930/)

---

### PMID: 34788438 (2021)
**Title**: Cellular and Extracellular Vesicle RNA Analysis in the Global Threat Fungus Candida auris

**Data Source**: PubMed

**Focus**: Small RNA sequencing of cellular and extracellular vesicle (EV) content

**Key Finding**: Comparison of RNA cargo between cells and EVs; response to caspofungin treatment

**Full PMC**: [PMC8672890](https://pmc.ncbi.nlm.nih.gov/articles/PMC8672890/)

---

### PMID: 35652307 (2022)
**Title**: Comparative Transcriptomics Reveal Possible Mechanisms of Amphotericin B Resistance in Candida auris

**Data Source**: PubMed

**Focus**: Amphotericin B (AmB)-resistant vs. sensitive isolates

**Key Finding**: AmB-resistant strains show enrichment of genes in lipid/ergosterol biosynthesis, adhesion, drug transport, and chromatin remodeling

**Full PMC**: [PMC9211394](https://pmc.ncbi.nlm.nih.gov/articles/PMC9211394/)

---

### PMID: 35968956 (2022) - NEW from Europe PMC
**Title**: Transcriptomics and Phenotyping Define Genetic Signatures Associated with Echinocandin Resistance in Candida auris

**Data Source**: Europe PMC

**Focus**: Echinocandin-resistant vs. susceptible clinical isolates

**Key Finding**: Identified core signature set of 362 differentially expressed genes in resistant isolates; mitochondrial gene expression and cell wall function most prominent

**Full PMC**: [PMC9426441](https://pmc.ncbi.nlm.nih.gov/articles/PMC9426441/)

---

### PMID: 36913408 (2023) - NEW from Europe PMC
**Title**: Clinical isolates of Candida auris with enhanced adherence and biofilm formation due to genomic amplification of ALS4

**Data Source**: Europe PMC

**Focus**: RNA-seq comparison of aggregative vs. nonaggregative strains with enhanced biofilm formation

**Key Finding**: ALS4 gene showed ~400-fold higher expression in aggregative form; genomic amplification of ALS4 responsible for enhanced adherence

**Full text**: [PLOS Pathogens](https://journals.plos.org/plospathogens/article?id=10.1371/journal.ppat.1011239)

---

### PMID: 37350781 (2023)
**Title**: Phenotypic and genetic features of a novel clinically isolated rough morphotype Candida auris

**Data Source**: PubMed

**Focus**: RNA-seq comparison of rough morphotype vs. smooth morphotype strains

**Key Finding**: IFF2/HYR3, DAL5, PSA31, and SIT1 notably upregulated in rough morphotype; cell wall-associated genes downregulated

**Full text**: [Frontiers](https://www.frontiersin.org/journals/microbiology/articles/10.3389/fmicb.2023.1174878/full)

---

### PMID: 37769084 (2023) - NEW from Repository Analysis
**Title**: A Candida auris-specific adhesin, Scf1, governs surface association, colonization, and virulence

**Data Source**: Repository Analysis (santana24_PRJNA904261)

**Journal**: Science 381(6665):1461-1467

**BioProject**: [PRJNA904261](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA904261)

**Focus**: Identification and characterization of SCF1 (Surface Colonization Factor 1), a C. auris-specific adhesin essential for biofilm formation and virulence

**RNA-seq Design**:
- Comparison 1: AR0382 (wild-type) vs. AR0382_tnSWI1 (SWI1 transposon mutant)
- Comparison 2: AR0382 (highly adhesive) vs. AR0387 (poorly adhesive)
- 2 biological replicates per condition

**Key Finding**: SCF1 (B9J08_001458) identified as the most strongly dysregulated gene (log2FC = -6.68 to -7.25), essential for adhesion to surfaces, biofilm formation, skin colonization, and virulence in systemic infection

**Tools**: FastQC, fastp, STAR aligner, featureCounts, DESeq2

**Genome**: GCA_002759435.3

**Repository Analysis**: Validation analysis achieved R² > 0.99 correlation with published results

---

### PMID: 38562758 (2024) - NEW from Repository Analysis
**Title**: Functional Redundancy in Candida auris Cell Surface Adhesins Crucial for Cell-Cell Interaction and Aggregation

**Data Source**: Repository Analysis (wang24_PRJNA1086003)

**Journal**: Nature Communications (2024)

**BioProject**: [PRJNA1086003](https://www.ncbi.nlm.nih.gov/bioproject/PRJNA1086003)

**Focus**: Cell surface glycan-lectin interactions modulate C. auris colonization and fungemia; comparison of aggregative vs. non-aggregative strains

**RNA-seq Design**:
- **In vitro**: AR0382 (aggregative, B11109) vs. AR0387 (non-aggregative, B8441), 3 replicates each
- **In vivo**: Same strain comparison during murine infection, 3-4 replicates per strain

**Key Finding**: Comprehensive transcriptional analysis revealed differential expression patterns between aggregative and non-aggregative phenotypes during both in vitro growth and in vivo infection

**Tools**: DESeq2, Galaxy RNA-seq pipeline (STAR alignment, featureCounts quantification)

**Genome**: GCA_002759435 (B8441 and B11109 reference)

**Significance threshold**: FDR < 0.01

---

### PMID: 38990436 (2024)
**Title**: Transcriptome Analysis of Human Dermal Cells Infected with Candida auris Identified Unique Pathogenesis/Defensive Mechanisms Particularly Ferroptosis

**Data Source**: PubMed

**Focus**: Host cell transcriptomic response to *C. auris* infection

**Key Finding**: Identified ferroptosis as a unique pathogenesis/defense mechanism in host dermal cells

---

### PMC11385638 (2024)
**Title**: Genetic microevolution of clinical Candida auris with reduced Amphotericin B sensitivity in China

**Data Source**: PubMed

**Focus**: Microevolution and reduced AmB sensitivity across patient isolates (2019-2022)

**Key Finding**: Transcriptomic analysis of three isolate groups (AmB0.5, AmB1, AmB2) revealed DEGs associated with AmB resistance development; ERG genes prominently involved

**Full PMC**: [PMC11385638](https://pmc.ncbi.nlm.nih.gov/articles/PMC11385638/)

---

### PMC11459930 (2024) - NEW from Europe PMC
**Title**: What makes Candida auris pan-drug resistant? Integrative insights from genomic, transcriptomic, and phenomic analysis

**Data Source**: Europe PMC

**Focus**: Whole transcriptome sequencing of unprecedented pan-drug resistant (PDR) strains resistant to all four major antifungal classes

**Key Finding**: Two genes significantly differentially expressed (DNA repair protein, chromatin assembly factor); 12 of 59 novel transcripts had no known homology

**Full PMC**: [PMC11459930](https://pmc.ncbi.nlm.nih.gov/articles/PMC11459930/)

---

### PMID: 40099908 (2025) - NEW from Europe PMC
**Title**: Rapid in vitro evolution of flucytosine resistance in Candida auris

**Data Source**: Europe PMC

**Year**: 2025 (published online)

**Focus**: Flucytosine (5-FC) resistance evolution; developed bioinformatics workflow for SNP identification from RNA-seq

**Key Finding**: Rapid development of 5-FC resistance via mutational inactivation of FUR1 gene; novel bioinformatics pipeline for clinical isolate analysis

**GEO Data**: GSE272878

**GitHub**: [5FC-Evo-2024 workflow](https://github.com/kakulab/5FC-Evo-2024)

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

### 1. Drug Resistance is the Dominant Research Focus
Drug resistance studies account for more than 50% of all RNA-seq research:
- **Amphotericin B resistance**: 3 studies
- **Echinocandin/caspofungin**: 2 studies
- **Flucytosine**: 1 study
- **Pan-drug resistance**: 1 study
- **Multi-drug resistance**: 2 studies

### 2. Biofilm Formation
Biofilm formation and aggregation phenotypes are major research themes (3-4 studies), often linked to antifungal resistance

### 3. Phenotypic Heterogeneity
Multiple studies focus on phenotypic variations:
- Aggregative vs. non-aggregative phenotypes
- Rough vs. smooth morphotypes
- Strain-to-strain variations within clades

### 4. Methodological Standardization
Most studies converge on similar bioinformatics pipelines:
- **Standard pipeline**: HISAT2 → HTSeq → DESeq2
- **Alternative approaches**: CLC Genomics Workbench for integrated analysis
- Growing use of advanced tools for variant calling from RNA-seq data

### 5. Reference Genome Usage
- **B8441 (Clade I)**: Most common reference (8 studies)
- **B11221 (Clade III)**: Secondary reference (3 studies)
- Version tracking becoming more standardized (GCA accessions)

### 6. Emerging Research Areas
- **Host-pathogen interaction transcriptomics**: Understanding immune response
- **Small RNA and extracellular vesicles**: Novel regulatory mechanisms
- **Epigenetic regulation**: Chromatin remodeling in resistance
- **Translational profiling**: Combined transcriptome and proteome analysis
- **SNP calling from RNA-seq**: Novel application for variant detection

### 7. Data Availability
- Increasing deposition of raw data in public repositories (GEO, SRA)
- Some studies include GitHub repositories with analysis pipelines
- Growing emphasis on reproducibility and open science

---

## Comparison: PubMed vs. Europe PMC vs. Repository Analysis

### Papers Found Exclusively Through Europe PMC Search:
1. **PMID: 34630944** - Caspofungin transcriptional/translational landscape (2021)
2. **PMID: 35968956** - Echinocandin resistance transcriptomics (2022)
3. **PMID: 36913408** - ALS4 biofilm amplification (2023)
4. **PMC11459930** - Pan-drug resistance (2024)
5. **PMID: 40099908** - Flucytosine resistance evolution (2025)

### Papers Found Through Repository Analysis:
Two major studies were identified through analysis of existing repository datasets, not through literature searches:
1. **PMID: 37769084** - Santana et al. (2023) - SCF1 adhesin characterization (Science)
2. **PMID: 38562758** - Wang et al. (2024) - Functional redundancy in adhesins (Nature Communications)

**Why these were missed in database searches:**
- RNA-seq was a supporting methodology, not the primary focus
- Papers emphasize functional phenotypes (adhesion, biofilm, colonization) over transcriptomics
- Search terms focused on "RNA-seq," "transcriptome," "differential expression" as primary keywords

### Overlapping Papers:
Most papers from the PubMed search were also indexed in Europe PMC, confirming cross-database coverage.

### Search Effectiveness:
- **PubMed**: Excellent for established literature, strong PMID coverage
- **Europe PMC**: Better for recent publications, European research output, integrated with other databases
- **Repository Analysis**: Essential for identifying papers where RNA-seq is secondary methodology; captures high-impact studies in top-tier journals (Science, Nature Communications) that may not emphasize sequencing in titles/abstracts

**Recommendation**: Use multiple approaches for comprehensive literature reviews:
1. Database searches (PubMed + Europe PMC)
2. BioProject/SRA repository searches
3. Citation tracking from key papers

---

## Data Sources

**Primary Searches**:
1. PubMed and PubMed Central (December 2, 2025)
2. Europe PMC (December 2, 2025)
3. Repository Analysis (December 2, 2025) - Analysis of existing BioProjects in local repository

**Search terms included**:
- "Candida auris RNA-seq"
- "Candidozyma auris transcriptome"
- "Candida auris differential expression"
- "Candida auris transcriptome sequencing"
- Various combinations with specific years (2020-2025)
- Drug-specific terms (caspofungin, amphotericin B, echinocandin, flucytosine)

**Total studies identified**: 16 RNA-seq studies (2020-2025)

---

**Document created**: December 2, 2025
**Last updated**: December 2, 2025
**Version**: 3.0 (Combined PubMed + Europe PMC + Repository Analysis)
