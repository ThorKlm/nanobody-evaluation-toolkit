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

## Limitations

Web server limited to 250 sequences per submission due to computational constraints. Large-scale screening requires local installation from GitLab repository.

## References

- Ramon A, Predeina O, Gaffey R, Kunz P, Onuoha S, and Sormanni P
Prediction of protein biophysical traits from limited data: a case study on nanobody thermostability through NanoMelt
MAbs 2025 doi.org/10.1080/19420862.2024.2442750

**Contact:** Pietro Sormanni  
**Institution:** Yusuf Hamied Department of Chemistry, University of Cambridge