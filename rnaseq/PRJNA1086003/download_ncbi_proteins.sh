#!/bin/bash
# Download protein sequences from NCBI for both annotation versions

echo "Downloading protein sequences from NCBI..."

# v2: GCA_002759435.2
echo "Downloading v2 annotation (GCA_002759435.2)..."
wget -O GCA_002759435.2_protein.faa.gz \
  "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/759/435/GCA_002759435.2_Cand_auris_B8441_V2/GCA_002759435.2_Cand_auris_B8441_V2_protein.faa.gz"

# v3: GCA_002759435.3
echo "Downloading v3 annotation (GCA_002759435.3)..."
wget -O GCA_002759435.3_protein.faa.gz \
  "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/002/759/435/GCA_002759435.3_Cand_auris_B8441_V3/GCA_002759435.3_Cand_auris_B8441_V3_protein.faa.gz"

# Decompress
echo "Decompressing..."
gunzip -f GCA_002759435.2_protein.faa.gz
gunzip -f GCA_002759435.3_protein.faa.gz

echo "✓ Download complete!"
echo "  - GCA_002759435.2_protein.faa"
echo "  - GCA_002759435.3_protein.faa"
