# Nanobody Evaluation Toolkit

## Project Overview

This project compares different computational tools for evaluating nanobody-antigen binding using the same set of 5x5 nanobody-antigen pairs. We test multiple approaches to see which ones work best for predicting binding:

**Tools being compared:**
- **HADDOCK 2.4** - Protein-protein docking webserver
- **AlphaFold2 Multimer v3** - Structure prediction for protein complexes
- **AlphaFold3** - Latest version for complex prediction, uses MSE over multiple seeds as well as prodigy for binding energy estimation
- **Rosetta** - Classical molecular modeling suite
- **Subcellular localization** - SLPred (https://github.com/cansyl/SLPred), SherLoc2 (https://github.com/KohlbacherLab/SherLoc2)
(comment: SLPred Windows: sed -i 's/python3 /python /g' *.py download_extract_data.sh)
- **Additional tools** - AbNatiV (nanobody scoring), IgFold (structure prediction), Solubis (stability and solubility assessment, http://solubis.switchlab.org).


**The goal:** Figure out which computational method gives the most reliable predictions for nanobody-antigen binding by testing them all on the same dataset and comparing results.

Each tool gets the same 25 nanobody-antigen combinations (5 nanobodies × 5 antigens) and we analyze which ones correctly identify the real binding pairs vs the wrong combinations.


# Environment Setup for Nanobody Evaluation

## Quick Setup Guide

This section provides a minimal conda environment setup for running the nanobody-antigen binding evaluation and plot generation scripts.

### Prerequisites
- Miniconda or Anaconda installed
- Internet connection for package downloads

### Create Local Evaluation Environment

```bash
conda create -n nanobody-eval python=3.9 -y
conda activate nanobody-eval
pip install -r requirements.txt

# Verify installation
python -c "import pandas, matplotlib, seaborn, numpy; print('All packages installed successfully')"
```

4. **Install PRODIGY (optional but recommended):**
   ```bash
   pip install prodigy-protein
   ```

5. **Install the package in development mode:**
   ```bash
   pip install -e .
   ```

### Verifying Installation

You can verify that everything is installed correctly by running:

```bash
python -m alphafold3_eval.cli --check
```