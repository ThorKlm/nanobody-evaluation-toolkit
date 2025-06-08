# Nanobody Evaluation Toolkit

## Project Overview

This project compares different computational tools for evaluating nanobody-antigen binding using the same set of 5x5 nanobody-antigen pairs. We test multiple approaches to see which ones work best for predicting binding:

**Tools being compared:**
- **HADDOCK 2.4** - Protein-protein docking webserver
- **AlphaFold2 Multimer v3** - Structure prediction for protein complexes
- **AlphaFold3** - Latest version for complex prediction
- **Rosetta** - Classical molecular modeling suite
- **Additional tools** - AbNatiV (nanobody scoring), IgFold (structure prediction)

**The goal:** Figure out which computational method gives the most reliable predictions for nanobody-antigen binding by testing them all on the same dataset and comparing results.

Each tool gets the same 25 nanobody-antigen combinations (5 nanobodies × 5 antigens) and we analyze which ones correctly identify the real binding pairs vs the wrong combinations.

## WSL Setup Instructions (Windows)

### 1. Install WSL Ubuntu 24.04
```bash
# In Windows PowerShell (as Administrator)
# wsl --install -d Ubuntu-24.04
# Alternatively download the latest official version
```

```bash
# If you have internet connectivity issues in WSL
sudo rm -f /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
sudo chattr +i /etc/resolv.conf
ping google.com  # Test connectivity
```

3. Install Miniconda
```bash
# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Follow the installer prompts, then restart terminal
```

4. Create Conda Environment with Exact Versions
```bash
# Create environment (note: using "Rosetta" as environment name to match working setup)
conda create -n Rosetta python=3.9 -y
conda activate Rosetta

# Install system dependencies first
sudo apt update && sudo apt upgrade -y
sudo apt --fix-broken install  # Fix any broken packages

# Install critical packages with exact versions from working environment
conda install -c conda-forge numpy=2.0.2 -y
conda install -c conda-forge scipy=1.13.1 -y  
conda install -c conda-forge matplotlib=3.9.4 -y
conda install -c conda-forge pandas=2.3.0 -y
conda install -c conda-forge pdb-tools=2.5.0 -y
conda install -c conda-forge freesasa=2.2.1 -y
conda install -c conda-forge openmm=7.7.0 -y
conda install -c conda-forge pdbfixer=1.8.1 -y

# Install via pip to get exact versions
pip install seaborn==0.13.2
pip install plotly==6.0.1
pip install biopython==1.85
pip install jupyter
```

5. Install Structure Prediction Tools
IgFold (Nanobody Structure Prediction)
```bash 
conda activate Rosetta
# Install IgFold from GitHub for latest version
pip install git+https://github.com/facebookresearch/IgFold.git
# Fix torch vision compatibility if needed
conda install torchvision=0.11.3 -y
```

AbNatiV (Nanobody Quality Scoring)
```bash 
# Clone AbNatiV repository
git clone https://gitlab.developers.cam.ac.uk/ch/sormanni/abnativ.git
cd abnativ

# Install required bioinformatics tools  
conda install -c bioconda abnumber=0.1.4 -y
conda install -c bioconda anarci=2024.05.21 -y
conda install -c bioconda hmmer=3.3.2 -y

# Test installation
python abnativ_script.py --help
cd ..
```

HADDOCK3 (Advanced Docking Pipeline)
```bash
conda activate Rosetta
# Install via pip (conda version had issues)
pip install haddock3==2025.5.0

# Verify installation
haddock3 --version
haddock3 modules
```

6. Create Data Directory Structure
```bash
# Create all necessary directories for the project
mkdir -p /mnt/c/WSL/sequences
mkdir -p /mnt/c/WSL/sequences_evaluation  
mkdir -p /mnt/c/WSL/structures
mkdir -p /mnt/c/WSL/structures_evaluation
mkdir -p /mnt/c/WSL/results
mkdir -p /mnt/c/WSL/haddock3
mkdir -p /mnt/c/WSL/haddock3_matrix_screening
```

7. Test Your Setup
```bash
conda activate Rosetta

# Test basic imports
python -c "import pandas, matplotlib, seaborn, numpy, scipy; print('Basic packages OK')"

# Test AbNatiV
python abnativ/abnativ_script.py --help

# Test HADDOCK3
haddock3 --help

# Test IgFold (if sequences available)
# python run_igfold.py
```

8. Environment Verification
Your environment should match these key versions:

Python: 3.9.23 (conda-forge)
NumPy: 2.0.2
Pandas: 2.3.0
Matplotlib: 3.9.4
SciPy: 1.13.1
BioPython: 1.85
HADDOCK3: 2025.5.0
OpenMM: 7.7.0

```bash
# Sav[haddock2_4_webserver_evaluation](haddock2_4_webserver_evaluation)e your environment for future recreation
conda activate Rosetta
conda env export --no-builds > environment.yml
```
9. Known Issues and Solutions

DNS Problems: Use the DNS fix in step 2 if wget/pip downloads fail
Package Conflicts: Use sudo apt --fix-broken install for system package issues
HADDOCK3 Installation: Use pip instead of conda if conda channels don't work
IgFold Dependencies: Install from GitHub if conda version is outdated
Large Downloads: HADDOCK3 jobs can take hours, use Ctrl+C to stop if needed

This setup creates a complete environment for comparing nanobody-antigen binding prediction tools.