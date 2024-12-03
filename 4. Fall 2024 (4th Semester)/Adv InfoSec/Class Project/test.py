import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Loading the dataset
dataset_path = '/Users/cyberzed/Documents/GitHub/MS-CSEC/4. Fall 2024 (4th Semester)/Adv InfoSec/Class Project/cybersecurity_attacks.csv'
df = pd.read_csv(dataset_path)

# Selecting relevant columns for the analysis
df = df[['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Attack Type']]

# Encoding categorical variables
df_encoded = pd.get_dummies(df, columns=['Protocol', 'Attack Type'])

# Selecting the target variable ('Attack Type_DDoS') and splitting the data
X = df_encoded.drop('Attack Type_DDoS', axis=1)
y = df_encoded['Attack Type_DDoS']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Measuring the time to train a RandomForestClassifier
start_time = time.time()
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
training_time = time.time() - start_time

# Measuring the time to generate predictions
start_time = time.time()
predictions = model.predict(X_test)
prediction_time = time.time() - start_time

# Calculating accuracy
accuracy = accuracy_score(y_test, predictions)

# Output results
print(f"Training Time: {training_time} seconds")
print(f"Prediction Time: {prediction_time} seconds")
print(f"Accuracy: {accuracy}")
