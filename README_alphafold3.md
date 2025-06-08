# AlphaFold3-Based Nanobody-Antigen Binding Evaluation

## Project Overview

This subproject evaluates nanobody-antigen binding using **AlphaFold3**, based on multi-seed prediction consistency and binding energy estimation. It has been moved to a dedicated repository for better structure and usability.

 **New repository:**  
 [https://github.com/ThorKlm/AlphaFold3-Prodigy-Antibody-Evaluation](https://github.com/ThorKlm/AlphaFold3-Prodigy-Antibody-Evaluation)

## What It Does

- Uses **AlphaFold3 ZIP outputs** (e.g., from [alphafoldserver.com](https://alphafoldserver.com))
- Automatically extracts structures, aligns by antigen, and calculates:
  - Pose consistency via antigen-aligned **MSE**
  - Binding energy via **PRODIGY** and a contact-based heuristic
- Aggregates results across all seeds and all nanobody-antigen experiments
- Generates plots, binding energy distributions, and **confusion matrices** to compare specificity

## References

- **AlphaFold3**: Jumper et al. (2024) – “AlphaFold3 predicts structures of protein complexes and interactions with small molecules and nucleic acids.” [DeepMind Blog](https://www.deepmind.com/blog/alphafold3-a-unified-model-of-protein-structure-and-interactions)
- **PRODIGY**: Xue et al. (2016) – “PRODIGY: A web server for predicting the binding affinity of protein–protein complexes.” *Bioinformatics.*

Please refer to the new repository’s README for setup, usage, and example output files.
