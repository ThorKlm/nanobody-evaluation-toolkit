# AlphaFold3-Based Nanobody-Antigen Binding Evaluation

A computational framework for evaluating nanobody-antigen binding specificity using AlphaFold3 multi-seed predictions and binding energy estimation.

## Methodology

The evaluation protocol combines pose consistency analysis across AlphaFold3 seeds with binding affinity prediction. Antigen-aligned MSE calculations quantify structural stability while contact-based and PRODIGY methods estimate interaction strength. True binding pairs exhibit significantly lower pose variance compared to non-specific combinations.

## Implementation

**Repository:** [https://github.com/ThorKlm/AlphaFold3-Prodigy-Antibody-Evaluation](https://github.com/ThorKlm/AlphaFold3-Prodigy-Antibody-Evaluation)

### Input/Output
- **Input**: AlphaFold3 ZIP archives from alphafoldserver.com
- **Output**: MSE matrices, binding energy distributions, specificity analysis
- **Processing**: Automated structure extraction, alignment, and multi-seed aggregation

## Key Features

- Multi-seed pose consistency evaluation
- Dual binding energy estimation (contact-based and ML-based)
- Quantitative specificity discrimination
- Integration-ready for antibody design pipelines

## References

## References

- Abramson, Josh, et al. "Accurate structure prediction of biomolecular interactions with AlphaFold 3." Nature 630.8016 (2024): 493-500.
- Abramson, Josh, et al. "Addendum: Accurate structure prediction of biomolecular interactions with AlphaFold 3." Nature (2024): 1-1.
- Xue, Li C., et al. "PRODIGY: a web server for predicting the binding affinity of protein–protein complexes." Bioinformatics 32.23 (2016): 3676-3678.
- Vangone, Anna, and Alexandre MJJ Bonvin. "Contacts-based prediction of binding affinity in protein–protein complexes." elife 4 (2015): e07454.
- Kastritis, Panagiotis L., et al. "Proteins feel more than they see: fine-tuning of binding affinity by properties of the non-interacting surface." Journal of molecular biology 426.14 (2014): 2632-2652.

Refer to the repository README for complete setup instructions and usage examples.