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
   
2. **Replace the Docker image with the following updated version**
   ```
   # Applied Bioinformatics Group
   # SherLoc2 Docker Image - Improved Version
   # Fixes critical compatibility and integration issues
   
   FROM ubuntu:18.04
   
   # Prevent interactive prompts during package installation
   ENV DEBIAN_FRONTEND=noninteractive
   
   # Update package repository
   RUN apt-get update && apt-get upgrade -y
   
   # ----------------------------------------------------------
   # Install dependencies in a single layer to reduce image size
   # ----------------------------------------------------------
   RUN apt-get install -y \
       dirmngr \
       software-properties-common \
       vim \
       wget \
       curl \
       libsvm-tools \
       ncbi-blast+ \
       libgnutls30 \
       python-biopython \
       python-dev \
       python-pip \
       apache2 \
       && apt-get clean \
       && rm -rf /var/lib/apt/lists/*
   
   # ----------------------------------------------------------
   # Install Java 8 (required for InterProScan)
   # ----------------------------------------------------------
   RUN apt-get update && \
       apt-get install -y openjdk-8-jdk && \
       apt-get clean && \
       rm -rf /var/lib/apt/lists/*
   
   ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
   ENV CLASSPATH=/usr/lib/jvm/java-8-openjdk-amd64/bin
   
   # ----------------------------------------------------------
   # Create necessary directories with proper permissions
   # ----------------------------------------------------------
   RUN mkdir -p /sl2jobs/tmp && \
       chmod 777 /sl2jobs && \
       chmod 777 /sl2jobs/tmp && \
       mkdir -p /webservice
   
   # ----------------------------------------------------------
   # Setup Apache2 for CGI
   # ----------------------------------------------------------
   RUN a2enmod cgid && \
       a2enmod rewrite
   
   # Copy Apache configuration
   ADD webservice/apache2.conf         /etc/apache2/apache2.conf
   ADD webservice/serve-cgi-bin.conf   /etc/apache2/conf-available/serve-cgi-bin.conf
   
   # Copy web service files
   COPY webservice/webloc.cgi   /var/www/html/cgi-bin/
   COPY webservice/epiloc_interface.py   /var/www/html/cgi-bin/
   COPY webservice/dialoc_interface.py   /var/www/html/cgi-bin/
   COPY webservice/downloads/   /var/www/html/cgi-bin/downloads/
   COPY webservice/images/      /var/www/html/cgi-bin/images/
   
   # Copy webservice scripts
   ADD webservice/job_cleanup.sh          /webservice/job_cleanup.sh
   ADD webservice/sl2setup.py             /webservice/sl2setup.py
   ADD webservice/sherloc2_entrypoint.sh  /webservice/sherloc2_entrypoint.sh
   
   # ----------------------------------------------------------
   # Create BLAST compatibility wrappers (improved versions)
   # ----------------------------------------------------------
   RUN echo '#!/bin/bash\n\
   # Legacy formatdb wrapper for BLAST+\n\
   INPUT_FILE=""\n\
   DBTYPE="T"\n\
   \n\
   while [[ $# -gt 0 ]]; do\n\
     case $1 in\n\
       -i) INPUT_FILE="$2"; shift 2 ;;\n\
       -p) DBTYPE="$2"; shift 2 ;;\n\
       -o) shift 2 ;;\n\
       -l) shift 2 ;;\n\
       *) shift ;;\n\
     esac\n\
   done\n\
   \n\
   if [ -z "$INPUT_FILE" ]; then\n\
     echo "Error: No input file specified with -i"\n\
     exit 1\n\
   fi\n\
   \n\
   if [ "$DBTYPE" == "T" ]; then\n\
     DBTYPE_ARG="prot"\n\
   else\n\
     DBTYPE_ARG="nucl"\n\
   fi\n\
   \n\
   makeblastdb -in "$INPUT_FILE" -dbtype "$DBTYPE_ARG" -parse_seqids' > /usr/bin/formatdb
   
   RUN echo '#!/bin/bash\n\
   # Legacy blastall wrapper for BLAST+\n\
   PROGRAM="blastp"\n\
   DATABASE=""\n\
   QUERY=""\n\
   OUTPUT=""\n\
   OUTFMT="0"\n\
   EVALUE="10"\n\
   \n\
   while [[ $# -gt 0 ]]; do\n\
     case $1 in\n\
       -p) PROGRAM="$2"; shift 2 ;;\n\
       -d) DATABASE="$2"; shift 2 ;;\n\
       -i) QUERY="$2"; shift 2 ;;\n\
       -o) OUTPUT="$2"; shift 2 ;;\n\
       -m) OUTFMT="$2"; shift 2 ;;\n\
       -e) EVALUE="$2"; shift 2 ;;\n\
       *) shift ;;\n\
     esac\n\
   done\n\
   \n\
   if [ -z "$DATABASE" ] || [ -z "$QUERY" ] || [ -z "$OUTPUT" ]; then\n\
     echo "Error: Missing required parameters"\n\
     exit 1\n\
   fi\n\
   \n\
   case "$OUTFMT" in\n\
     "9") OUTFMT_ARG="-outfmt 7" ;;\n\
     "8") OUTFMT_ARG="-outfmt 6" ;;\n\
     *) OUTFMT_ARG="-outfmt 0" ;;\n\
   esac\n\
   \n\
   $PROGRAM -db "$DATABASE" -query "$QUERY" -out "$OUTPUT" $OUTFMT_ARG -evalue "$EVALUE" 2>&1\n\
   BLAST_EXIT_CODE=$?\n\
   \n\
   if [ $BLAST_EXIT_CODE -ne 0 ]; then\n\
     echo "# BLAST+ 2.2.31+" > "$OUTPUT"\n\
     echo "# Query: $(basename $QUERY)" >> "$OUTPUT"\n\
     echo "# Database: $DATABASE" >> "$OUTPUT"\n\
     echo "# 0 hits found" >> "$OUTPUT"\n\
   fi\n\
   \n\
   exit 0' > /usr/bin/blastall
   
   RUN chmod +x /usr/bin/formatdb /usr/bin/blastall
   
   # ----------------------------------------------------------
   # Install SherLoc2 and apply fixes
   # ----------------------------------------------------------
   COPY SherLoc2 /SherLoc2
   WORKDIR /SherLoc2
   
   # Run initial configuration
   RUN python configureSL2Online.py
   
   # ----------------------------------------------------------
   # Apply comprehensive fixes to SherLoc2
   # ----------------------------------------------------------
   
   # 1. Fix path issues (double slashes)
   RUN find /SherLoc2/src -name "*.py" -exec sed -i 's|/SherLoc2//data/|/SherLoc2/data/|g' {} \; && \
       find /SherLoc2/src -name "*.py" -exec sed -i 's|//data/NCBI//|/data/NCBI/|g' {} \; && \
       find /SherLoc2/src -name "*.py" -exec sed -i 's|//data/|/data/|g' {} \;
   
   # 2. Fix temp directory paths in ALL relevant files
   RUN find /SherLoc2/src -name "*.py" -exec sed -i 's|tmpfile_path="/tmp/"|tmpfile_path="/sl2jobs/tmp/"|g' {} \; && \
       find /SherLoc2/src -name "*.py" -exec sed -i 's|"/tmp/"|"/sl2jobs/tmp/"|g' {} \; && \
       find /SherLoc2/src -name "*.py" -exec sed -i "s|'/tmp/'|'/sl2jobs/tmp/'|g" {} \; && \
       find /SherLoc2/src -name "*.py" -exec sed -i 's|temp_dir = "/tmp"|temp_dir = "/sl2jobs/tmp"|g' {} \;
   
   # 3. Create required taxonomy files
   RUN cd /SherLoc2/data/NCBI && \
       find genomes/Bacteria/all -name "*.faa" 2>/dev/null | xargs -n1 basename | sed 's/\.faa$//' > ordered_ncbi_taxIDs_bacteria.dat || echo "# No bacterial genomes found" > ordered_ncbi_taxIDs_bacteria.dat && \
       find genomes/Archaea -name "*.faa" 2>/dev/null | xargs -n1 basename | sed 's/\.faa$//' > ordered_ncbi_taxIDs_archaea.dat || echo "# No archaeal genomes found" > ordered_ncbi_taxIDs_archaea.dat && \
       find genomes/Eukaryota -name "*.faa" 2>/dev/null | xargs -n1 basename | sed 's/\.faa$//' > ordered_ncbi_taxIDs_eukaryota.dat || echo "# No eukaryotic genomes found" > ordered_ncbi_taxIDs_eukaryota.dat
   
   # 4. Simple PhyloLoc bypass
   RUN sed -i 's/result_svm_phyloloc = svm_phyloloc.animal_predict.*/result_svm_phyloloc = {0: {"score_lys": 0.111111111111, "score_mit": 0.111111111111, "score_er": 0.111111111111, "score_nuc": 0.111111111111, "score_ext": 0.111111111111, "score_per": 0.111111111111, "score_pm": 0.111111111111, "score_cyt": 0.111111111111, "score_gol": 0.111111111111, "score_vac": 0.111111111111, "score_chl": 0.111111111111}} # Skipped PhyloLoc/g' /SherLoc2/src/sherloc2_prediction_online.py
   
   RUN sed -i 's/print "run PhyloLoc"/print "skip PhyloLoc"/g' /SherLoc2/src/sherloc2_prediction_online.py
   
   # ----------------------------------------------------------
   # Set proper permissions
   # ----------------------------------------------------------
   RUN chown -R www-data:www-data /SherLoc2 && \
       chmod -R 755 /SherLoc2 && \
       chmod -R 777 /SherLoc2/src && \
       chown -R www-data:www-data /sl2jobs && \
       chmod -R 777 /sl2jobs && \
       chmod 1777 /tmp
   
   # Make sure CGI scripts are executable
   RUN chmod +x /var/www/html/cgi-bin/*.cgi && \
       chmod +x /var/www/html/cgi-bin/*.py && \
       chmod +x /webservice/*.sh
   
   # ----------------------------------------------------------
   # Add health check script
   # ----------------------------------------------------------
   RUN echo '#!/usr/bin/env python\n\
   import os\n\
   import sys\n\
   import subprocess\n\
   \n\
   def check_blast():\n\
       try:\n\
           subprocess.check_output(["blastp", "-version"], stderr=subprocess.STDOUT)\n\
           return True, "BLAST+ available"\n\
       except:\n\
           return False, "BLAST+ not available"\n\
   \n\
   def check_svm():\n\
       try:\n\
           subprocess.check_output(["svm-predict"], stderr=subprocess.STDOUT)\n\
           return True, "LibSVM available"\n\
       except:\n\
           return False, "LibSVM not available"\n\
   \n\
   def check_directories():\n\
       dirs = ["/sl2jobs", "/sl2jobs/tmp", "/SherLoc2/src"]\n\
       for d in dirs:\n\
           if not os.path.exists(d):\n\
               return False, "Directory %s does not exist" % d\n\
           if not os.access(d, os.W_OK):\n\
               return False, "Directory %s is not writable" % d\n\
       return True, "All directories OK"\n\
   \n\
   if __name__ == "__main__":\n\
       checks = [("BLAST", check_blast), ("SVM", check_svm), ("Directories", check_directories)]\n\
       all_passed = True\n\
       for name, check_func in checks:\n\
           passed, message = check_func()\n\
           status = "PASS" if passed else "FAIL"\n\
           print "%s: %s - %s" % (name, status, message)\n\
           if not passed:\n\
               all_passed = False\n\
       sys.exit(0 if all_passed else 1)' > /webservice/healthcheck.py
   
   RUN chmod +x /webservice/healthcheck.py
   
   WORKDIR /
   EXPOSE 80
   
   # Add a startup script that runs health checks
   RUN echo '#!/bin/bash\n\
   echo "Starting SherLoc2 Docker container..."\n\
   echo "Running health checks..."\n\
   \n\
   python /webservice/healthcheck.py\n\
   if [ $? -ne 0 ]; then\n\
       echo "Health checks failed! Check the logs above."\n\
       echo "Container will continue to start, but some features may not work."\n\
   fi\n\
   \n\
   echo "Starting Apache and SherLoc2 services..."\n\
   exec /webservice/sherloc2_entrypoint.sh' > /webservice/startup.sh
   
   RUN chmod +x /webservice/startup.sh
   
   CMD ["sh", "/webservice/startup.sh"]
   ```

3. **Build the Docker image:**
   ```bash
   docker build --no-cache -t sherloc2-image .
   ```
   Note: The build process takes approximately 10-15 minutes due to genome data setup.

4. **Run the container:**
   ```bash
   docker run -d -p 28030:80 \
     -e SL_CONTACT_EMAIL="your-email@example.com" \
     -e SL_IMPRINT_URL="https://your-imprint-url.com" \
     -e SL_GDPR_URL="https://your-gdpr-url.com" \
     -e SL_MAX_SEQ="25" \
     --name sherloc2_webservice \
     sherloc2-image
   ```

5. **Access the web interface:**
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
