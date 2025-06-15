# Rosetta Nanobody-Antigen Binding Evaluation

PyRosetta-based framework for predicting nanobody-antigen binding through ensemble docking with IgFold structure generation.

## Overview

This project implements Rosetta protocols for evaluating nanobody-antigen binding interactions. The development process involved resolving numerous technical challenges related to PyRosetta compilation, dependency management, and API compatibility before achieving a functional pipeline supporting both local and cloud-based execution.

## Implementation Approaches

### Local Installation (WSL/Linux)

Complex installation requiring specific Python versions, library dependencies, and environment configurations. See detailed setup instructions below.

### Google Colab Deployment

Streamlined cloud implementation providing GPU acceleration for IgFold predictions and simplified setup.

Notebook: `rosetta_igfold_nanobody_binding_prediction_pipeline_GoogleColab.ipynb`

Based on: [PyRosetta Notebooks - Docking Tutorial](https://github.com/RosettaCommons/PyRosetta.notebooks/tree/master/notebooks/12.00-Protein-Docking)

## Evaluation Results

Multi-seed analysis of 36 nanobody-antigen pairs (6×6 matrix) was conducted using PyRosetta DockingProtocol with 10 independent runs per combination.

### Key Findings

The evaluation revealed **no reasonable specificity** for correct binding partners. Mean binding energy across all pairs was -4.3 ± 1.4 REU, with only 10/36 combinations showing binding energies below -5 REU. Critically, these strong binders were distributed randomly across the matrix rather than clustering along the diagonal where true binding pairs reside.

### Visualization

![PyRosetta Binding Matrix](binding_matrix_pyrosetta4_igfold.png)
*Figure: Binding energy matrix showing no preferential binding along the diagonal (red boxes). Values represent the mean and with ± the standard deviation across 10 seeds. The uniform distribution of binding energies indicates insufficient specificity to be used in the subsequent experiments.*

### Limitations

The current PyRosetta implementation with standard DockingProtocol fails to discriminate between actual binding and non-binding nanobody-antigen pairs. Possible causes include:
- Insufficient sampling of conformational space
- Generic scoring function not optimized for antibody interfaces
- Lack of antibody-specific docking protocols (SnugDock unavailable in current build)
- IgFold structure accuracy limitations

Even tought this experiment was heavily inspired by the current official implementation, 
there could be unexplored options, like Alphafold3 nanobodies instead of igFold or other options that might enhance its capabilities and specificity.
## Local Setup Instructions

### Prerequisites

- Ubuntu/WSL2 on Windows
- Miniconda or Anaconda installed
- At least 20GB free disk space
- Academic license for PyRosetta (https://www.pyrosetta.org/downloads)

### Environment Setup

```bash
conda create -n pyrosetta_igfold python=3.8 -y
conda activate pyrosetta_igfold
conda install numpy pandas biopython pytorch torchvision cpuonly -c pytorch -y
pip install igfold transformers==4.25.1 huggingface-hub==0.11.1 tokenizers==0.13.2
```

### PyRosetta Installation

1. Download from https://www.pyrosetta.org/downloads
2. Install: `pip install PyRosetta-4.Release.python38.linux.release-[version].whl`
3. Set environment: `export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6`

## References

- Ruffolo, J. A., Chu, L. S., Mahajan, S. P., & Gray, J. J. (2023). Fast, accurate antibody structure prediction from deep learning on massive set of natural antibodies. Nature communications, 14(1), 2389.
- Das, R., & Baker, D. (2008). Macromolecular modeling with rosetta. Annu. Rev. Biochem., 77(1), 363-382.
- Leaver-Fay, A., Tyka, M., Lewis, S. M., Lange, O. F., Thompson, J., Jacak, R., ... & Bradley, P. (2011). ROSETTA3: an object-oriented software suite for the simulation and design of macromolecules. In Methods in enzymology (Vol. 487, pp. 545-574). Academic Press.
- Chaudhury, S., Lyskov, S., & Gray, J. J. (2010). PyRosetta: a script-based interface for implementing molecular modeling algorithms using Rosetta. Bioinformatics, 26(5), 689-691.
- Ruffolo, J. A., Sulam, J., & Gray, J. J. (2022). Antibody structure prediction using interpretable deep learning. Patterns, 3(2).
- Adolf-Bryfogle, J., Labonte, J. W., Kraft, J. C., Shapovalov, M., Raemisch, S., Lütteke, T., ... & Schief, W. R. (2024). Growing Glycans in Rosetta: Accurate de novo glycan modeling, density fitting, and rational sequon design. PLoS computational biology, 20(6), e1011895.- Weitzner, B.D., Jeliazkov, J.R., Lyskov, S., Marze, N., Kuroda, D., Frick, R., Adolf-Bryfogle, J., Biswas, N., Dunbrack Jr, R.L., & Gray, J.J. (2017). Modeling and docking of antibody structures with Rosetta. Nature Protocols, 12(2), 401-416.
- Sircar, A., & Gray, J. J. (2010). SnugDock: paratope structural optimization during antibody-antigen docking compensates for errors in antibody homology models. PloS computational biology, 6(1), e1000644.
