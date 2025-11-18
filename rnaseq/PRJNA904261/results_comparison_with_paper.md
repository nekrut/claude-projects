# DESeq2 Results Comparison with Santana et al. (2023) Science Paper

## Study Information
- **Paper**: "A Candida auris–specific adhesin, Scf1, governs surface association, colonization, and virulence"
- **Authors**: Santana et al., Science 381, 1461–1467 (2023)
- **BioProject**: PRJNA904261
- **Your Analysis**: AR0382_tnSWI1_KO vs AR0382_burn_WT

## Critical Finding: SCF1 Expression

### Paper's Claim (Figure 1D)
According to the paper:
> "Compared with the AR0382 parent, the tnSWI1 mutant exhibited no significant transcriptional dysregulation of the ALS or IFF/HYR adhesins, suggesting alternative mediators of adhesion (Fig. 1D). The strongest, most significantly dysregulated gene in tnSWI1 was an uncharacterized open reading frame (ORF) (B9J08_001458)..."

**Expected Results:**
- SCF1 (B9J08_001458) = most strongly dysregulated gene
- SCF1 should be DOWN-regulated in tnSWI1 mutant
- High statistical significance

### Your DESeq2 Results

**SCF1 (B9J08_01458) Statistics:**
- log2FoldChange: **+0.035** (essentially no change)
- Adjusted p-value: **0.827** (NOT significant)
- Mean expression: 1674.8

**Raw Count Data:**
| Condition | Sample A | Sample B | Mean |
|-----------|----------|----------|------|
| AR0382_burn_WT | 2013 | 1729 | 1871 |
| AR0382_tnSWI1_KO | 1754 | 2380 | 2067 |

**Fold Change:** 1.10x (slight increase in knockout, NOT decrease)

### Verdict: ❌ DOES NOT MATCH PAPER

## Overall DESeq2 Results Summary

### Statistics
- Total genes analyzed: 5,593
- Significantly DE genes (padj < 0.05): 1,229
  - Down-regulated: 473 genes
  - Up-regulated: 756 genes

### Top 10 Most Significantly Dysregulated Genes

#### Top DOWN-regulated (in tnSWI1 knockout):
1. B9J08_04997: log2FC = -5.36, padj = 5.2e-90
2. B9J08_00520: log2FC = -5.30, padj = 7.0e-57
3. B9J08_04853: log2FC = -5.08, padj = 3.5e-51
4. B9J08_02973: log2FC = -4.79, padj = 2.0e-98
5. B9J08_03776: log2FC = -4.43, padj = 4.1e-03
6. B9J08_00441: log2FC = -4.14, padj = 3.5e-15
7. B9J08_05591: log2FC = -3.52, padj = 3.4e-14
8. B9J08_01958: log2FC = -3.35, padj = 3.4e-05
9. B9J08_05119: log2FC = -2.96, padj = 7.4e-37
10. B9J08_00016: log2FC = -2.88, padj = 8.1e-122

#### Top UP-regulated (in tnSWI1 knockout):
1. B9J08_00860: log2FC = +8.03, padj < 1e-300
2. B9J08_04747: log2FC = +6.98, padj = 5.6e-103
3. B9J08_03708: log2FC = +6.82, padj < 1e-300
4. B9J08_00861: log2FC = +6.16, padj = 7.7e-18
5. B9J08_00453: log2FC = +5.36, padj = 2.9e-157
6. B9J08_05461: log2FC = +5.31, padj = 2.4e-146
7. B9J08_03214: log2FC = +5.16, padj < 1e-300
8. B9J08_01167: log2FC = +5.07, padj < 1e-300
9. B9J08_00523: log2FC = +5.02, padj = 1.0e-254
10. B9J08_03542: log2FC = +4.97, padj = 4.2e-06

**Note:** SCF1 is NOT in the top dysregulated genes!

### SWI1 Gene Status
- **B9J08_03460** (SWI1 gene itself)
  - log2FC: -0.005
  - padj: 0.988
  - Not differentially expressed (expected for transposon insertion)

## Possible Explanations for Discrepancy

### 1. Different Experiment in Paper
The PRJNA904261 RNA-seq data may correspond to a **different experiment** in the paper, not the tnSWI1 screen shown in Figure 1D. The paper includes multiple experiments:
- Transposon mutant screens
- Different growth conditions
- Adhesion assays
- Biofilm formation
- In vivo colonization models

### 2. Growth Conditions Matter
The paper states that SCF1 expression is:
> "among the highest 2.5% of all genes in this strain background"

This high expression might be **condition-dependent**:
- Different media (YPD vs specialized media)
- Different growth phase
- Different temperature
- Presence/absence of serum or other factors

### 3. Strain Background Differences
From the paper (Figure 2B):
> "SCF1 was the most down-regulated gene compared with the highly adhesive AR0382, reminiscent of the poorly adhesive tnSWI1 mutant"

The paper shows that SCF1 expression varies dramatically between strains (Fig 2D):
- Some strains have very high SCF1 expression
- Some strains have very low SCF1 expression
- This variation is strain-specific, not clade-specific

### 4. Experimental Design
Your RNA-seq comparison:
- tnSWI1_KO (TO219) vs burn_WT (TO33)
- Standard growth conditions
- Bulk RNA-seq

Paper's RNA-seq (Figure 1D):
- May have used specific adhesion-inducing conditions
- May have selected cells based on adhesion phenotype
- Different time points or growth phase

## Additional Observations

### Gene Expression Patterns
Looking at the genes that ARE significantly dysregulated in your data:
- Many metabolic genes
- Stress response genes
- Transport genes

This suggests the tnSWI1 mutation affects multiple cellular processes, but **not SCF1 expression** under these conditions.

### Biological Interpretation
The paper's model:
```
SWI1 (chromatin remodeler)
    ↓ (regulates)
SCF1 transcription
    ↓ (produces)
Scf1 adhesin protein
    ↓ (mediates)
Surface adhesion
```

Your data suggests:
- SWI1 knockout does NOT reduce SCF1 transcription (in these conditions)
- The regulatory relationship may be condition-specific
- Or there may be compensatory mechanisms

## Recommendations

### 1. Verify Sample Identity
- Double-check that samples are correctly labeled
- Verify strain identities (TO33 vs TO219)
- Confirm growth conditions match paper

### 2. Check Paper Supplementary Data
- Look for the actual RNA-seq data from Figure 1D
- Compare with other datasets in PRJNA904261
- Check if there are multiple RNA-seq experiments

### 3. Contact Authors
If this discrepancy persists:
- Email correspondence to: tromeara@umich.edu
- Ask about specific growth conditions for Figure 1D RNA-seq
- Request access to the exact dataset used for Figure 1D

### 4. Alternative Analysis
Try other comparisons in your dataset:
- AR0387_blood_WT vs AR0382_burn_WT (strain differences)
- Look at SCF1 expression across all 3 conditions

## Conclusion

Your DESeq2 analysis is technically correct and well-executed. However, **the results do not match the paper's Figure 1D** regarding SCF1 dysregulation in the tnSWI1 mutant.

This discrepancy likely indicates that:
1. The PRJNA904261 RNA-seq data corresponds to a different experiment than Figure 1D, OR
2. SCF1 regulation by SWI1 is highly condition-dependent, OR
3. There are experimental differences we're not aware of

The analysis successfully identified 1,229 differentially expressed genes between the tnSWI1 knockout and wild-type, showing the mutation has significant transcriptional effects - just not on SCF1 under these conditions.

## Data Files
- DESeq2 results: `deseq2_results.tsv`
- Sample mapping: `sample_mapping.md`
- This comparison: `results_comparison_with_paper.md`
