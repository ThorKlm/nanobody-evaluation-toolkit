# Nanobody Non-Binding Experiments Workflow

## Quick Start

### 1. Get all available SABDAB nanobody entries
Go to
https://opig.stats.ox.ac.uk/webapps/sabdab-sabpred/sabdab/nano/?all=true.
Scroll down the full page until the *Download results* section appears. Download the summary file and copy it into this directory.
### 1. Get Sequences
To get the single letter coded nanobody sequences (as they are not included in the summary file), run the following python command/ script:
```bash
# Download nanobody sequences from SABDAB
python retrieve_single_chain_sequences_drom_SABDAB.py
# Generates: nanobody_sequences.fasta
```

### 2. Create Batches
```bash
# Create batches for web servers
python sample_batching.py nanobody_sequences.fasta -b 25 -o batches_fasta
python sample_batching.py nanobody_sequences.fasta -b 50 -o batches_txt -f txt
```

## Web Server Analysis

### Aggregation & Stability
- **AggreProt**: https://loschmidt.chemi.muni.cz/aggreprot/ (3 seq/batch, FASTA)
- **Aggrescan3D**: https://biocomp.chem.uw.edu.pl/A3D2 (individual structures)
- **NanoMelt**: https://www-cohsoftware.ch.cam.ac.uk/index.php/nanomelt (250 seq/batch, requires account)
- **SolubiS**: https://solubis.switchlab.org/node/add/solubis-job (1 structure/batch, pdb format)

### Naturalness & Localization
- **AbNatiV**: https://www-cohsoftware.ch.cam.ac.uk/index.php/abnativ (1 seq/batch)
- **DeepLoc 2.1**: https://services.healthtech.dtu.dk/services/DeepLoc-2.1/ (250 seq/batch, max 500)

### Local Tools
```bash
# SherLoc2 (Docker-based, 25 seq/batch)
docker build -t sherloc2-image .
docker run -d -p 28030:80 sherloc2-image
# Access: http://localhost:28030/cgi-bin/webloc.cgi
```

## Batch Sizes Summary
```
AggreProt/NanoMelt/SherLoc2: 25 sequences (FASTA)
AbNatiV/SolubiS:            50 sequences 
DeepLoc 2.1:               100 sequences (max 500)
Aggrescan3D:               Individual submission
```

Upload appropriate batches to each server, download results, and organize in `results/` subdirectories by tool name.