"""
Ruben Valdez
Adv_InfoSec
Prof. Dr. Alsmadi
Semester Project: Cyber Security Attacks _ Analytics
"""

# Import required libraries
# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
import plotly.express as px
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv1D, MaxPooling1D, Flatten  # Added imports
from time import time
from scipy.stats import chi2_contingency
from plotly.subplots import make_subplots



def load_and_preprocess_data(file_path):
    """
    Load the dataset from the given file path and prepare it for analysis.
    """
    df = pd.read_csv(file_path)
    df.dropna(inplace=True)

    if all(col in df.columns for col in ['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']):
        df['Attack Time'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])
        df['Hour'] = df['Attack Time'].dt.hour
        df['DayOfWeek'] = df['Attack Time'].dt.dayofweek
    else:
        print("Some time columns are missing, skipping time-based analysis.")
        df['Hour'] = None
        df['DayOfWeek'] = None

    label_encoder = LabelEncoder()
    df['Browser'] = label_encoder.fit_transform(df['Browser'])
    df['Device/OS'] = label_encoder.fit_transform(df['Device/OS'])
    df['Traffic Type'] = label_encoder.fit_transform(df['Traffic Type'])
    df['Protocol'] = label_encoder.fit_transform(df['Protocol'])

    return df

def plot_feature_importance(rf_model, X):
    """
    Plot the feature importance to show which features had the biggest impact on the model.
    """
    feature_importance = rf_model.feature_importances_
    features = X.columns
    plt.figure(figsize=(10, 6))
    sns.barplot(x=feature_importance, y=features)
    plt.title('Feature Importance')
    plt.show()

def analyze_browser_os_correlation(df):
    """
    Analyze which browsers and operating systems are targeted more frequently by attack types.
    """
    plt.figure(figsize=(12, 6))
    sns.countplot(x='Browser', hue='Traffic Type', data=df, palette='Set3')
    plt.title('Attack Type Distribution by Browser')
    plt.xticks(rotation=45)
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.countplot(x='Device/OS', hue='Traffic Type', data=df, palette='Set3')
    plt.title('Attack Type Distribution by Operating System')
    plt.xticks(rotation=45)
    plt.show()

def train_random_forest(df):
    """
    Train a Random Forest model using the dataset and return the trained model
    along with the test set for evaluation.
    """
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    from time import time

    # Splitting data into features and target
    X = df[['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Browser', 'Device/OS']]
    y = df['Traffic Type']

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Scaling the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Initializing the Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Training the model
    start_time = time()
    rf_model.fit(X_train, y_train)
    training_time = time() - start_time
    print(f"\nTraining Time: {training_time} seconds")

    # Making predictions
    start_time = time()
    y_pred = rf_model.predict(X_test)
    prediction_time = time() - start_time
    print(f"Prediction Time: {prediction_time} seconds")

    return rf_model, X_test, y_test


def evaluate_model(rf_model, X_test, y_test, df):
    """
    Evaluate the Random Forest model and display performance metrics.
    """
    y_pred = rf_model.predict(X_test)
    print("Accuracy Score:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    conf_matrix = confusion_matrix(y_test, y_pred)
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title('Random Forest Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.show()

# def analyze_source_port_correlation(df):
#     """
#     Analyze how attack types are related to the source port using a heatmap.
#     """
#     port_vs_attack = pd.crosstab(df['Source Port'], df['Traffic Type'])
#     sns.heatmap(port_vs_attack, cmap="YlGnBu", annot=False)
#     plt.title('Heatmap: Source Port vs Attack Type')
#     plt.show()

def analyze_source_port_correlation(df, port_service_mapping):
    """
    Analyze how attack types are related to the source port using an interactive heatmap
    with hover data showing port number, traffic type, and frequency.
    
    Parameters:
    - df: DataFrame containing Source Port and Traffic Type.
    - port_service_mapping: Dictionary mapping port numbers to services (e.g., {80: 'HTTP'}).
    """
    # Create a crosstab of Source Port and Traffic Type
    port_vs_attack = pd.crosstab(df['Source Port'], df['Traffic Type'])

    # Check if the crosstab contains valid data
    if not port_vs_attack.empty:
        # Prepare data for hover with port, traffic type, and frequency
        hover_text = []
        for y_idx, port in enumerate(port_vs_attack.index):
            service = port_service_mapping.get(port, 'Unknown')  # Map port to service
            hover_text_row = []
            for x_idx, traffic_type in enumerate(port_vs_attack.columns):
                frequency = int(port_vs_attack.iloc[y_idx, x_idx])
                hover_text_row.append(
                    f"Port: {port} ({service})<br>Traffic Type: {traffic_type}<br>Frequency: {frequency}"
                )
            hover_text.append(hover_text_row)

        # Create the heatmap with hover text
        fig = go.Figure(
            data=go.Heatmap(
                z=port_vs_attack.values,
                x=port_vs_attack.columns,
                y=port_vs_attack.index,
                colorscale='YlGnBu',
                hoverongaps=False,
                text=hover_text,
                hoverinfo="text",  # Use text for hover data
            )
        )

        # Add titles and labels
        fig.update_layout(
            title='Interactive Heatmap: Source Port vs Traffic Type',
            xaxis=dict(title='Traffic Type', tickangle=45),
            yaxis=dict(title='Source Port', autorange='reversed'),  # Reverse for consistency with Seaborn
        )

        # Show the interactive heatmap
        fig.show()
    else:
        print("No data available for the heatmap.")


def analyze_attack_time_correlation(df):
    """
    Analyze how different attack types are distributed by time (hour of day and day of the week).
    """
    if df['Hour'].isnull().all():
        print("No time data available.")
        return

    plt.figure(figsize=(12, 6))
    sns.countplot(x='Hour', hue='Traffic Type', data=df, palette='Set2')
    plt.title('Attack Type Distribution by Hour of the Day')
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.countplot(x='DayOfWeek', hue='Traffic Type', data=df, palette='Set1')
    plt.title('Attack Type Distribution by Day of the Week')
    plt.xticks(rotation=45)
    plt.show()

def train_and_evaluate_deep_learning(df):
    """
    Train a deep learning model and measure its performance.
    """
    X = df[['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Browser', 'Device/OS']]
    y = df['Traffic Type']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    y_train_encoded = tf.keras.utils.to_categorical(y_train)
    y_test_encoded = tf.keras.utils.to_categorical(y_test)

    model = Sequential()
    model.add(Dense(128, activation='relu', input_shape=(X_train.shape[1],)))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(y_train_encoded.shape[1], activation='softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    start_time = time()
    model.fit(X_train, y_train_encoded, epochs=50, batch_size=32, verbose=1, validation_split=0.2)
    training_time = time() - start_time

    print(f"\nDeep Learning Training Time: {training_time:.2f} seconds")

    start_time = time()
    test_loss, test_accuracy = model.evaluate(X_test, y_test_encoded, verbose=0)
    prediction_time = time() - start_time

    print(f"Deep Learning Prediction Time: {prediction_time:.2f} seconds")
    print(f"Deep Learning Test Accuracy: {test_accuracy:.2f}")

    return model, test_accuracy


def train_and_evaluate_cnn(df):
    """
    Train and evaluate a CNN model on the dataset.
    """
    # Extract features and target
    X = df[['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Browser', 'Device/OS']]
    y = df['Traffic Type']

    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Reshape for CNN (samples, timesteps, features)
    X_train_cnn = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test_cnn = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # One-hot encode target variable
    y_train_encoded = tf.keras.utils.to_categorical(y_train)
    y_test_encoded = tf.keras.utils.to_categorical(y_test)

    # Build CNN model
    cnn_model = Sequential([
        Conv1D(64, kernel_size=2, activation='relu', input_shape=(X_train_cnn.shape[1], 1)),
        MaxPooling1D(pool_size=2),
        Dropout(0.5),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(y_train_encoded.shape[1], activation='softmax')  # Use 'softmax' for multiclass
    ])

    # Compile the model
    cnn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train the model
    print("\nTraining CNN Model...")
    start_time = time()
    history = cnn_model.fit(X_train_cnn, y_train_encoded, epochs=20, batch_size=32, validation_split=0.2, verbose=1)
    training_time = time() - start_time
    print(f"CNN Training Time: {training_time:.2f} seconds")

    # Evaluate the model
    print("\nEvaluating CNN Model...")
    start_time = time()
    loss, accuracy = cnn_model.evaluate(X_test_cnn, y_test_encoded, verbose=0)
    prediction_time = time() - start_time
    print(f"CNN Prediction Time: {prediction_time:.2f} seconds")
    print(f"CNN Test Accuracy: {accuracy:.2f}")

    # Plot training history
    def plot_training_history(history):
        """
        Plot the accuracy and loss during training.
        """
        plt.figure(figsize=(12, 6))

        # Accuracy
        plt.subplot(1, 2, 1)
        plt.plot(history.history['accuracy'], label='Train Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.title('CNN Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

        # Loss
        plt.subplot(1, 2, 2)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('CNN Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()

        plt.tight_layout()
        plt.show()

    plot_training_history(history)

    return cnn_model, accuracy



def main():
    """
    Run the analysis for the final project submission.
    """
    file_path = '/Users/cyberzed/Desktop/updated_cybersecurity_attacks.csv'

    # Define port-to-service mapping
    port_service_mapping = {
        80: 'HTTP',
        443: 'HTTPS',
        22: 'SSH',
        53: 'DNS',
        25: 'SMTP',
        3306: 'MySQL',
        110: 'POP3',
        143: 'IMAP',
    }

    df = load_and_preprocess_data(file_path)
    rf_model, X_test, y_test = train_random_forest(df)
    evaluate_model(rf_model, X_test, y_test, df)

    # Additional Graphs
    plot_feature_importance(rf_model, df[['Source Port', 'Destination Port', 'Packet Length', 'Protocol', 'Browser', 'Device/OS']])
    analyze_attack_time_correlation(df)
    analyze_source_port_correlation(df, port_service_mapping)
    analyze_browser_os_correlation(df)

    # Train and Evaluate Deep Learning Model
    dl_model, dl_accuracy = train_and_evaluate_deep_learning(df)

    # Train and Evaluate CNN Model
    cnn_model, cnn_accuracy = train_and_evaluate_cnn(df)

    print(f"\nComparison of Models:")
    print(f"Deep Learning Test Accuracy: {dl_accuracy:.2f}")
    print(f"CNN Test Accuracy: {cnn_accuracy:.2f}")

    print(f"\nEnd of Program!!!!!! \n END OF SEMESTER!!!!!!!!!! \n WHOSE NEXT LoL!?!?!?!?!?!?!?! JK <3 \n")

if __name__ == "__main__":
    main()
