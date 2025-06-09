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

#### HADDOCK3 (Optional - Computationally Intensive)
```bash
pip install haddock3==2025.5.0
haddock3 --version  # Verify installation
```

### Directory Structure
```bash
mkdir -p /mnt/c/WSL/{sequences,sequences_evaluation,structures,structures_evaluation,results}
```

## Verification

### Package Testing
```bash
conda activate Rosetta

# Test core imports
python -c "import pandas, matplotlib, seaborn, numpy, scipy; print('Core packages OK')"

# Test tools
python abnativ/abnativ_script.py --help
haddock3 --help  # If installed
```

### Environment Export
```bash
conda env export --no-builds > environment.yml
```

## Key Package Versions

- Python: 3.9.23
- NumPy: 2.0.2
- Pandas: 2.3.0  
- BioPython: 1.85
- HADDOCK3: 2025.5.0 (optional)

## Troubleshooting

### Common Issues
- **DNS failures**: Apply DNS fix in system setup
- **Package conflicts**: Use `sudo apt --fix-broken install`
- **HADDOCK3 installation**: Use pip if conda channels fail
- **IgFold dependencies**: Install from GitHub for latest version

### Resource Considerations
HADDOCK3 docking jobs require significant computational resources and extended runtime. Consider computational constraints when planning batch evaluations.

## Integration Notes

This environment provides the foundation for structure-based nanobody evaluation experiments. Tools integrate with the broader developmentability assessment pipeline through standardized input/output formats and scoring methodologies.