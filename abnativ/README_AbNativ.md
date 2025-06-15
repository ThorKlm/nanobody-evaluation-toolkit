# AbNatiV Batch Analysis for Nanobody Naturalness

Computational framework for large-scale nanobody sequence naturalness assessment through AbNatiV, 
enabling systematic evaluation of therapeutic candidates across extensive sequence libraries. 
Current way of predicitng the naturalness and to measure how good "in-distribution" a given (e.g. generated) sample would be.

## Overview

AbNatiV quantifies nanobody "nativeness" through deep learning assessment of sequence similarity to natural camelid immune repertoires. The methodology provides interpretable scores approaching 1.0 for highly native sequences, establishing 0.8 as the empirically validated threshold distinguishing native from engineered variants. Accordingly, this scoring framework enables systematic filtering of therapeutic candidates based on natural precedent.

**Web Server**: [AbNatiV Online](https://www-cohsoftware.ch.cam.ac.uk/index.php/abnativ) (single sequences only)  
**Repository**: https://gitlab.developers.cam.ac.uk/ch/sormanni/abnativ.git

## Installation & Setup

Due to computational requirements and Linux dependencies, WSL environment configuration becomes essential for Windows users. Follow [WSL Environment Setup](README_main_tools_and_wsl_setup.md) for comprehensive system preparation, subsequently:

```bash
# Clone and setup AbNatiV
git clone https://gitlab.developers.cam.ac.uk/ch/sormanni/abnativ.git
cd abnativ
bash setup_env.sh
conda activate abnativ_env
```

**Direct command line usage**:
```bash
# Score nanobody sequences with alignment
python abnativ_script.py score -i sequences.fasta -odir results/ -oid batch_name -isVHH -nat VHH -align
```

## Batch Processing

### Input Structure
```
C:\WSL\abnativ_batches\
├── batch_1.fasta
├── batch_2.fasta
└── ...
```

### Running Analysis
```bash
python abnativ_local_script_for_linux.py
```

### Output Structure
```
C:\WSL\abnativ_output\
├── batch_1_results/batch_5_abnativ_res_scores.csv  # Single amino acid measures
├── batch_1_results/batch_5_abnativ_seq_scores.csv  # Final measures split into 4 values
├── batch_2_results/
...
```

## Results Analysis

![AbNatiV Naturalness Distributions](abnativ_naturalness_distributions.png)

Naturalness score distributions were analyzed across functional domains. 
Framework regions exhibited high conservation (0.910 ± 0.088, range: 0.136-1.000) 
while CDR regions showed increased variability. 
CDR1 and CDR2 demonstrated moderate naturalness (0.652 ± 0.322 and 0.627 ± 0.319 
respectively) with ranges extending to negative values 
(-1.514 to 1.000 and -2.800 to 1.000). CDR3 displayed the lowest scores 
(0.428 ± 0.176, range: -2.302 to 0.969), consistent with hypervariable regions. 
Overall VHH scores (0.812 ± 0.083) indicated most sequences exceeded the 0.8 
naturalness threshold, *(even though this evaluation might indicate that 0.8 might be a quite high threshold, 
as actual ground truth database samples up to a significant share do not exceed this threshold)*. 
Negative CDR scores suggested reduced naturalness compared 
to native repertoires, validating expected biological patterns across 1051 sequences.

## Reference

- Ramon, A., Ali, M., Atkinson, M., Saturnino, A., Didi, K., Visentin, C., ... & Sormanni, P. (2024). Assessing antibody and nanobody nativeness for hit selection and humanization with AbNatiV. Nature Machine Intelligence, 6(1), 74-91.
