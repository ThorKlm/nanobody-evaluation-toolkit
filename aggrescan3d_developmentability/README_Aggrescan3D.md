# Aggrescan3D Developmentability Scoring Protocol

A minimal Python implementation for converting Aggrescan3D server outputs into a single developmentability score for nanobody candidate ranking.

## Overview

Protein aggregation represents a significant failure mode in nanobody development pipelines. This protocol provides a trivial method to extract a composite aggregation risk score from structure-based Aggrescan3D predictions, enabling systematic candidate filtering and ranking.

## Methodology

### Input Processing
The algorithm processes per-residue Aggrescan3D scores using equal-weighted components (20% each):
- Average aggregation tendency
- Maximum aggregation risk
- Positive score fraction
- High-risk residue density  
- Total aggregation burden

### Score Calculation
The score is the (trivial) combined score of the combination of the following retrieved sub-scores.
```python
score = 0.2 * (avg_component + max_component + pos_fraction_component + 
               high_risk_component + burden_component)
```

## Usage

### Data Acquisition
1. Submit nanobody structure to https://biocomp.chem.uw.edu.pl/A3D2/
2. Download CSV output table
3. Store at a known directory under a known filename of type ".csv"
4. Run the script (the script would open some file selection window).

### Execution
```bash
python quality_score_prediction_by_single_amino_acid_values.py
```

Output format:
```
protein_chain: 0.5602 (N residues)
```

## Score Interpretation

- **≥0.40**: Low aggregation risk
- **0.25-0.39**: Moderate risk, additional validation recommended
- **<0.25**: High aggregation risk

## Integration

Designed for integration into multi-objective optimization pipelines. Not intended as standalone assessment tool.

```python
# Pipeline integration example
dev_score = compute_developmentability_score(aggrescan_scores)
candidate.metrics['developmentability'] = dev_score
```

## Data Format

Required CSV structure:
```
protein,chain,residue,residue_name,score
sample,H,1,Q,-1.4267
sample,H,2,V,-1.3302
...
```

## Dependencies

```bash
pip install pandas numpy
```

## Limitations

- Structure-dependent predictions only
- Context-independent scoring
- Relative ranking metric, not absolute aggregation prediction
- Requires experimental validation for final candidate selection

## References

- Aggrescan3D (A3D) 2.0: prediction and engineering of protein solubility, Nucleic Acids Research, gkz321, 2019
- Aggrescan3D standalone package for structure-based prediction of protein aggregation properties Bioinformatics, btz143, 2019
- AGGRESCAN3D (A3D): server for prediction of aggregation properties of protein structures, Nucleic Acids Research, 43, W306-W313, 2015
- Combining Structural Aggregation Propensity and Stability Predictions To Redesign Protein Solubility, Molecular Pharmaceutics, 10.1021/acs.molpharmaceut.8b00341, 2018
- The example guide for A3D 2.0: A3D 2.0 update for the prediction and optimization of protein solubility, Methods in Molecular Biology (biorxiv preprint), 2021