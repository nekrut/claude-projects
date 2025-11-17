# How to Continue This Work at Home

## ✅ What's Already Saved

All your work has been committed and pushed to GitHub:
- Repository: `git@github.com:nekrut/claude-projects.git`
- Branch: `main`
- Commit: `c00c608` - "Add PRJNA1086003 DESeq2 differential expression analysis"

## 🏠 To Continue at Home

### Step 1: Clone or Pull the Repository

If you don't have the repository at home yet:
```bash
git clone git@github.com:nekrut/claude-projects.git
cd claude-projects/rnaseq/PRJNA1086003
```

If you already have it:
```bash
cd /path/to/claude-projects
git pull origin main
cd rnaseq/PRJNA1086003
```

### Step 2: Review the Work

All important information is documented in these files:

1. **SUMMARY.md** - Complete overview of everything we did
2. **DESEQ2_ANALYSIS.md** - Detailed methodology and expected results
3. **gxy.md** - Galaxy artifacts, collections, and analyses info
4. **samples_in_vitro.tsv** / **samples_in_vivo.tsv** - Sample metadata

### Step 3: Check DESeq2 Results in Galaxy

The DESeq2 jobs are running in your Galaxy history:
- URL: https://usegalaxy.org/u/cartman/h/prjna1086003
- Galaxy API key: YOUR_GALAXY_API_KEY (stored in gxy.md)

Look for the most recent DESeq2 outputs:
- "DESeq2 result file" - Contains the differential expression statistics
- "DESeq2 plots" - Diagnostic plots

### Step 4: Scripts You Can Run

**To check DESeq2 job status:**
```bash
python3 check_deseq2_results.py
```

**To rerun DESeq2 if needed:**
```bash
python3 run_deseq2_proper.py
```

All scripts require `bioblend` library:
```bash
pip install bioblend
```

### Step 5: Analyze Results

Once DESeq2 jobs complete:

1. Download the result files from Galaxy
2. Filter for significant genes:
   - |log2FoldChange| ≥ 1
   - padj (adjusted p-value) < 0.01

3. Compare with paper expectations:
   - In vitro: ~76 DEGs
   - In vivo: ~259 DEGs

4. Look for key adhesin genes:
   - SCF1 (B9J08_001458)
   - ALS4112 (B9J08_004112)
   - IFF4109 (B9J08_004109)

## 📋 What We Accomplished

1. ✅ Split samples into in vitro and in vivo experiments
2. ✅ Created Galaxy collections (#621, #629)
3. ✅ Added group tags to all 13 datasets
4. ✅ Created strain-specific sub-collections (#641, #645, #651, #656)
5. ✅ Ran DESeq2 comparing AR0382 vs AR0387 for both experiments

## 🔑 Key Files

```
PRJNA1086003/
├── SUMMARY.md                      # Start here!
├── DESEQ2_ANALYSIS.md             # Detailed methodology
├── gxy.md                         # Galaxy info
├── samples_in_vitro.tsv           # In vitro samples
├── samples_in_vivo.tsv            # In vivo samples
├── run_deseq2_proper.py           # Final working script
├── split_collection.py            # Split original collection
├── add_tags_to_collections.py     # Added group tags
└── [papers and supplementary]     # Reference materials
```

## 💡 Tips

- The conversation context is saved in all the markdown files
- Galaxy history is accessible from any location with the API key
- All scripts are documented and ready to run
- The git repository tracks all changes

## 🆘 If You Need Help

Start a new Claude Code session at home and say:

> "I'm continuing work on PRJNA1086003 DESeq2 analysis.
> Please read SUMMARY.md to understand what's been done."

Claude Code will read the summary and help you continue!
