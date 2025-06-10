# DeepLoc 2.1 Integration for Subcellular Localization Prediction

Deep learning-based prediction of eukaryotic protein subcellular localization using multi-label classification for 10 cellular compartments and 4 membrane associations.

## Methodology

DeepLoc 2.1 predicts where proteins end up in eukaryotic cells and how they associate with membranes. The tool distinguishes between major cellular locations (nucleus, cytoplasm, mitochondria, etc.) and membrane types (transmembrane, peripheral, lipid anchor, soluble).

## Implementation

**Web Server:** https://services.healthtech.dtu.dk/services/DeepLoc-2.1/

- **Input**: FASTA sequences (max 500, min 10 AA)
- **Output**: Localization predictions with confidence scores
- **Models**: Slow (high-quality) or Fast (high-throughput)
- **Limits**: 4000 AA (slow) or 1022 AA (fast), 4-hour execution

## Integration Context

Provides cellular localization context for nanobody targets, helping assess accessibility and potential therapeutic challenges based on subcellular distribution patterns.

## Usage Notes

Free access including commercial use. For batch processing >100 sequences, use short output format for faster processing.

## References

- Almagro Armenteros, J. J., Sønderby, C. K., Sønderby, S. K., Nielsen, H., & Winther, O. (2017). DeepLoc: prediction of protein subcellular localization using deep learning. Bioinformatics, 33(21), 3387-3395.
- Thumuluri, V., Almagro Armenteros, J. J., Johansen, A. R., Nielsen, H., & Winther, O. (2022). DeepLoc 2.0: multi-label subcellular localization prediction using protein language models. Nucleic acids research, 50(W1), W228-W234.
- Ødum, M. T., Teufel, F., Thumuluri, V., Almagro Armenteros, J. J., Johansen, A. R., Winther, O., & Nielsen, H. (2024). DeepLoc 2.1: multi-label membrane protein type prediction using protein language models. Nucleic Acids Research, 52(W1), W215-W220.

**Institution**: DTU Health Tech, Technical University of Denmark  
**Contact**: Henrik Nielsen