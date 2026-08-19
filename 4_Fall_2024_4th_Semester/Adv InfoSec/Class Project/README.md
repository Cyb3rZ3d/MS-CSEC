# Cyber Attack Dataset Analytics

An Advanced Information Security (CSEC 5327) semester project that explores cybersecurity attack data through statistical analysis, visualization, and machine-learning classification. The submitted report frames the work around attack timing, source ports, and platform-targeting patterns.

## Research Questions

1. Do attack types vary by time of day or day of the week?
2. Can source location or originating port help predict attack type?
3. Are particular browsers or operating systems targeted more frequently for specific attack types?

## Existing Project Files

```text
Class Project/
├── CyberSec_Analytics.py
├── CyberSec_Analytics_1.py
├── CyberSec_Analytics_2.py
├── test.py
└── cybersecurity_attacks.csv
```

The three `CyberSec_Analytics` scripts show the progression of the project from exploratory analysis and Random Forest classification to dense neural-network and 1D-CNN experiments.

## Dataset Inventory

The included CSV contains **40,000 records and 25 columns**. The recorded attack classes are:

| Attack type | Records |
|---|---:|
| DDoS | 13,428 |
| Malware | 13,307 |
| Intrusion | 13,265 |

The traffic-type distribution is HTTP (13,360), DNS (13,376), and FTP (13,264).

## Implemented Work

- Loaded and cleaned cybersecurity event data with pandas.
- Encoded categorical variables and standardized numeric features.
- Split data into 70% training and 30% testing subsets with a fixed random state.
- Implemented a 100-tree Random Forest classifier.
- Implemented a dense neural network with 128- and 64-unit hidden layers and dropout.
- Implemented a 1D-CNN with convolution, max pooling, dropout, flattening, and dense layers.
- Generated classification reports and confusion matrices.
- Measured model training and prediction time.
- Added feature-importance analysis.
- Analyzed activity by time, source port, browser, and operating system.
- Created Seaborn, Matplotlib, and Plotly visualizations, including an interactive port heatmap.

## Recorded Experiment Results

The semester report preserves the following execution output from the project runs:

| Model | Training time | Prediction time | Test accuracy |
|---|---:|---:|---:|
| Random Forest | 4.14 s | 0.20 s | 33.52% |
| Dense neural network | 22.03 s | 0.16 s | 33% |
| 1D-CNN | 10.38 s | 0.17 s | 33% |

The Random Forest classification report records macro and weighted precision, recall, and F1 values of approximately 0.34 across a 12,000-record test set. In these captured runs, all three models performed near one-third accuracy, so the evidence supports an efficiency comparison more strongly than a predictive-performance advantage.

## Report Evidence Gallery

The following 30 original figures were extracted from the submitted semester report and are preserved in report order.

| Sequence | Figure |
|---:|---|
| 01 | [Basic data exploration](report-evidence/01-basic-data-exploration.png) |
| 02 | [Dataset schema](report-evidence/02-dataset-schema.png) |
| 03 | [Descriptive statistics](report-evidence/03-descriptive-statistics.png) |
| 04 | [Missing-value inventory](report-evidence/04-missing-values.png) |
| 05 | [Missing-value cleaning](report-evidence/05-missing-value-cleaning.png) |
| 06 | [Dataset preview](report-evidence/06-dataset-preview.png) |
| 07 | [Dataset information](report-evidence/07-dataset-information.png) |
| 08 | [Null-value check](report-evidence/08-null-value-check.png) |
| 09 | [Month and weekday heatmap](report-evidence/09-month-weekday-heatmap.png) |
| 10 | [Attack-type distribution](report-evidence/10-attack-type-distribution.png) |
| 11 | [Protocol distribution](report-evidence/11-protocol-distribution.png) |
| 12 | [Anomaly score by attack](report-evidence/12-anomaly-score-by-attack.png) |
| 13 | [Source port by attack](report-evidence/13-source-port-by-attack.png) |
| 14 | [Packet length by attack](report-evidence/14-packet-length-by-attack.png) |
| 15 | [Payload word cloud](report-evidence/15-payload-word-cloud.png) |
| 16 | [Random Forest code](report-evidence/16-random-forest-code.png) |
| 17 | [Feature-importance code](report-evidence/17-feature-importance-code.png) |
| 18 | [Preprocessing code](report-evidence/18-preprocessing-code.png) |
| 19 | [Time-correlation code](report-evidence/19-time-correlation-code.png) |
| 20 | [Browser and OS correlation code](report-evidence/20-browser-os-correlation-code.png) |
| 21 | [Attack-time distribution](report-evidence/21-attack-time-distribution.png) |
| 22 | [Source-port correlation code](report-evidence/22-source-port-correlation-code.png) |
| 23 | [Source-port heatmap](report-evidence/23-source-port-heatmap.png) |
| 24 | [Browser and OS analysis code](report-evidence/24-browser-os-analysis-code.png) |
| 25 | [Operating-system distribution](report-evidence/25-operating-system-distribution.png) |
| 26 | [Random Forest results](report-evidence/26-random-forest-results.png) |
| 27 | [Dense-network training start](report-evidence/27-dense-network-training-start.png) |
| 28 | [Dense-network training results](report-evidence/28-dense-network-training-results.png) |
| 29 | [CNN training output](report-evidence/29-cnn-training-output.png) |
| 30 | [CNN training history](report-evidence/30-cnn-training-history.png) |

## Project Progression

1. `CyberSec_Analytics.py` - initial preprocessing, Random Forest classification, feature importance, correlations, and visual analysis.
2. `CyberSec_Analytics_1.py` - expanded interactive visualization and added a dense neural network.
3. `CyberSec_Analytics_2.py` - added a 1D-CNN and model-comparison output.
4. `test.py` - focused Random Forest timing and binary DDoS classification experiment.

## Reproducibility Note

The scripts preserve the original course-project state. They contain hard-coded local file paths, and the later scripts reference `Browser` and `Device/OS` fields that are not present in the included 25-column CSV. Those paths and feature selections must be aligned with the intended dataset before rerunning the complete pipeline. The metrics above are transcribed from the submitted semester report and are not newly reproduced benchmark results.

## Technologies

Python, pandas, NumPy, scikit-learn, TensorFlow/Keras, Matplotlib, Seaborn, Plotly, SciPy, Random Forest, dense neural networks, and 1D convolutional neural networks.

## Responsible Interpretation

This is an academic analytics project. Model output should be validated for dataset quality, class definitions, leakage, bias, and operational relevance before use in a security environment.

## Portfolio

[View the digital project profile](https://cyb3rz3d.github.io/cyber-attack-dataset-analytics.html)
