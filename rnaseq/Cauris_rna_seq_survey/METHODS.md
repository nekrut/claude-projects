# Methods: RNA-seq Literature Survey Compilation

## Overview

This document describes the methodology used to create the comprehensive RNA-seq literature survey for *Candida auris* (Candidozyma auris) studies published since 2020.

**Date of search**: December 2, 2025
**Search scope**: Publications from 2020-2025
**Total studies identified**: 16 RNA-seq studies
**Sources**: PubMed/PubMed Central + Europe PMC + Repository Analysis
**AI Assistant**: Claude Sonnet 4.5 (Anthropic)

---

## Search Strategy

### 1. Initial Search Queries

Multiple search queries were executed using web search tools to identify relevant publications:

#### Primary Search Terms:
- `"Candida auris RNA-seq PubMed 2020-2025"`
- `"Candidozyma auris transcriptome sequencing PubMed"`
- `"Candida auris" "RNA sequencing" differential expression`
- `"Candida auris RNA-seq methods genome reference 2020-2025 site:pmc.ncbi.nlm.nih.gov"`

#### Secondary Search Terms:
- `Candida auris transcriptome differential expression 2022 2023 2024`
- `"Candida auris" RNA-seq 2024 PMID`
- `Candida auris biofilm RNA-seq aggregation phenotype 2020 2021 2022`

### 2. Database Sources

The following databases were searched:
- **PubMed** (pubmed.ncbi.nlm.nih.gov)
- **PubMed Central** (pmc.ncbi.nlm.nih.gov) for full-text articles
- **Europe PMC** (europepmc.org) - European biomedical literature database
- **Journal websites** (ASM Journals, Frontiers, Nature Communications, PLOS Pathogens) when full text was accessible

### 3. Europe PMC Search (Secondary Search)

Following the initial PubMed search, a comprehensive search was conducted on Europe PMC to identify additional studies that may have been missed:

#### Europe PMC Search Terms:
- `site:europepmc.org "Candida auris" RNA-seq 2020-2025`
- `site:europepmc.org Candidozyma auris transcriptome sequencing`
- `site:europepmc.org "Candida auris" differential expression RNA sequencing`
- `europepmc.org Candida auris RNA-seq transcriptome 2020 2021 2022`
- `europepmc.org Candida auris transcriptome 2023 2024`
- `"Candida auris" caspofungin transcriptional translational landscape PMID 2021`
- `"Candida auris" RNA-seq biofilm aggregation PMID 2020 2021 2022 2023`
- `"Candida auris" RNA-seq PMID 2024 flucytosine resistance`

#### Additional Papers Identified Through Europe PMC:
1. **PMID: 34630944** - Caspofungin response (transcriptional and translational landscape)
2. **PMID: 35968956** - Echinocandin resistance transcriptomics
3. **PMID: 36913408** - ALS4 gene amplification and biofilm formation
4. **PMC11459930** - Pan-drug resistant strains
5. **PMID: 40099908** - Flucytosine resistance evolution (2025)

#### Rationale for Dual-Database Search:
- **Complementary coverage**: Europe PMC indexes European research outputs and may have different emphasis than PubMed
- **Cross-validation**: Overlap between databases confirms comprehensive coverage
- **Completeness**: Ensures recently published or early online articles are captured
- **Different indexing**: Some articles may be more readily discoverable through Europe PMC's interface

### 4. Repository Analysis (Tertiary Search)

After completing database searches, two additional studies were identified through analysis of BioProject data already present in the local repository:

#### Repository Projects Analyzed:
1. **PRJNA904261** (santana24_PRJNA904261 directory)
   - Santana et al. (2023) - Science
   - SCF1 adhesin characterization
   - PMID: 37769084

2. **PRJNA1086003** (wang24_PRJNA1086003 directory)
   - Wang et al. (2024) - Nature Communications
   - Functional redundancy in cell surface adhesins
   - PMID: 38562758

#### Why These Were Not Found in Database Searches:
- RNA-seq was a **supporting methodology** rather than the primary focus
- Paper titles/abstracts emphasize functional phenotypes:
  - "adhesin," "colonization," "surface association," "virulence"
  - NOT "RNA-seq," "transcriptome," or "differential expression"
- Published in high-impact general science journals (Science, Nature Communications)
- Comprehensive functional studies where transcriptomics was one of multiple methods

#### Discovery Process:
1. Existing analysis reports in repository referenced these BioProjects
2. Papers were retrieved via PubMed ID lookup
3. Full-text methods sections confirmed RNA-seq methodology
4. Technical details extracted from repository analysis reports

#### Implications for Literature Searches:
- **Database keyword searches have limitations** - they miss papers where RNA-seq is secondary
- **Repository-based discovery** is essential for comprehensive coverage
- High-impact functional studies often use RNA-seq without emphasizing it in titles/abstracts
- **BioProject/SRA searches** should complement traditional literature searches

---

## Data Extraction Methodology

### Phase 1: Initial Identification

1. **Web searches** returned lists of potentially relevant publications
2. Each result was evaluated for relevance based on:
   - Organism: *Candida auris* or *Candidozyma auris*
   - Method: RNA-seq, transcriptome sequencing, or transcriptomics
   - Publication date: 2020 or later
   - Study type: Original research articles (not reviews)

### Phase 2: Abstract Screening

For each identified paper:
1. **PubMed ID (PMID)** was recorded
2. **Abstract** was fetched using WebFetch tool
3. Initial assessment determined if RNA-seq methods were used

**Limitation**: Many abstracts did not contain detailed methodological information, requiring full-text access.

### Phase 3: Full-Text Review

For papers passing abstract screening:

1. **Full-text articles** were accessed when available through:
   - PubMed Central (PMC) open access articles
   - Publisher websites with open access
   - Direct DOI links

2. **Methods sections** were specifically targeted to extract:
   - Genome reference version/assembly used
   - Type of RNA-seq analysis performed
   - Complete bioinformatics pipeline/tools used

3. **WebFetch tool** was used with targeted prompts:
   ```
   Extract from the methods section:
   (1) what genome version or reference assembly was used for RNA-seq analysis,
   (2) what type of RNA-seq analysis was performed,
   (3) all tools and software used for RNA-seq analysis including
       quality control, alignment, quantification, and statistical analysis
   ```

### Phase 4: Data Compilation

For each study, the following information was systematically recorded:

1. **PubMed ID and URL**
2. **Publication year**
3. **Genome reference version**
   - Recorded as specified in methods (e.g., "B8441", "B11221", "GCA_002759435")
   - Marked as "N/A" when not specified in accessible text
4. **Type of RNA-seq analysis**
   - Differential expression analysis (most common)
   - De novo transcriptome assembly
   - Small RNA sequencing
   - Host-pathogen transcriptomics
5. **Bioinformatics tools and software**
   - Categorized by function: QC, alignment, quantification, statistical analysis, functional annotation

---

## Information Extraction Challenges and Solutions

### Challenge 1: Incomplete Methods in Abstracts
**Problem**: Most PubMed abstracts lacked detailed methodological information, particularly genome versions and specific tools.

**Solution**:
- Prioritized accessing full-text articles from PubMed Central
- When full text unavailable, marked information as "N/A"
- Did not speculate or infer missing information

### Challenge 2: Access Restrictions
**Problem**: Some journal articles returned 403 errors or required subscriptions.

**Solution**:
- Focused on open-access articles through PMC
- Used alternative open-access versions when available
- Documented when information could not be retrieved

### Challenge 3: Inconsistent Nomenclature
**Problem**: Genome references cited inconsistently across papers:
- "B8441" vs "GCA_002759435" vs "C. auris B8441"
- Version numbers sometimes included (V1, V2), sometimes omitted

**Solution**:
- Recorded genome references exactly as stated in original paper
- Added accession numbers in parentheses when provided
- Cross-referenced with NCBI databases when clarification needed

### Challenge 4: Tool Version Specificity
**Problem**: Some papers specified tool versions (e.g., "HISAT2 v2.1.0"), others did not.

**Solution**:
- Recorded tool names as primary information
- Included versions when explicitly stated in source
- Did not attempt to infer or standardize versions

---

## Quality Control Measures

### 1. Verification of PubMed IDs
- All PMIDs were verified by accessing the PubMed page directly
- URLs were tested to ensure they resolved correctly

### 2. Cross-referencing
- When papers cited genome databases, these were noted
- Common genome references (B8441, B11221) were cross-checked across multiple papers

### 3. Systematic Documentation
- All information was extracted directly from source materials
- No information was assumed or inferred beyond what was explicitly stated
- "N/A" designation used consistently when information was unavailable

---

## Tools and Technologies Used

### AI-Assisted Literature Review
**Claude Sonnet 4.5** (Anthropic) was used with the following capabilities:

1. **WebSearch tool**: Performed systematic searches across PubMed and scientific databases
2. **WebFetch tool**: Retrieved and parsed content from specific URLs (PubMed, PMC, journal websites)
3. **Natural language processing**: Extracted structured information from unstructured text in methods sections
4. **Markdown formatting**: Compiled information into organized tables and documentation

### Search and Retrieval Process
```
User Query → Web Search (multiple queries in parallel)
         ↓
    Result URLs identified
         ↓
    WebFetch full text for each paper
         ↓
    Extract methods information
         ↓
    Structure data in table format
         ↓
    Compile comprehensive document
```

---

## Inclusion and Exclusion Criteria

### Inclusion Criteria:
- ✅ Studies performing RNA-seq on *Candida auris* or *Candidozyma auris*
- ✅ Original research articles
- ✅ Published 2020 or later
- ✅ Any RNA-seq analysis type (differential expression, de novo assembly, small RNA, etc.)
- ✅ Any experimental condition (drug resistance, biofilm, morphotype, etc.)

### Exclusion Criteria:
- ❌ Review articles or meta-analyses
- ❌ Whole genome DNA sequencing without transcriptomics
- ❌ Studies published before 2020
- ❌ Conference abstracts without full publication
- ❌ Studies on other *Candida* species without *C. auris*

---

## Data Organization and Presentation

### Table Structure
The final table includes four columns:
1. **PubMed ID**: Hyperlinked to PubMed page
2. **Genome Version**: Reference assembly used (or "N/A")
3. **Type of RNA-seq**: Analysis approach
4. **Tools Used**: Complete bioinformatics pipeline

### Supplementary Information
Beyond the table, additional context provided:
- Individual study summaries with key findings
- Analysis of trends across studies
- Identification of most commonly used tools and references
- Statistical thresholds commonly employed
- Links to full-text sources when available

---

## Limitations

### 1. Search Comprehensiveness
- Search relied on keyword matching and may have missed studies with non-standard terminology
- Only English-language publications were effectively searched
- Some relevant studies may exist in preprint servers not systematically searched

### 2. Full-Text Access
- Not all papers had freely accessible full text
- Some methods details may have been missed due to access limitations
- Paywalled journals were not accessed

### 3. Time-Bounded Search
- Search conducted on single date (December 2, 2025)
- New publications after this date not included
- Papers "in press" or "early online" may have been missed

### 4. Information Extraction Depth
- Focused on key methodological elements (genome, tools, analysis type)
- Did not extract sample sizes, sequencing depth, or all experimental details
- Some nuanced methodological variations may have been simplified

---

## Reproducibility

To reproduce this literature survey:

1. **Execute search queries** listed above in PubMed and PMC
2. **Screen results** using inclusion/exclusion criteria
3. **Access full-text articles** for papers passing screening
4. **Extract data** systematically from methods sections:
   - Genome reference version
   - RNA-seq analysis type
   - Complete tool list
5. **Compile** into structured table format
6. **Verify** all PubMed IDs and URLs

**Note**: Results may vary if repeated at a different time due to new publications.

---

## Future Improvements

To enhance this survey in future iterations:

1. **Expanded search**: Include preprint servers (bioRxiv, medRxiv)
2. **Systematic review protocol**: Register with PROSPERO or similar
3. **Quality assessment**: Add scoring for methodological rigor
4. **Meta-analysis**: Quantitatively compare outcomes across studies
5. **Regular updates**: Quarterly or annual refresh of search
6. **Citation tracking**: Forward and backward citation searching
7. **Contact authors**: Request clarification on missing methodological details

---

## Summary Statistics

### Search Coverage
**Total searches performed**: 15+ distinct search queries across two databases plus repository analysis
**Papers identified in PubMed search**: ~20+ candidate papers
**Papers identified in Europe PMC search**: ~15+ candidate papers (5 new papers not in PubMed results)
**Papers identified through repository analysis**: 2 high-impact papers
**Papers with full-text access**: 16 papers
**Papers included in final table**: 16 papers (2020-2025)

### Source Breakdown
**PubMed/PubMed Central**: 9 papers
**Europe PMC (exclusive)**: 5 papers
**Repository Analysis (exclusive)**: 2 papers
**Total unique papers**: 16 papers

### Research Characteristics
**Geographic distribution**: China, USA, Europe, India, Middle East
**Date range**: 2020-2025 (one paper published January 2025)
**Most common clade studied**: Clade I (B8441) and Clade III (B11221)
**Primary research focus**: Antifungal drug resistance (>50% of studies)

---

## Contact and Updates

This methods document describes the process as of December 2, 2025. For questions about methodology or to suggest additional papers for inclusion, please refer to the git repository history and commit messages.

**Repository**: claude-projects
**Directory**: rnaseq/Cauris_rna_seq_survey/
**Last updated**: December 2, 2025
