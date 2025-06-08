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