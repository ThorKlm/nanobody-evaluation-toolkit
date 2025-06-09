# ColabFold Binding Specificity Evaluation

Google Colab-compatible nanobody-antigen binding assessment using ColabFold v1.5.5 with automated batch processing and matrix visualization.

## Methodology

Uses AlphaFold2-Multimer v3 via ColabFold with combined confidence scoring (0.6×ipTM + 0.3×pTM + 0.1×pLDDT/100). Automated FASTA generation processes all nanobody-antigen combinations with binding matrix visualization.

## Implementation

**Google Colab Notebook**: Direct browser execution with GPU runtime

- **Input**: Predefined nanobody/antigen sequence databases
- **Output**: Binding confidence matrices, structure predictions, CSV results
- **Processing**: Sequential prediction with automated analysis

## Key Limitations

- **Deterministic seeding**: Fixed internal seeds without user control
- **Single model output**: No multi-seed consistency analysis
- **Colab constraints**: GPU memory and runtime limitations
- **Static randomization**: Seeds not accessible for modification

## Integration Context

Provides Colab-compatible alternative to AlphaFold3 for initial binding specificity screening. Lacks multi-seed ensemble analysis but offers accessible sequence-based assessment without external server requirements.

## Performance Notes

Generates binding confidence scores through established AlphaFold2-Multimer methodology. Deterministic seeding limitations require experimental validation for definitive binding assessment.

## References

- Mirdita M, Schütze K, Moriwaki Y, Heo L, Ovchinnikov S, Steinegger M. ColabFold: Making protein folding accessible to all. *Nature Methods*, 2022
- Evans R, O'Neill M, Pritzel A, et al. Protein complex prediction with AlphaFold-Multimer. *bioRxiv* 2021