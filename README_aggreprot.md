# AggreProt Integration for Nanobody Developmentability Assessment

Sequence-based aggregation prediction using deep convolutional neural networks to complement structure-based Aggrescan3D analysis.

## Methodology

AggreProt utilizes ensemble deep learning models to identify aggregation-prone regions in protein sequences.
The web server provides per-residue aggregation propensity predictions and suggests mutations for reducing aggregation risk.

## Implementation/ Online Tool

**Web Server:** https://loschmidt.chemi.muni.cz/aggreprot/

- **Input**: Protein sequence (FASTA format)
- **Output**: Per-residue aggregation scores, interactive visualization, mutation suggestions
- **Access**: Free, no registration required

## Integration Rationale

Provides sequence-based aggregation assessment complementing Aggrescan3D's structure-dependent approach. The orthogonal methodologies enhance prediction reliability through different analytical perspectives.

## Limitations

Optimized for APRs ≤50 residues. Performance not guaranteed for large aggregation domains or structure-dependent mechanisms such as disulfide bridge-induced aggregation.

## References

- Planas-Iglesias, J., Borko, S., Swiatkowski, J., Elias, M., Havlasek, M., Salamon, O., Grakova, E., Kunka, A., Martinovic, T., Damborsky, J., Martinovic, J., Bednar, D., 2024: AggreProt: a web server for predicting and engineering aggregation prone regions in proteins. Nucleic Acids Research 52 (W1): W159–W169.