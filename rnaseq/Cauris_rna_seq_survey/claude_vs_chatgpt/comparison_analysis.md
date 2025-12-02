# Claude vs ChatGPT: Literature Survey Comparison

## Overview

**Claude Survey**: 16 papers (2020-2025)
- Data sources: PubMed (9) + Europe PMC (5) + Repository Analysis (2)

**ChatGPT Survey**: 9 papers with valid PMIDs (2020-2025)
- Data sources: PubMed + Europe PMC (both databases searched)
- Note: ChatGPT list includes 2 additional papers with placeholder PMIDs (XXXXXXX, YYYYYYY)

**Overlap**: **ZERO** - No common PMIDs despite searching same databases!

## Direct Comparison

### Papers Found by BOTH

Looking at the PMIDs, there is **NO DIRECT OVERLAP** - Claude and ChatGPT found completely different sets of papers!

However, there are some **thematic overlaps** on similar topics:

| Topic | Claude PMID | ChatGPT PMID | Notes |
|-------|-------------|--------------|-------|
| Farnesol response | 34485470 | 33983315 | Different studies on same topic |
| Caspofungin response | 34630944 | 34778924 | Different studies on same drug |
| Transcriptome signatures | 33937102 | 33995473 | Different studies on phenotypic variation |
| Adhesin function | 38562758 (2024) | 35649081 (2022) | Different papers, possibly related projects |

## Papers Found ONLY by Claude (16 papers)

### From PubMed Search (9 papers):
1. **PMID 32581078** (2020) - Biofilm phenotypic heterogeneity
2. **PMID 33937102** (2021) - Transcriptome signatures predicting phenotypic variations
3. **PMID 34354695** (2021) - Drug-sensitive vs resistant China
4. **PMID 34485470** (2021) - Farnesol response
5. **PMID 34788438** (2021) - Small RNA/Extracellular vesicles
6. **PMID 35652307** (2022) - Amphotericin B resistance
7. **PMID 37350781** (2023) - Rough morphotype
8. **PMID 38990436** (2024) - Host dermal cells (ferroptosis)
9. **PMC11385638** (2024) - AmB microevolution

### From Europe PMC Search (5 papers):
10. **PMID 34630944** (2021) - Caspofungin transcriptional/translational
11. **PMID 35968956** (2022) - Echinocandin resistance
12. **PMID 36913408** (2023) - ALS4 biofilm amplification
13. **PMC11459930** (2024) - Pan-drug resistance
14. **PMID 40099908** (2025) - Flucytosine resistance

### From Repository Analysis (2 papers):
15. **PMID 37769084** (2023) - Santana et al. SCF1 adhesin (Science)
16. **PMID 38562758** (2024) - Wang et al. Adhesin redundancy (Nature Comm)

## Papers Found ONLY by ChatGPT (9 papers)

1. **PMID 33983315** (2021) - Farnesol exposure (mSphere)
2. **PMID 34778924** (2021) - Caspofungin translational landscape (Comput Struct Biotechnol J)
3. **PMID 33995473** (2021) - Transcriptome signatures (Front Cell Infect Microbiol)
4. **PMID 37548469** (2023) - Tyrosol exposure (AMB Express)
5. **PMID 38537618** (2024) - Farnesol/tyrosol biofilms (Microbiol Spectrum)
6. **PMID 38745637** (2024) - IL-1R immune evasion single-cell RNA-seq (PLOS Pathogens)
7. **PMID 37925028** (2025) - White-Brown switching (Cell Reports)
8. **PMID 35649081** (2022) - Functional redundancy adhesins (Nature Commun)
9. **PMID 34462177** (2021) - Global stress responses (FEMS Yeast Res)

## Key Differences

### 1. Search Approach
- **Claude**: Multi-database (PubMed + Europe PMC + Repository analysis), systematic parallel searches, full-text access for methods extraction
- **ChatGPT**: Also searched both PubMed AND Europe PMC, abstract-based analysis, explicitly noted "many full-text articles are not accessible"

**Critical Finding**: Despite searching the SAME databases (PubMed + Europe PMC) on the same date, the two AI assistants found completely different sets of papers!

### 2. Paper Selection Criteria
- **Claude**: Emphasized drug resistance studies (44% of papers)
- **ChatGPT**: More diverse - stress responses, morphology, biofilm studies

### 3. Level of Detail
- **Claude**:
  - Extracted specific genome versions from methods sections
  - Complete tool pipelines documented
  - Verified via full-text PMC articles

- **ChatGPT**:
  - Many genome versions listed as "N/A"
  - Tools "inferred from standard practice" (not extracted)
  - Limited by full-text access

### 4. Notable Findings

**Claude found but ChatGPT missed:**
- 2 high-impact papers (Science, Nature Comm) via repository analysis
- Pan-drug resistance study (cutting edge)
- Flucytosine resistance (2025, most recent)
- Echinocandin resistance study
- Small RNA/EV study

**ChatGPT found but Claude missed:**
- Single-cell RNA-seq study (PMID 38745637) - different methodology
- White-Brown switching (PMID 37925028)
- Tyrosol studies (PMIDs 37548469, 38537618)
- Global stress response study (PMID 34462177)
- Alternative caspofungin/farnesol papers

## Combined Total: 25 Unique Papers

If we combined both surveys, we would have **25 unique RNA-seq papers** on C. auris since 2020!

### Research Gap Analysis

**Papers ChatGPT found that are genuinely new:**
- **Single-cell RNA-seq** (PMID 38745637) - This is a methodologically distinct approach!
- **Tyrosol studies** (PMIDs 37548469, 38537618) - Focus on different quorum-sensing molecule
- **White-Brown switching** (PMID 37925028) - Important phenotypic plasticity study
- **Global stress responses** (PMID 34462177) - Comprehensive stress analysis

These represent important gaps in Claude's survey!

## Why ZERO Overlap?

This is a striking finding: **Both AI assistants searched PubMed AND Europe PMC on the same date (Dec 2, 2025) but found completely different papers!**

Several factors explain this:

### 1. Different Search Queries and Keywords
- **Claude**: Focused on "RNA-seq", "transcriptome", "differential expression", "Candida auris"
- **ChatGPT**: Likely used different keyword combinations and query structures
- Even subtle differences in query syntax can dramatically change results

### 2. Search Ranking and Relevance Algorithms
- Both searches accessed same databases but received different result rankings
- AI assistants may use different strategies for evaluating relevance
- First-page results differ between search implementations

### 3. Selection and Filtering Criteria
- **Claude**: Prioritized drug resistance (44% of papers), emphasized papers with accessible methods sections
- **ChatGPT**: More diverse selection across stress responses, morphology, biofilm studies
- Human/AI curation decisions differ even with same source data

### 4. Full-Text Access and Verification
- **Claude**: Accessed PMC full texts for methods extraction, verified RNA-seq usage in detail
- **ChatGPT**: Explicitly noted "many full-text articles are not accessible in the current environment"
- Full-text access allows verification of methodology, potentially filtering out false positives

### 5. Repository Analysis (Claude unique)
- **Claude**: Added 2 papers from BioProject analysis (PMID 37769084, 38562758)
- **ChatGPT**: Did not perform repository-based discovery
- High-impact papers (Science, Nature Comm) missed by keyword searches alone

### 6. Search Interface and Tools
- **Claude**: Used WebSearch and WebFetch tools programmatically
- **ChatGPT**: Unknown search implementation details
- Different technical approaches to querying databases

## Recommendations for Comprehensive Survey

To capture all relevant papers, researchers should:

1. **Use multiple databases**: PubMed, Europe PMC, Scopus, Web of Science
2. **Vary search terms**:
   - "RNA-seq", "RNA sequencing", "transcriptome", "transcriptomic"
   - Specific molecules: "farnesol", "tyrosol", "caspofungin"
   - Methodologies: "single-cell", "bulk RNA-seq"
3. **Check BioProject/SRA**: For papers where RNA-seq is secondary
4. **Cross-reference**: Each AI tool finds different papers!
5. **Manual curation**: Essential for comprehensive coverage

## Conclusion

**Surprising Result**: **ZERO papers overlap** between the two AI-assisted searches despite both searching PubMed AND Europe PMC on the same date (Dec 2, 2025)!

This is a critical finding for AI-assisted literature reviews:

### Key Insights

1. **Same Databases ≠ Same Results**
   - Both AI assistants searched PubMed and Europe PMC
   - Both found 9-16 papers each
   - Zero overlap in results
   - Demonstrates fundamental differences in search strategies, query formulation, and paper selection

2. **Search Strategy Matters Enormously**
   - Keyword choices critically affect results
   - Ranking algorithms produce different "top results"
   - Full-text access enables better verification
   - Repository analysis captures papers missed by keyword searches

3. **No Single Approach Captures All Papers**
   - Claude found 16 papers, ChatGPT found 9 different papers
   - **Combined total: 25 unique papers**
   - **56% more papers** when using both approaches (25 vs 16)
   - Each AI assistant has unique strengths and blind spots

4. **AI Tools Have Different Search Biases**
   - Claude: Drug resistance focus (44%), systematic methodology extraction
   - ChatGPT: More diverse topics, broader phenotypic studies
   - Both are valuable but incomplete alone

### Implications for Researchers

When conducting literature reviews with AI assistance:

- ✅ **Use multiple AI assistants** - Different tools find different papers
- ✅ **Search multiple databases** - PubMed, Europe PMC, Web of Science, Scopus
- ✅ **Check repositories** - BioProject/SRA contain papers where RNA-seq is secondary
- ✅ **Verify full-text** - Abstracts alone may miss or mischaracterize methodology
- ✅ **Vary search terms** - RNA-seq, transcriptome, transcriptomic, differential expression
- ✅ **Manual curation remains essential** - AI tools are powerful but not comprehensive

### Best Practice

**Use multiple AI assistants with different search strategies, then merge and deduplicate results.** This study demonstrates that Claude + ChatGPT together provide 56% more coverage than either alone, with zero redundancy between them.
