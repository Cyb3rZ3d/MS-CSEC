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
from scipy.stats import chi2_contingency

def load_and_preprocess_data(file_path):
    """
    Load the dataset and perform preprocessing steps such as handling missing values,
    encoding categorical features, and generating time-based features.
    """
    # Load the dataset
    df = pd.read_csv(file_path)

    # Handle missing values (drop rows with missing data)
    df.dropna(inplace=True)

    # Create 'Attack Time' from individual columns if they exist
    if all(col in df.columns for col in ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']):
        df['Attack Time'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])
        df['Hour'] = df['Attack Time'].dt.hour
        df['DayOfWeek'] = df['Attack Time'].dt.dayofweek  # Monday=0, Sunday=6
    else:
        print("Some of the necessary time columns are missing. Time-based analysis will be skipped.")
        df['Hour'] = None
        df['DayOfWeek'] = None

    # Define mappings for categorical features
    browser_mapping = {0: 'Chrome', 1: 'Firefox', 2: 'Safari', 3: 'Edge', 4: 'Opera', 5: 'Brave', 6: 'Other'}
    os_mapping = {0: 'Windows', 1: 'macOS', 2: 'Linux', 3: 'Android', 4: 'iOS'}
    day_of_week_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    traffic_type_mapping = {0: 'DDoS', 1: 'Phishing', 2: 'SQL Injection', 3: 'Brute Force', 4: 'Malware'}

    # Encode categorical features
    label_encoder = LabelEncoder()
    df['Browser'] = label_encoder.fit_transform(df['Browser'])
    df['Device/OS'] = label_encoder.fit_transform(df['Device/OS'])
    df['Traffic Type'] = label_encoder.fit_transform(df['Traffic Type'])  # Assuming Traffic Type is the attack type
    df['Protocol'] = label_encoder.fit_transform(df['Protocol'])

    # Map encoded values back to meaningful names
    df['Browser Name'] = df['Browser'].map(browser_mapping)
    df['OS Name'] = df['Device/OS'].map(os_mapping)
    df['Day of Week Name'] = df['DayOfWeek'].map(day_of_week_mapping)
    df['Traffic Type Name'] = df['Traffic Type'].map(traffic_type_mapping)

    # Ensure all browsers are included in the Browser Name category, even if missing
    df['Browser Name'] = pd.Categorical(df['Browser Name'], categories=list(browser_mapping.values()))

    return df


def train_random_forest(df):
    """
    Train a Random Forest model using the selected features and the attack type as the target variable.
    Return the trained model and test data.
    """
    # Feature Selection for prediction model
    X = df[['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Browser', 'Device/OS']]
    y = df['Traffic Type']  # Target variable (attack type)

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Train the Random Forest classifier
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    return rf_model, X_test, y_test


def evaluate_model(rf_model, X_test, y_test, df):
    """
    Evaluate the trained Random Forest model by displaying accuracy, classification report, and confusion matrix.
    This function replaces numeric class labels (0, 1, 2, etc.) with meaningful attack type names.
    
    Args:
    - rf_model: The trained Random Forest model
    - X_test: The test data for evaluation
    - y_test: The actual labels of the test data
    - df: The original dataframe containing the 'Traffic Type Name' mapping
    """
    # Model predictions
    y_pred = rf_model.predict(X_test)

    # Get the mapping for Traffic Type Name
    traffic_type_mapping = dict(df[['Traffic Type', 'Traffic Type Name']].drop_duplicates().values)

    # Replace numeric labels with actual Traffic Type names for the classification report
    y_test_named = pd.Series(y_test).map(traffic_type_mapping)
    y_pred_named = pd.Series(y_pred).map(traffic_type_mapping)

    # Model evaluation
    print("Accuracy Score:", accuracy_score(y_test_named, y_pred_named))
    print("\nClassification Report:\n", classification_report(y_test_named, y_pred_named))

    # Confusion matrix
    conf_matrix = confusion_matrix(y_test_named, y_pred_named, labels=list(traffic_type_mapping.values()))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=traffic_type_mapping.values(), yticklabels=traffic_type_mapping.values())
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()


def plot_feature_importance(rf_model, X):
    """
    Display the feature importance plot, showing which features contributed the most to the Random Forest model's predictions.
    """
    feature_importance = rf_model.feature_importances_
    features = X.columns
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importance, y=features)
    plt.title('Feature Importance')
    plt.show()


def analyze_attack_time_correlation(df):
    """
    Analyzes the correlation between attack type and the time of attack (hour of day and day of the week).
    Displays results using bar plots.
    """
    if df['Hour'].isnull().all():
        print("No time-based data available for analysis.")
        return

    plt.figure(figsize=(12, 6))
    sns.countplot(x='Hour', hue='Traffic Type Name', data=df, palette='Set2')
    plt.title('Attack Type Distribution by Hour of the Day')
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.countplot(x='Day of Week Name', hue='Traffic Type Name', data=df, palette='Set1',
                  order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    plt.title('Attack Type Distribution by Day of the Week')
    plt.xticks(rotation=45)
    plt.show()


def analyze_source_port_correlation(df):
    """
    Analyzes the correlation between source port and attack type by generating a heatmap.
    The heatmap displays the number of occurrences of each attack type based on the originating source port.
    A chi-square test is performed to determine if the source port is statistically significant in predicting attack type.
    """
    port_vs_attack = pd.crosstab(df['Source Port'], df['Traffic Type Name'])
    chi2, p, dof, expected = chi2_contingency(port_vs_attack)
    print(f"Chi-square test results - p-value: {p}")
    if p < 0.05:
        print("Source Port is statistically significant in predicting attack type.")
    else:
        print("No strong correlation between Source Port and attack type.")
    plt.figure(figsize=(10, 8))
    sns.heatmap(port_vs_attack, cmap="YlGnBu", annot=False)
    plt.title('Heatmap: Source Port vs Attack Type')
    plt.show()


def analyze_browser_os_correlation(df):
    """
    Analyzes the correlation between browsers/operating systems and attack types by generating bar plots.
    Displays the distribution of different attack types across various browsers and operating systems.
    """
    plt.figure(figsize=(12, 6))
    sns.countplot(x='Browser Name', hue='Traffic Type Name', data=df, palette='Set3')
    plt.title('Attack Type Distribution by Browser')
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.countplot(x='OS Name', hue='Traffic Type Name', data=df, palette='Set3')
    plt.title('Attack Type Distribution by Operating System')
    plt.xticks(rotation=45)
    plt.show()


def main():
    """
    Main function to run the program, which includes loading data, training a model, evaluating it,
    and performing exploratory data analysis on attack type correlations.
    """
    file_path = '/Users/cyberzed/Desktop/updated_cybersecurity_attacks.csv'

    # Load and preprocess the data
    df = load_and_preprocess_data(file_path)

    # Train the Random Forest model
    rf_model, X_test, y_test = train_random_forest(df)

    # Evaluate the model
    evaluate_model(rf_model, X_test, y_test, df)  # Pass the dataframe to retain 'Traffic Type Name' mapping

    # Plot feature importance
    plot_feature_importance(rf_model, df[['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Browser', 'Device/OS']])

    # Perform data analysis
    analyze_attack_time_correlation(df)
    analyze_source_port_correlation(df)
    analyze_browser_os_correlation(df)


if __name__ == "__main__":
    main()
 