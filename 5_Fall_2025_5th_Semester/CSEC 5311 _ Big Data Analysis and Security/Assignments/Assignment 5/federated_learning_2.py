import os
import pandas as pd
import numpy as np
import flwr as fl
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load and preprocess dataset
def load_and_preprocess_data(filepath):
    column_names = [
        "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
        "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        "hours-per-week", "native-country", "income"
    ]
    data = pd.read_csv(filepath, header=None, names=column_names, na_values=" ?", skipinitialspace=True)
    data.dropna(inplace=True)

    # Encode categorical features
    for col in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])

    # Normalize numeric features
    scaler = StandardScaler()
    for col in ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]:
        data[col] = scaler.fit_transform(data[[col]])

    return data

# Create 5 non-IID clients by age groups
def split_data_non_iid(data):
    X = data.drop("income", axis=1)
    y = data["income"]
    age_bins = pd.qcut(data['age'], 5, labels=False)
    clients = [(X[age_bins == i], y[age_bins == i]) for i in range(5)]
    return clients, X, y

# Define Flower client
class SklearnClient(fl.client.NumPyClient):
    def __init__(self, X_train, y_train, X_test, y_test):
        self.model = LogisticRegression(max_iter=100)
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

    def get_parameters(self, config):
        self.model.fit(self.X_train, self.y_train)
        return [self.model.coef_, self.model.intercept_]

    def fit(self, parameters, config):
        self.model.coef_, self.model.intercept_ = parameters
        self.model.fit(self.X_train, self.y_train)
        return [self.model.coef_, self.model.intercept_], len(self.X_train), {}

    def evaluate(self, parameters, config):
        self.model.coef_, self.model.intercept_ = parameters
        preds = self.model.predict(self.X_test)
        probas = self.model.predict_proba(self.X_test)
        acc = accuracy_score(self.y_test, preds)
        loss = log_loss(self.y_test, probas)
        return loss, len(self.X_test), {"accuracy": acc}

# Run Flower federated simulation
def run_flower_simulation(clients_data, X_test, y_test, num_rounds=10):
    clients = [SklearnClient(X, y, X_test, y_test) for X, y in clients_data]
    fl.simulation.start_simulation(
        client_fn=lambda cid: clients[int(cid)],
        num_clients=len(clients),
        config=fl.server.ServerConfig(num_rounds=num_rounds),
    )

# Main function
# def main():
#     # ✅ Customize this path to wherever your adult.data file lives
#     data_dir = "CSEC 5311 _ Big Data Analysis and Security/Assignments/Assignment 5/adult"
#     filepath = os.path.join(data_dir, "adult.data")

#     print("[*] Loading and preprocessing data...")
#     data = load_and_preprocess_data(filepath)

#     print("[*] Creating client splits...")
#     clients_data, X, y = split_data_non_iid(data)
#     _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     print("[*] Starting federated learning simulation with Flower...")
#     run_flower_simulation(clients_data, X_test, y_test, num_rounds=10)



def main():
    # Absolute path to where adult.data is stored
    data_dir = r"C:\Users\rubva\GitHub\MS-CSEC\5_Fall_2025_5th_Semester\CSEC 5311 _ Big Data Analysis and Security\Assignments\Assignment 5\adult"
    filepath = os.path.join(data_dir, "adult.data")

    print("[*] Loading and preprocessing data...")
    data = load_and_preprocess_data(filepath)

    print("[*] Creating client splits...")
    clients_data, X, y = split_data_non_iid(data)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("[*] Starting federated learning simulation with Flower...")
    run_flower_simulation(clients_data, X_test, y_test, num_rounds=10)




if __name__ == "__main__":
    main()
