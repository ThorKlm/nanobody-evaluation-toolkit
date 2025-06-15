# AGGRESCAN Integration for Aggregation Propensity Assessment

Computational framework for nanobody sequence aggregation prediction through AGGRESCAN, providing Na4vSS scores where negative values indicate favorable solubility profiles.

## Overview

AGGRESCAN quantifies protein aggregation propensity through amino acid sequence analysis. The methodology establishes 0.0 as the threshold distinguishing low-risk (negative) from high-risk (positive) sequences for therapeutic applications.

**Web Server**: http://bioinf.uab.es/aggrescan/

## Usage

When you execute [aggrescan copy and paste script](aggrescan_copy_and_paste_script.py) and the source data is correctly placed,
the FASTA sequences of the acutal batch are automatically copied to the clipboard, you could then paste them into AGGRESCAN web interface, and save the complete webpage results as text files (with the name provided by the script, so that the next time it could copy the next batch).
The visualization script automatically processes these files to generate distribution plots and summary statistics.

## Evaluation Results

AGGRESCAN analysis of 1,212 nanobody sequences demonstrates favorable aggregation profiles with an average Na4vSS score of **-6.31 ± 4.89**, ranging from -20.10 to 29.80. **92.6% of sequences show low aggregation risk** (Na4vSS < 0), while only 7.4% exceed the zero threshold.

![AGGRESCAN Na4vSS Distribution](aggrescan_na4vss_distribution.png)
*Figure: Distribution of Na4vSS aggregation scores. Blue bars indicate low aggregation risk (Na4vSS < 0), dark blue bars show high aggregation risk (Na4vSS ≥ 0). Orange dashed line shows mean (-6.31), gold line shows median (-6.20). The predominantly negative distribution indicates favorable aggregation profiles.*

## Integration Purpose

Provides sequence-based aggregation assessment complementing structure-based developmentability metrics. 
Low Na4vSS scores correlate with reduced aggregation risk during manufacturing and storage.

## References

- Conchillo-Solé, O., de Groot, N. S., Avilés, F. X., Vendrell, J., Daura, X., & Ventura, S. (2007). AGGRESCAN: a server for the prediction and evaluation of" hot spots" of aggregation in polypeptides. BMC bioinformatics, 8, 1-17.