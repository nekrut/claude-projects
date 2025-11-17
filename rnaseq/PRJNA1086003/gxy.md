## Links to get context from

https://bioblend.readthedocs.io/en/latest/
https://usegalaxy.org/api/docs
https://training.galaxyproject.org/training-material/topics/galaxy-interface/tutorials/group-tags/tutorial.html

## Galaxy artifacts:

- Galaxy API-key: YOUR_GALAXY_API_KEY
- Galaxy instance: https://usegalaxy.org
- https://usegalaxy.org/u/cartman/h/prjna1086003

## Collections:

- **Original collection** (#601): Counts Table (13 samples - all samples)
- **In vitro collection** (#621): PRJNA1086003_in_vitro (6 samples from in vitro biofilm experiment)
  - All datasets tagged with group tags (e.g., group:82_Bio_1, group:87_Bio_1, etc.)
  - Sub-collections created:
    - #641: PRJNA1086003_in_vitro_AR0382 (3 samples)
    - #645: PRJNA1086003_in_vitro_AR0387 (3 samples)
- **In vivo collection** (#629): PRJNA1086003_in_vivo (7 samples from in vivo catheter experiment)
  - All datasets tagged with group tags (e.g., group:82_RNA_inVivo_blueink, group:87-1, etc.)
  - Sub-collections created:
    - #651: PRJNA1086003_in_vivo_AR0382 (3 samples)
    - #656: PRJNA1086003_in_vivo_AR0387 (4 samples)

## DESeq2 Analyses:

### ✓ CORRECT Method (Latest Run)

**In vitro experiment (strain 82 vs 87):**
- Factor level "87" (AR0387, non-aggregative, n=3): Collection #645
- Factor level "82" (AR0382, aggregative, n=3): Collection #641
- Expected ~76 DEGs (LFC ≥ |1|, FDR < 0.01) based on paper
- Results: Check latest DESeq2 outputs in history

**In vivo experiment (strain 82 vs 87):**
- Factor level "87" (AR0387, non-aggregative, n=4): Collection #656
- Factor level "82" (AR0382, aggregative, n=3): Collection #651
- Expected ~259 DEGs (LFC ≥ |1|, FDR < 0.01) based on paper
- Results: Check latest DESeq2 outputs in history

**Method:** Each factor level (strain) gets its own collection fed to DESeq2

