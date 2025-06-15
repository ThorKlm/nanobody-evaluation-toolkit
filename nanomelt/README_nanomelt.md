# NanoMelt Integration for Nanobody Thermostability Assessment

Another tool for nanobody evaluation, NanoMelt provides machine learning-based prediction of nanobody apparent melting temperatures using ensemble learning and sequence embeddings.

## Methodology

NanoMelt employs ensemble machine learning trained on 640 experimental melting temperature measurements to predict nanobody thermostability. The method uses sequence embeddings to provide robust predictions across diverse nanobody sequences, including those distant from training data.

## Implementation/ Web server

**Web Server:** https://www-cohsoftware.ch.cam.ac.uk/index.php/nanomelt

### Input/Output
- **Input**: Single nanobody sequence or FASTA file (max 250 sequences)
- **Output**: Predicted apparent melting temperature (Tm)
- **Processing**: Web-based analysis with email notification for batch jobs

### Access Requirements
- Requires the creation of an account, but accepts e.g. university mail-accounts without problems
- Amino acid sequences only (20 standard residues)
- Processing time: Several minutes per submission
- Batch processing available via downloadable method

## Integration Purpose

Provides thermostability assessment complementing aggregation-based developmentability metrics. High melting temperatures correlate with improved stability during manufacturing and storage, representing a critical factor in nanobody development success.

## Analysis Results

NanoMelt analysis of 1,049 nanobody sequences from SABDAB shows a normal distribution of predicted melting temperatures.

### Key Findings

The dataset exhibits an average melting temperature of **67.3 ± 4.8°C**, with median at 66.7°C. Temperature predictions range from 48.7°C to 86.8°C, indicating diverse thermal stability across nanobody sequences.

Most sequences cluster around the mean, with relatively few outliers at extreme temperatures. This suggests the majority of nanobodies have moderate-to-good thermal stability suitable for therapeutic applications.

### Visualization

![NanoMelt Temperature Distribution](nanomelt_temperature_distribution.png)
*Figure: Distribution of predicted melting temperatures for nanobody sequences. Orange dashed line shows mean (67.3°C), red solid line shows median (66.7°C). The near-normal distribution indicates consistent thermal properties across the dataset.*

The distribution's shape and central tendency around 67°C aligns with typical therapeutic protein stability requirements, where temperatures above 60°C generally indicate sufficient stability for pharmaceutical development and storage.

## References

- Ramon A, Predeina O, Gaffey R, Kunz P, Onuoha S, and Sormanni P
Prediction of protein biophysical traits from limited data: a case study on nanobody thermostability through NanoMelt
MAbs 2025 doi.org/10.1080/19420862.2024.2442750