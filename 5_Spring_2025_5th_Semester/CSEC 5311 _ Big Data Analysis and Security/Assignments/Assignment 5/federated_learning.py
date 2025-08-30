"""
Federated Learning on UCI Adult Census Income Dataset
This script simulates a Federated Learning setup using PyTorch where:
- Data is split non-IID among 5 clients
- Each client trains a logistic regression model locally
- A central server aggregates updates using FedAvg
- The global model is evaluated across communication rounds
"""

import pandas as pd
import numpy as np
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt

# Constants
NUM_CLIENTS = 5
NUM_ROUNDS = 20
EPOCHS = 5
BATCH_SIZE = 32
LR = 0.01

# Load and preprocess dataset
def load_preprocess_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    columns = [
        "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
        "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        "hours-per-week", "native-country", "income"
    ]
    df = pd.read_csv(url, header=None, names=columns, na_values=" ?", skipinitialspace=True)
    df.dropna(inplace=True)

    # Encode categorical features
    for col in df.select_dtypes(include='object').columns:
        df[col] = LabelEncoder().fit_transform(df[col])

    # Normalize all features
    df[df.columns] = StandardScaler().fit_transform(df[df.columns])

    X = df.drop("income", axis=1).values
    #y = df["income"].values
    y = (df["income"] > 0).astype(float).values

    return X, y

# Custom Dataset
class CensusDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# Non-IID data partitioning
def create_clients(X, y):
    sorted_idx = np.argsort(X[:, 3])  # Sort by 'education-num'
    X_sorted = X[sorted_idx]
    y_sorted = y[sorted_idx]
    split_size = len(X) // NUM_CLIENTS
    clients_X, clients_y = [], []
    for i in range(NUM_CLIENTS):
        start, end = i * split_size, (i + 1) * split_size if i < NUM_CLIENTS - 1 else len(X)
        clients_X.append(X_sorted[start:end])
        clients_y.append(y_sorted[start:end])
    return clients_X, clients_y

# Logistic Regression Model
class LogisticRegressionModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.linear = nn.Linear(input_dim, 1)

    def forward(self, x):
        return torch.sigmoid(self.linear(x))

# Train model locally
def train_local_model(model, dataloader, criterion, optimizer):
    model.train()
    for _ in range(EPOCHS):
        for X_batch, y_batch in dataloader:
            optimizer.zero_grad()
            output = model(X_batch)
            loss = criterion(output, y_batch)
            loss.backward()
            optimizer.step()
    return model.state_dict()

# Federated averaging
def average_weights(weights):
    avg_weights = {}
    for key in weights[0].keys():
        avg_weights[key] = sum(w[key] for w in weights) / len(weights)
    return avg_weights

# Evaluate global model
def evaluate_model(model, dataloader):
    model.eval()
    total_loss, correct, total = 0, 0, 0
    criterion = nn.BCELoss()
    with torch.no_grad():
        for X_batch, y_batch in dataloader:
            outputs = model(X_batch)
            preds = (outputs > 0.5).float()
            correct += (preds == y_batch).sum().item()
            total += y_batch.size(0)
            total_loss += criterion(outputs, y_batch).item()
    return correct / total, total_loss / len(dataloader)

# Federated learning routine
def run_federated_learning():
    X, y = load_preprocess_data()
    clients_X, clients_y = create_clients(X, y)
    test_X, test_y = X[:5000], y[:5000]
    test_loader = DataLoader(CensusDataset(test_X, test_y), batch_size=BATCH_SIZE)

    global_model = LogisticRegressionModel(X.shape[1])
    global_weights = global_model.state_dict()
    acc_list, loss_list = [], []

    for rnd in range(NUM_ROUNDS):
        local_weights = []
        for i in range(NUM_CLIENTS):
            model = LogisticRegressionModel(X.shape[1])
            model.load_state_dict(global_weights)
            loader = DataLoader(CensusDataset(clients_X[i], clients_y[i]), batch_size=BATCH_SIZE, shuffle=True)
            optimizer = torch.optim.SGD(model.parameters(), lr=LR)
            criterion = nn.BCELoss()
            local_weights.append(train_local_model(model, loader, criterion, optimizer))

        global_weights = average_weights(local_weights)
        global_model.load_state_dict(global_weights)
        acc, loss = evaluate_model(global_model, test_loader)
        acc_list.append(acc)
        loss_list.append(loss)
        print(f"Round {rnd+1}: Accuracy = {acc:.4f}, Loss = {loss:.4f}")

    # Plot Accuracy
    plt.figure()
    plt.plot(range(1, NUM_ROUNDS+1), acc_list, marker='o')
    plt.title("Global Model Accuracy vs Communication Rounds")
    plt.xlabel("Communication Rounds")
    plt.ylabel("Accuracy")
    plt.grid(True)
    plt.show()

    # Plot Loss
    plt.figure()
    plt.plot(range(1, NUM_ROUNDS+1), loss_list, marker='x')
    plt.title("Global Model Loss vs Communication Rounds")
    plt.xlabel("Communication Rounds")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_federated_learning()
