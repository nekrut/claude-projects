# DESeq2 Setup Guide for C. auris SWI1 Knockout Analysis

## Quick Links

**Your Galaxy History:** https://usegalaxy.org/u/cartman/h/prjna904261

**Direct Access:**
1. Go to your history: https://usegalaxy.org/histories/view?id=bbd44e69cb8906b5713a37cc4e6846ea
2. In the Tools panel (left side), search for "DESeq2"
3. Click on "DESeq2" tool

## Study Design (from Paper)

**Comparison:** AR0382_tnSWI1_KO vs AR0382_burn_WT

- **Control (Reference):** AR0382_burn_WT - Wild-type parent strain (strain TO33)
- **Treatment (Test):** AR0382_tnSWI1_KO - SWI1 transposon knockout mutant (strain TO219)

**Expected Key Finding:** SCF1 (gene B9J08_001458) should be the most strongly down-regulated gene in the knockout

## DESeq2 Configuration in Galaxy

### Step 1: Select Input Data Type
- **How:** Select from treatment group and control group
- **Count data:** This is count data (you have count tables)

### Step 2: Treatment Group (Factor Level 1)
- **Factor level name:** `AR0382_tnSWI1_KO`
- **Counts file:** Select **Collection #412** (AR0382_tnSWI1_KO)
  - This contains: AR0382_tnSWI1_A and AR0382_tnSWI1_B

### Step 3: Control Group (Factor Level 2)
- **Factor level name:** `AR0382_burn_WT`
- **Counts file:** Select **Collection #409** (AR0382_burn_WT)
  - This contains: AR0382_A and AR0382_B

### Step 4: Files Have Header?
- **Yes** (your count tables have gene ID headers)

### Step 5: Choose Differential Expression Method
- **Factor:** You can name it `Condition` or `Genotype`
- **First factor level (reference):** AR0382_burn_WT
- **Second factor level (treatment):** AR0382_tnSWI1_KO

### Step 6: Advanced Options (Optional but Recommended)
- **Output normalized counts table:** Yes (useful for visualization)
- **Output rlog transformed data:** No (optional, only if you want to do clustering)
- **Fit type:** Parametric (default, works well for most cases)
- **Outlier replacement:** Yes (default)

### Step 7: Execute
Click "Execute" button

## Expected Outputs

1. **DESeq2 result file** - Main differential expression results with:
   - Gene IDs
   - baseMean (average expression)
   - log2FoldChange (positive = upregulated in knockout, negative = downregulated)
   - lfcSE (standard error)
   - pvalue
   - padj (adjusted p-value)

2. **Normalized counts table** (if selected) - For plotting expression values

3. **DESeq2 plots** - MA plot, dispersion plot, etc.

## What to Look For

According to the paper (Figure 1D):
- **SCF1 (B9J08_001458)** should be the most significantly DOWN-regulated gene
- This means:
  - **Negative log2FoldChange** (lower expression in tnSWI1 knockout)
  - **Very low padj value** (highly significant)
  - Should be at the top when sorting by significance

## Alternative: Simple Interface Method

If the above seems complex, Galaxy also has a "Simple" mode:

1. Tool: DESeq2
2. Select: **Simple factorial design**
3. Factor name: `Genotype`
4. **Level 1:** AR0382_burn_WT → Collection #409
5. **Level 2:** AR0382_tnSWI1_KO → Collection #412
6. Specify which comparison: Level 2 vs Level 1 (knockout vs wild-type)

## Collection Information

For reference, your collections are:

| Collection Name | HID | Collection ID | Samples |
|----------------|-----|---------------|---------|
| AR0382_burn_WT | #409 | cd59c7371096bd0c | AR0382_A, AR0382_B |
| AR0382_tnSWI1_KO | #412 | 5fcc8224c9a714d1 | AR0382_tnSWI1_A, AR0382_tnSWI1_B |

## Interpretation

The comparison `AR0382_tnSWI1_KO vs AR0382_burn_WT` will show:
- **Positive log2FC:** Genes with HIGHER expression in the knockout (upregulated when SWI1 is knocked out)
- **Negative log2FC:** Genes with LOWER expression in the knockout (downregulated when SWI1 is knocked out, likely SWI1-dependent genes)

**SCF1 should have a large negative log2FC** because SWI1 knockout causes reduced SCF1 expression.

## After Analysis

Once DESeq2 completes:
1. Download the results table
2. Sort by padj (adjusted p-value) or log2FoldChange
3. Look for SCF1 (B9J08_001458) at the top of significantly down-regulated genes
4. You can also create an MA plot or volcano plot to visualize the results
