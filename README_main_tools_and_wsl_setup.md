# Linux-Based Nanobody Evaluation Tools 
### WSL-based Windows compatibility

WSL environment configuration for nanobody structure prediction and quality assessment tools, providing reproducible computational setup for binding evaluation experiments.

## Overview

This setup enables comparative evaluation of nanobody-antigen binding prediction using complementary computational approaches. The environment supports structure prediction, quality scoring, and docking methodologies within a standardized Linux framework.

## Core Tools

### Structure Prediction
- **IgFold**: Nanobody structure prediction from sequence
- **HADDOCK3**: Protein-protein docking pipeline (computationally intensive)

### Quality Assessment  
- **AbNatiV**: Nanobody sequence naturalness scoring
- **PDB-tools**: Structure manipulation and analysis utilities

## WSL Environment Setup

### System Installation
```bash
# Install WSL Ubuntu 24.04
wsl --install -d Ubuntu-24.04

# Fix DNS connectivity if needed
sudo rm -f /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
sudo chattr +i /etc/resolv.conf
```

### Miniconda Installation
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Restart terminal after installation
```

### Environment Configuration
```bash
# Create environment with validated package versions
conda create -n Rosetta python=3.9 -y
conda activate Rosetta

# System dependencies
sudo apt update && sudo apt upgrade -y
sudo apt --fix-broken install

# Core scientific packages
conda install -c conda-forge numpy=2.0.2 scipy=1.13.1 matplotlib=3.9.4 pandas=2.3.0 -y
conda install -c conda-forge pdb-tools=2.5.0 freesasa=2.2.1 openmm=7.7.0 pdbfixer=1.8.1 -y

# Additional packages via pip
pip install seaborn==0.13.2 plotly==6.0.1 biopython==1.85 jupyter
```

### Tool Installation

#### IgFold (Structure Prediction)
```bash
pip install git+https://github.com/facebookresearch/IgFold.git
conda install torchvision=0.11.3 -y  # Compatibility fix if needed
```
IgFold could be used via the local script:
```python
import os
from Bio import SeqIO
from igfold import IgFoldRunner
from igfold.refine.pyrosetta_ref import init_pyrosetta

# Initialize PyRosetta for structure refinement
init_pyrosetta()
task_name = "_evaluation"

# Input FASTA file (Windows path via WSL)
input_fasta = "/mnt/c/WSL/sequences"+task_name+"/nanobodies.fasta"

# Output directory for predicted structures
output_dir = "/mnt/c/WSL/structures"+task_name
os.makedirs(output_dir, exist_ok=True)

# Initialize IgFold model
igfold = IgFoldRunner()

# Iterate through all sequences in the FASTA file
for record in SeqIO.parse(input_fasta, "fasta"):
    seq_id = record.id
    sequence = str(record.seq)

    # IgFold expects a dictionary with chain ID as key
    sequences = {"H": sequence}

    output_pdb_path = os.path.join(output_dir, f"{seq_id}.pdb")
    print(f"Predicting structure for {seq_id}...")

    igfold.fold(
        output_pdb_path,
        sequences=sequences,
        do_refine=True,  # Use PyRosetta refinement
        do_renum=False   # Set True if you want Chothia renumbering
    )

    print(f"Saved structure to {output_pdb_path}")
```
#### AbNatiV (Quality Scoring)
```bash
git clone https://gitlab.developers.cam.ac.uk/ch/sormanni/abnativ.git
cd abnativ

# Bioinformatics dependencies
conda install -c bioconda abnumber=0.1.4 anarci=2024.05.21 hmmer=3.3.2 -y

# Verify installation
python abnativ_script.py --help
cd ..
```
AbNativ was then used via the python script called *abnativ_script.py* as present in the Github Repository.

#### HADDOCK3 (Optional - Computationally Intensive)
```bash
pip install haddock3==2025.5.0
haddock3 --version  # Verify installation
```
The Haddock3 associated experiments were conducted using the following specificity evaluation script 
[HADDOCK3 local specificity evaluation script](haddock3/haddock3_local_specificity_evaluation_script.py). 

# Directory Structure Setup

### Standard Evaluation Directory Layout
```bash
# Create standardized directory structure
mkdir -p /mnt/c/WSL/{nanobody_sequences,antigen_structures,nanobody_structures,results}
```

### Input File Organization

#### Nanobody Sequences
```bash
# Place FASTA file in sequences directory
/mnt/c/WSL/nanobody_sequences/nanobodies.fasta
```

#### Antigen Structures  
```bash
# AlphaFold3-derived antigen structures
/mnt/c/WSL/antigen_structures/
├── antigen_albumin_alphafold3.pdb
├── antigen_gfp_alphafold3.pdb  
├── antigen_lysozyme_alphafold3.pdb
├── antigen_mcherry_alphafold3.pdb
├── antigen_nat_alphafold3.pdb
└── antigen_sars_cov2_rbc_alphafold3.pdb
```

### Generated Outputs
```bash
# IgFold predicted nanobody structures
/mnt/c/WSL/nanobody_structures/
├── nbALB_8y9t.pdb
├── nbGFP_6xzf.pdb
└── [additional predicted structures]

# Analysis results
/mnt/c/WSL/results/
├── binding_matrix.csv
├── rosetta_multiseed_raw_results.csv
└── rosetta_multiseed_statistics.csv
```

## Updated Package Versions

Replace in environment configuration:
```bash
# IgFold installation with dependency fixes
pip install igfold biopython==1.81
pip install transformers==4.25.1 huggingface-hub==0.11.1 tokenizers==0.13.2

# Additional Rosetta integration packages
pip install abnumber  # For antibody renumbering
```

## HADDOCK3 Pipeline Integration

Configuration example:
```python
from haddock3_matrix_pipeline import HADDOCK3MatrixScreening

screener = HADDOCK3MatrixScreening(
    structures_dir="/mnt/c/WSL/antigen_structures",
    nanobodies_dir="/mnt/c/WSL/nanobody_structures", 
    output_dir="/mnt/c/WSL/results/haddock3_screening"
)
```

# References

- Giulini, M., Reys, V., Teixeira, J. M., Jiménez-García, B., Honorato, R. V., Kravchenko, A., ... & Bonvin, A. M. (2025). HADDOCK3: A modular and versatile platform for integrative modelling of biomolecular complexes. bioRxiv, 2025-04.
- Van Zundert, G. C. P., Rodrigues, J. P. G. L. M., Trellet, M., Schmitz, C., Kastritis, P. L., Karaca, E., ... & Bonvin, A. M. J. J. (2016). The HADDOCK2. 2 web server: user-friendly integrative modeling of biomolecular complexes. Journal of molecular biology, 428(4), 720-725.