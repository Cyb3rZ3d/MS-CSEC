#CyberSec_Analytics.py
"""
Ruben Valdez
Adv_InfoSec
Prof. Dr. Alsmadi
Semester Project:   Cyber Security Attacks _ Analytics
"""

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# Load the dataset
file_path = '/mnt/data/updated_cybersecurity_attacks.csv'
df = pd.read_csv(file_path)

# Preprocessing
# Handle missing values (drop rows with missing data)
df.dropna(inplace=True)

# Encode categorical features such as Browser, OS, and Attack Type
label_encoder = LabelEncoder()
df['Browser'] = label_encoder.fit_transform(df['Browser'])
df['Device/OS'] = label_encoder.fit_transform(df['Device/OS'])
df['Traffic Type'] = label_encoder.fit_transform(df['Traffic Type']) # Assuming Traffic Type is the attack type

# Feature Selection
X = df[['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Browser', 'Device/OS']]
y = df['Traffic Type']  # Target variable (attack type)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model training using Random Forest
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Model predictions
y_pred = rf_model.predict(X_test)

# Model evaluation
print("Accuracy Score:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Feature importance
feature_importance = rf_model.feature_importances_
features = X.columns
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance, y=features)
plt.title('Feature Importance')
plt.show()
