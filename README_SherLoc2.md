# SherLoc2 - Subcellular Localization Prediction

## Overview

SherLoc2 is a bioinformatics tool for predicting protein subcellular localizations in eukaryotic cells. This implementation provides a containerized version of SherLoc2 as a web service, making it easier to deploy and use compared to the original standalone installation.

**Original Repository:** https://github.com/KohlbacherLab/SherLoc2

## Features

SherLoc2 combines multiple prediction methods:
- **SVMTarget** - N-terminal targeting sequences (signal peptides, mitochondrial/chloroplast transit peptides)
- **SVMSA** - Signal anchors
- **SVMaac** - Overall amino acid composition
- **MotifSearch** - Sequence motifs (NLS, KDEL, SKL, DNA binding domains)
- **GOLoc** - Gene Ontology terms
- **PhyloLoc** - Phylogenetic profiles (currently bypassed due to compatibility issues)
- **EpiLoc** - Text-based features from PubMed abstracts

## Prerequisites

- Docker installed and running
- At least 4GB of free disk space for the Docker image
- Port 28030 available (or modify the run command)

## Quick Start

1. **Clone this repository and navigate to the SherLoc2 directory:**
   ```bash
   cd nanobody-tools/SherLoc2
   ```

2. **Build the Docker image:**
   ```bash
   docker build --no-cache -t sherloc2-image .
   ```
   Note: The build process takes approximately 10-15 minutes due to genome data setup.

3. **Run the container:**
   ```bash
   docker run -d -p 28030:80 \
     -e SL_CONTACT_EMAIL="your-email@example.com" \
     -e SL_IMPRINT_URL="https://your-imprint-url.com" \
     -e SL_GDPR_URL="https://your-gdpr-url.com" \
     -e SL_MAX_SEQ="25" \
     --name sherloc2_webservice \
     sherloc2-image
   ```

4. **Access the web interface:**
   Open your browser and navigate to: http://localhost:28030/cgi-bin/webloc.cgi

## Usage

1. **Input Format:**
   - Protein sequences in FASTA format
   - Maximum 25 sequences per submission (configurable via SL_MAX_SEQ)
   - Select organism type: Animal, Plant, or Fungal

2. **Output:**
   - Probability scores for each subcellular location
   - Locations include: nucleus, cytoplasm, mitochondria, extracellular, plasma membrane, peroxisome, ER, Golgi, lysosome
   - Plant-specific: chloroplast, vacuole
   - Results can be downloaded as text files

3. **Example sequence:**
   ```
   >test_protein
   MGSNKSKPKDASQRRRSLEPAENVHGAGGGAFPASQTPSKPASADGHRGPSAAFAPAAAE
   PKLFGGFNSSDTVTSPQRAGALAGGVTTFVALYDYESRTETDLSFKKGERLQIVNNTEGD
   ```

## Technical Details

### Docker Image Modifications

The containerized version includes several fixes for compatibility with modern systems:

1. **BLAST Compatibility:** Legacy BLAST commands (`formatdb`, `blastall`) are wrapped to use BLAST+ tools
2. **Temp Directory:** Changed from `/tmp/` to `/sl2jobs/tmp/` to avoid permission issues
3. **Path Fixes:** Corrected double-slash issues in genome paths
4. **PhyloLoc Module:** Currently bypassed due to parsing errors with dummy values (all scores set to 0.111)

### Directory Structure
```
/SherLoc2/          - Main application directory
/sl2jobs/           - Job files and temporary data
/sl2jobs/tmp/       - Temporary files for predictions
/var/www/html/cgi-bin/ - Web interface scripts
```

### Troubleshooting

1. **Container won't start:**
   ```bash
   docker logs sherloc2_webservice
   ```

2. **Check health status:**
   ```bash
   docker exec sherloc2_webservice python /webservice/healthcheck.py
   ```

3. **No results appearing:**
   - Check if job files are created: `docker exec sherloc2_webservice ls -la /sl2jobs/`
   - PhyloLoc module is bypassed - results may be less accurate for evolutionary-based predictions

4. **Port already in use:**
   Change the port mapping: `-p 8080:80` instead of `-p 28030:80`

## Limitations

- PhyloLoc module is currently disabled due to compatibility issues
- Maximum 25 sequences per submission (configurable)
- Genome databases are included in the image, making it quite large (~2GB)
- Some features may show reduced accuracy without PhyloLoc

## Citation

If you use SherLoc2, please cite:

Briesemeister, S.; Blum, T.; Brady, S.; Lam, Y.; Kohlbacher, O. and Shatkay, H. (2009) **SherLoc2: a high-accuracy hybrid method for predicting subcellular localization of proteins.** J. Proteome Res., 8(11):5363-5366

## Maintenance Notes

This containerized version was created as part of the Nanobody Evaluation Toolkit project. The original SherLoc2 codebase has been modified for compatibility with modern systems while preserving the core prediction functionality.

For issues specific to this containerized version, please open an issue in this repository. For questions about the SherLoc2 algorithm itself, refer to the original publication.
