# SolubiS Integration for Protein Optimization

Web-based tool for optimizing protein solubility through stabilizing mutations using combined TANGO aggregation prediction and FoldX stability analysis.

## Methodology

SolubiS identifies point mutations that reduce aggregation while maintaining structural integrity through dual assessment:
- **TANGO**: Aggregation tendency prediction
- **FoldX**: Protein stability estimation (ΔΔG values)

## Implementation

**Web Server**: https://solubis.switchlab.org/node/add/solubis-job

### Aggregation Quality Score (AQS)
```
AQS = ΔTANGO + λ × ΔΔG
```
- **ΔTANGO**: Aggregation reduction [TANGO(WT) - TANGO(mutant)]
- **ΔΔG**: Stability change (kcal/mol)
- **λ**: Stability penalty weight (e.g., λ = 10)

Higher AQS values indicate superior mutations balancing aggregation suppression with fold stability.

## Application

Provides mutation-based optimization for experimental validation by ranking candidates that improve solubility while preserving protein structure,
but also measures to assess protein characteristics.

Team: Van Durme, J., De Baets, G., Rousseau, F., Schymkowitz, J. (VIB Switch Laboratory)