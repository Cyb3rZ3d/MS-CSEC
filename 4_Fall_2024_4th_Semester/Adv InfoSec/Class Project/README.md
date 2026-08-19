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
