# Rosetta PyRosetta and IgFold Installation Guide

This guide provides comprehensive instructions for setting up Rosetta PyRosetta and IgFold in a unified environment for nanobody-antigen binding evaluation.

## Prerequisites

- Ubuntu/WSL2 on Windows
- Miniconda or Anaconda installed
- At least 20GB free disk space
- Academic license for PyRosetta (https://www.pyrosetta.org/downloads)

## Environment Setup

### 1. Create Conda Environment

```bash
conda create -n pyrosetta_igfold python=3.8 -y
conda activate pyrosetta_igfold
```

### 2. Install Base Dependencies

```bash
# Core packages
conda install numpy pandas biopython -y

# PyTorch (required for IgFold)
conda install pytorch torchvision cpuonly -c pytorch -y
```

### 3. Install IgFold with Compatible Dependencies

```bash
# Install IgFold
pip install igfold

# Install specific versions to avoid conflicts
pip install transformers==4.25.1 huggingface-hub==0.11.1 tokenizers==0.13.2 datasets==2.8.0
pip install charset-normalizer==2.1.1
```

### 4. Download IgFold Model Weights

If model weights are missing, download them:

```bash
# The models will be automatically downloaded on first use
# Alternatively, copy from existing installation:
# cp -r /path/to/existing/igfold/trained_models $(python -c "import igfold; print(igfold.__path__[0])")/
```

## Rosetta Installation

### Option A: Build PyRosetta from Source (Recommended)

1. **Download Rosetta Source Bundle**
   - Obtain from https://www.rosettacommons.org/software/license-and-download
   - Extract: `tar -xjf rosetta_src_[version]_bundle.tar.bz2`

2. **Build PyRosetta**
   ```bash
   cd rosetta_src_[version]_bundle/source/src/python/PyRosetta/src
   python setup.py install
   ```

3. **Set Environment Variables**
   ```bash
   # Add to ~/.bashrc or activate script
   export ROSETTA_DIR=$HOME/rosetta_src_[version]_bundle
   export PYTHONPATH=$ROSETTA_DIR/source/build/PyRosetta/$(uname -s)-$(uname -m)/$(uname -r)/python-3.8/release/build:$PYTHONPATH
   export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6
   ```

### Option B: Pre-built PyRosetta

1. Download pre-built PyRosetta from https://www.pyrosetta.org/downloads
2. Install wheel:
   ```bash
   pip install PyRosetta-4.Release.python38.linux.release-[version].whl
   ```

## Verification

```bash
# Test imports
python -c "import pyrosetta; print('PyRosetta:', pyrosetta.__version__)"
python -c "from igfold import IgFoldRunner; print('IgFold loaded successfully')"

# Test IgFold
cat > test_igfold.py << 'EOF'
from igfold import IgFoldRunner
igfold = IgFoldRunner()
test_seq = {"H": "QVQLVESGGGLVQPGGSLRLSCAASGFTFSSYAMSWVRQAPGKGLEWVSAISGSGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCARDRRWGQGTLVTVSS"}
igfold.fold("test.pdb", sequences=test_seq)
print("IgFold test successful - check test.pdb")
EOF
python test_igfold.py

# Test PyRosetta
cat > test_pyrosetta.py << 'EOF'
import pyrosetta
pyrosetta.init("-mute all")
print("PyRosetta initialized successfully")
EOF
python test_pyrosetta.py
```

## Running the Evaluation Pipeline

### Structure Generation with IgFold

```bash
cat > generate_structures.py << 'EOF'
from Bio import SeqIO
from igfold import IgFoldRunner
import os

# Initialize IgFold
igfold = IgFoldRunner()

# Input/output paths
input_fasta = "nanobodies.fasta"
output_dir = "structures"
os.makedirs(output_dir, exist_ok=True)

# Generate structures
for record in SeqIO.parse(input_fasta, "fasta"):
    seq_id = record.id
    sequence = str(record.seq)
    sequences = {"H": sequence}
    output_pdb = os.path.join(output_dir, f"{seq_id}.pdb")
    
    print(f"Predicting structure for {seq_id}...")
    igfold.fold(output_pdb, sequences=sequences, do_refine=True)
    print(f"Saved to {output_pdb}")
EOF
```

### Rosetta Binding Evaluation

See `rosetta_3_14_evaluation/` directory for complete scripts.

## Troubleshooting

### Common Issues

1. **ImportError with PyRosetta**
   - Ensure `LD_PRELOAD` is set correctly
   - Check Python version matches PyRosetta build (3.8)

2. **IgFold model weights missing**
   - Models download automatically on first use
   - Check internet connection
   - Verify write permissions in site-packages

3. **Transformer version conflicts**
   - Use exact versions specified above
   - Run `pip list` to verify installed versions

4. **Memory errors**
   - IgFold requires ~4GB RAM per structure
   - Reduce batch size or use one structure at a time

### Environment Export

Save environment for reproducibility:
```bash
conda env export > pyrosetta_igfold_env.yml
```

## Usage in Nanobody Evaluation Pipeline

This installation supports:
- Structure prediction from sequence (IgFold)
- Ensemble generation with different random seeds
- Binding affinity evaluation (Rosetta)
- Interface analysis and scoring

Integration with other tools in the pipeline (AlphaFold3, HADDOCK, etc.) follows similar evaluation protocols using the generated structures.

## References

- Ruffolo, J. A., Chu, L. S., Mahajan, S. P., & Gray, J. J. (2023). Fast, accurate antibody structure prediction from deep learning on massive set of natural antibodies. Nature communications, 14(1), 2389.
- Das, R., & Baker, D. (2008). Macromolecular modeling with rosetta. Annu. Rev. Biochem., 77(1), 363-382.
- Leaver-Fay, A., Tyka, M., Lewis, S. M., Lange, O. F., Thompson, J., Jacak, R., ... & Bradley, P. (2011). ROSETTA3: an object-oriented software suite for the simulation and design of macromolecules. In Methods in enzymology (Vol. 487, pp. 545-574). Academic Press.
- Chaudhury, S., Lyskov, S., & Gray, J. J. (2010). PyRosetta: a script-based interface for implementing molecular modeling algorithms using Rosetta. Bioinformatics, 26(5), 689-691.
