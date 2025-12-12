# AI Can Make Mistakes: no sh&t!

*December 2024*

## TL;DR

While reanalyzing *Candida auris* RNA-seq data, Claude (the AI) devised a "clever" method to map gene IDs between annotation versions using log2 fold change (LFC) similarity. The result: R² = 0.9996—nearly perfect correlation. The problem: only 1% of gene mappings were actually correct. This post documents how we discovered the error and fixed it.

---

## The Setup

We were reanalyzing published RNA-seq datasets from two *C. auris* studies:

- **Santana et al. (2024)**: SCF1 adhesin characterization
- **Wang et al. (2024)**: Glycan-lectin interactions in aggregative strains

Both studies used genome annotation version GCA_002759435.2 (v2), but our Galaxy pipeline used the current version GCA_002759435.3 (v3). The problem: gene IDs changed between versions.

```
v2: B9J08_001458 (6-digit suffix)
v3: B9J08_03708  (5-digit suffix)
```

To validate our DESeq2 results against the publications, we needed to map v2 gene IDs to v3.

## Claude's "Clever" Solution

Without access to an official gene ID mapping, Claude proposed matching genes by their expression values. The logic seemed "scientific":

> "The same gene should have the same log2 fold change in both analyses. Match each paper gene to the gene in our results with the closest LFC."

```python
# The algorithm that seemed brilliant
for paper_gene in paper_degs:
    best_match = min(
        our_genes,
        key=lambda g: abs(paper_lfc[paper_gene] - our_lfc[g])
    )
    mapping[paper_gene] = best_match
```

The result was spectacular: **R² = 0.9996**. Nearly perfect correlation between paper LFC values and our values. Validation complete!

## Hmmm ...

Something nagged. R² = 0.9996 is *suspiciously* good for biological data. Real RNA-seq comparisons between labs show R² ~ 0.85-0.95 due to:

- Batch effects
- Different normalization methods
- Read mapping differences
- Annotation version differences

Yet our "clever hack" outperformed what should be achievable? That's a red flag.

## The Discovery

We found the official NCBI gene ID mapping buried in the v3 GTF file. The `old_locus_tag` attribute explicitly records the correspondence:

```
gene_id "B9J08_03708"; old_locus_tag "B9J08_001458";
```

Cross-referencing our LFC-based mapping against this ground truth:

| Metric | Value |
|--------|-------|
| LFC-matched pairs | 203 |
| Correct matches | 2 |
| **Accuracy** | **1.0%** |

**Our "perfect" R² = 0.9996 mapping was 99% wrong.**

## Why LFC Matching Fails

The failure mode is obvious in hindsight. Consider the math:

1. Both datasets come from the same RNA samples
2. DESeq2 produces similar LFC distributions regardless of annotation version
3. With ~5,500 genes and ~200 DEGs, the probability of finding *some* gene with a similar LFC is high
4. Nearest-neighbor matching optimizes for correlation *by design*

The algorithm didn't find corresponding genes. It found genes with coincidentally similar fold changes—completely unrelated sequences that happened to change expression by similar amounts.

It's like matching people by height and concluding you found twins. Sure, you'll get height correlation, but they're not the same people.

## The Correct Approach

Using the official NCBI `old_locus_tag` mapping:

| Metric | LFC Method | Official Method |
|--------|------------|-----------------|
| R² | 0.9996 | 0.9397 |
| Correct genes | 1% | 100% |

The "worse" R² (0.94) reflects real biological variation—normalization differences, annotation changes, mapping ambiguities. That's what correct validation looks like.

We further validated the NCBI mapping by comparing protein sequences:

| Comparison | Pairs | Exact Protein Match |
|------------|-------|---------------------|
| Santana - tnSWI1 | 167 | 100% |
| Santana - AR0387 | 140 | 100% |
| Wang - In Vitro | 68 | 100% |
| Wang - In Vivo | 229 | 100% |

Every mapped gene encodes the identical protein. The mapping is correct.

## The Corrected Results

With proper gene ID mapping, our validation shows strong reproducibility:

| Study | Comparison | R² | Direction Agreement |
|-------|------------|-----|---------------------|
| Santana | AR0382 vs tnSWI1 | 0.94 | 99% |
| Santana | AR0382 vs AR0387 | 0.89 | 97% |
| Wang | In Vitro | 0.98 | 100% |
| Wang | In Vivo | 0.9998 | 100% |

The key finding—SCF1 as the primary adhesin differentiating *C. auris* strains—is fully validated.

---

## Technical Appendix

### Extracting NCBI Gene ID Mapping

```python
import re

v2_to_v3 = {}
with open('GCA_002759435.3_genomic.gtf') as f:
    for line in f:
        if '\tgene\t' in line:
            gene_id = re.search(r'gene_id "([^"]+)"', line)
            old_tag = re.search(r'old_locus_tag "([^"]+)"', line)
            if gene_id and old_tag:
                v2_to_v3[old_tag.group(1)] = gene_id.group(1)
```

### Protein Sequence Validation

```python
def validate_mapping(v2_gene, v3_gene, v2_fasta, v3_fasta):
    v2_seq = v2_fasta.get(v2_gene)
    v3_seq = v3_fasta.get(v3_gene)
    if v2_seq and v3_seq:
        return v2_seq == v3_seq  # Exact match
    return None  # Missing sequence
```

### Files

- Analysis reports: `santana24_PRJNA904261/ANALYSIS_REPORT.md`, `wang24_PRJNA1086003/ANALYSIS_REPORT.md`
- Validation data: `analysis/validated/protein_comparison_*.csv`
- Deprecated LFC mapping: `analysis/deprecated/gene_mapping_by_lfc.csv`
