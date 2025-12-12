# DESeq2 Reanalysis Validation

Validate DESeq2 reanalysis results against published data using LFC-based gene matching.

## Problem

Different genome annotation versions produce different gene IDs, preventing direct comparison between your reanalysis and published results.

## Solution

Genes with identical expression produce identical log2 fold changes. This notebook matches genes by LFC correlation—annotation-agnostic.

## Usage

1. **Prepare publication data** using an LLM (see notebook instructions)
2. **Configure** `DESEQ2_FILE` and `PUBLICATION_FILE` paths
3. **Run all cells**
4. **Review** R², direction agreement, Bland-Altman plot

## Inputs

| File | Format | Required Columns |
|------|--------|------------------|
| DESeq2 output | TSV | Gene_ID, log2FoldChange, padj |
| Publication data | CSV | gene_id, log2fc |

## Outputs

- `gene_mapping.csv` - matched gene pairs with LFC values
- `validation.html` - interactive scatter + Bland-Altman plot
- Console metrics: R², Spearman r, direction agreement

## Features

- Auto-detects reversed comparison direction
- Interactive Altair plots with gene tooltips
- Optional significance/LFC filtering
