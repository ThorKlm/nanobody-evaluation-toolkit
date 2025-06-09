# SherLoc2 Integration for Subcellular Localization Prediction

Containerized bioinformatics tool for predicting protein subcellular localization in eukaryotic cells using multiple complementary prediction methods.

## Overview

SherLoc2 combines multiple prediction approaches including signal sequence analysis, amino acid composition, sequence motifs, and Gene Ontology terms to predict subcellular localization. This containerized implementation provides web service functionality with compatibility fixes for modern systems.

## Methodology

The tool integrates several prediction modules:
- **SVMTarget**: N-terminal targeting sequences analysis
- **SVMSA**: Signal anchor prediction
- **SVMaac**: Amino acid composition evaluation
- **MotifSearch**: Sequence motif identification (NLS, KDEL, SKL domains)
- **GOLoc**: Gene Ontology term analysis
- **PhyloLoc**: Phylogenetic profiles (currently bypassed)

## Implementation
## Dockerfile Place the following in a file named `Dockerfile`: 
```
# Applied Bioinformatics Group
# SherLoc2 Docker Image
#
# Philipp Thiel

FROM ubuntu:18.04

# Update package repository
RUN apt-get update
#RUN apt-get -y upgrade


# ----------------------------------------------------------
# Install some useful and required stuff
# ----------------------------------------------------------
RUN apt-get install -y dirmngr software-properties-common vim wget


# ----------------------------------------------------------
# Install LibSVM and BLAST
# ----------------------------------------------------------
RUN apt-get install -y libsvm-tools ncbi-blast+


# ----------------------------------------------------------
# Install InterProScan dependencies
# ----------------------------------------------------------
RUN apt-get install -y libgnutls30

# RUN add-apt-repository -y ppa:webupd8team/java
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk

# RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections
# RUN apt-get install -y -q --no-install-recommends oracle-java8-installer
# RUN apt-get install -y -q oracle-java8-set-default
# RUN apt-get install -y openjdk-8-jdk

ENV JAVA_HOME=/usr/lib/jvm/java-8-oracle
ENV CLASSPATH=/usr/lib/jvm/java-8-oracle/bin


# ----------------------------------------------------------
# Setup MultiLoc2 Webservice
# ----------------------------------------------------------
RUN apt-get -y install python-biopython apache2
RUN a2enmod cgid
ADD webservice/apache2.conf         /etc/apache2/apache2.conf
ADD webservice/serve-cgi-bin.conf   /etc/apache2/conf-available/serve-cgi-bin.conf

COPY webservice/webloc.cgi   /var/www/html/cgi-bin/
COPY webservice/epiloc_interface.py   /var/www/html/cgi-bin/
COPY webservice/dialoc_interface.py   /var/www/html/cgi-bin/
COPY webservice/downloads/   /var/www/html/cgi-bin/downloads/
COPY webservice/images/      /var/www/html/cgi-bin/images/

RUN mkdir /webservice
ADD webservice/job_cleanup.sh          /webservice/job_cleanup.sh
ADD webservice/sl2setup.py             /webservice/sl2setup.py
ADD webservice/sherloc2_entrypoint.sh  /webservice/sherloc2_entrypoint.sh

RUN mkdir /sl2jobs
RUN chmod 777 /sl2jobs

# ----------------------------------------------------------
# Install MultiLoc2
# ----------------------------------------------------------
COPY SherLoc2 /SherLoc2
WORKDIR /SherLoc2
RUN python configureSL2Online.py

WORKDIR /
RUN  chown -R www-data:www-data /SherLoc2
RUN  chmod -R 775 /SherLoc2


EXPOSE 80

CMD ["sh", "/webservice/sherloc2_entrypoint.sh"]
```
Replace the above with the default Dockerfile content. 
### Docker Setup
```bash
# Build container
docker build --no-cache -t sherloc2-image .

# Run service
docker run -d -p 28030:80 \
  -e SL_CONTACT_EMAIL="your-email@example.com" \
  -e SL_MAX_SEQ="25" \
  --name sherloc2_webservice \
  sherloc2-image
```

### Access
**Web Interface**: http://localhost:28030/cgi-bin/webloc.cgi

### Input/Output
- **Input**: Protein sequences in FASTA format (max 25 sequences)
- **Output**: Probability scores for subcellular locations
- **Locations**: Nucleus, cytoplasm, mitochondria, ER, Golgi, plasma membrane, peroxisome, lysosome, extracellular
- **Plant-specific**: Chloroplast, vacuole

## Technical Modifications

The containerized version includes compatibility fixes:
- **BLAST+ integration**: Legacy command wrappers for modern BLAST tools
- **Path corrections**: Fixed directory structure issues
- **Permission management**: Proper file access configuration
- **PhyloLoc bypass**: Module disabled due to parsing compatibility issues

## System Requirements

- Docker environment
- 4GB disk space minimum
- Available port (default 28030)
- Build time: 10-15 minutes

## Limitations

- PhyloLoc module bypassed (reduced evolutionary analysis accuracy)
- Maximum 25 sequences per submission
- Large image size (~2GB) due to included genome databases
- Some prediction accuracy reduction without PhyloLoc

## Integration Purpose

Provides subcellular localization prediction for comprehensive nanobody characterization, complementing binding specificity and developmentability assessment in therapeutic development pipelines.

## References

- Briesemeister, S.; Blum, T.; Brady, S.; Lam, Y.; Kohlbacher, O. and Shatkay, H. (2009). SherLoc2: a high-accuracy hybrid method for predicting subcellular localization of proteins. *J. Proteome Res.* 8(11):5363-5366.

**Original Repository**: https://github.com/KohlbacherLab/SherLoc2