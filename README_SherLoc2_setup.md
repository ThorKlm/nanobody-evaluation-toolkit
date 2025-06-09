# SherLoc2 - Local Docker Deployment on Windows 
SherLoc2 is a bioinformatics tool for predicting subcellular localizations of 
eukaryotic proteins using a hybrid system of SVM-based and knowledge-driven 
predictors. 
## Overview SherLoc2 combines the results of multiple sub-predictors:
- **SVMTarget**: Detects N-terminal targeting sequences (SPs, MTPs, CTPs)
- **SVMSA**: Identifies signal anchors
- **SVMaac**: Analyzes amino acid composition
- **MotifSearch**: Recognizes sequence motifs (NLS, KDEL, SKL)
- **GOLoc**: Uses Gene Ontology terms
- **PhyloLoc**: Uses phylogenetic profiles (78 reference genomes)
- **EpiLoc**: Uses text-mined features from PubMed
## Requirements
- **Docker Desktop for Windows** - 
- A terminal (PowerShell, WSL, or Git Bash)
- Internet access for downloading genomes (optional)
- Input sequences in **FASTA format**: 
``` >your_sequence_id MAKERSFAKESEQUENCEHERE ``` 
## Directory Structure Ensure your project structure matches: 
``` 
SherLoc2/ 
│ 
├── SherLoc2Jobs/ # Temporary job folder (bind-mounted) 
├── SherLoc2/data/ 
│     └── NCBI/genomes/ # Genome files (e.g., 9606.faa) 
└── Dockerfile 
``` 
Example of a genome file: 
``` 
SherLoc2/data/NCBI/genomes/Eukaryota/9606.faa 
``` 
## Pre-Docker Setup Convert all scripts to Unix line endings (from Windows CRLF): 
```
bash dos2unix webservice/*.sh dos2unix webservice/*.py dos2unix webservice/*.cgi 
``` 
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
Replace the above with your actual Dockerfile content. 
## Build Docker Image From the root of the project directory: 
```
bash docker build --no-cache -t sherlco2-image . 
``` 
## Run Container 
```
powershell docker rm -f abi_webservice_sherloc2 docker run -d -p 28030:80 
-e SL_CONTACT_EMAIL="abi-services@informatik.uni-tuebingen.de" 
-e SL_IMPRINT_URL="https://www-abi.informatik.uni-tuebingen.de/imprint" 
-e SL_GDPR_URL="https://www-abi.informatik.uni-tuebingen.de/gdpr" 
-e SL_MAX_SEQ="25" 
-v "${PWD}\SherLoc2Jobs:/sl2jobs" 
-v "${PWD}\SherLoc2\data\NCBI\genomes:/SherLoc2/data/NCBI/genomes" 
--name abi_webservice_sherloc2 
sherlco2-image 
``` 
## Access Web Interface Open your browser and visit: 
``` 
http://localhost:28030/cgi-bin/webloc.cgi 
``` 
Paste FASTA sequence and choose organism origin (`animal`, `plant`, `fungal`). 
## Running Predictions Manually (Optional) Enter container shell: 
```
bash docker exec -it abi_webservice_sherloc2 bash 
``` 
List jobs: 
```
bash ls /sl2jobs 
``` 
Run a specific job: 
```
bash bash /sl2jobs/<job_id>__run.sh 
``` 
## Troubleshooting ### File not found (.faa) Example error: 
``` 
.faa does not exist: File /SherLoc2/data/NCBI/genomes/Eukaryota/9606.faa 
``` 
Make sure the expected `.faa` file exists 
and is bind-mounted into the container at: 
``` 
-v "${PWD}\SherLoc2\data\NCBI\genomes:/SherLoc2/data/NCBI/genomes" 
``` 
### Permission Denied on /tmp If you get: 
``` 
IOError: [Errno 13] Permission denied: '/tmp/<file>' 
```
Fix it by either: 
```
bash chmod 1777 /tmp 
```
Or inside the container: 
```
bash mkdir -p /sl2jobs/tmp chmod 777 /sl2jobs/tmp export TMPDIR=/sl2jobs/tmp 
``` 
Then rerun the job. ## Downloading Genomes (Optional) You can use: 
```
powershell Invoke-WebRequest -Uri "https://ftp.ncbi.nlm.nih.gov/refseq/release/complete/complete.
nonredundant_protein.faa.gz" -OutFile "complete.nonredundant_protein.faa.gz" 
```
## Success Once the job finishes, it generates: 
- `__result` → prediction output 
- - `__epiloc.txt` → EpiLoc terms 
- - `__run.sh` → reproducible script Monitor via: 
```bash docker logs -f abi_webservice_sherloc2 
``` 
Or open `http://localhost:28030/cgi-bin/webloc.cgi`.
