"""
Federated Learning on US Census Income Dataset (UCI)
Author: Ruben Valdez
Course: CSEC 5311 / CETE 4392
Spring 2025

This script loads and preprocesses the US Census Income dataset,
implements Federated Learning with 5 clients (non-IID split), trains a
simple neural network model, and plots performance graphs.
"""

import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt

def load_and_preprocess_data():
    """Downloads and preprocesses the US Census Income dataset."""
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    column_names = [
        "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
        "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        "hours-per-week", "native-country", "income"
    ]
    data = pd.read_csv(url, header=None, names=column_names, na_values=" ?", skipinitialspace=True)
    data.dropna(inplace=True)

    label_encoders = {}
    for col in data.select_dtypes(include="object").columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        label_encoders[col] = le

    X = data.drop("income", axis=1)
    y = data["income"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    full_df = pd.DataFrame(X_scaled, columns=X.columns)
    full_df["income"] = y.values
    return full_df, X_scaled, y

def split_data_non_iid(full_df):
    """Splits the data into 5 clients using non-IID distribution based on education level."""
    client_data = {}
    grouped = full_df.groupby(pd.qcut(full_df["education-num"], 5, labels=False, duplicates='drop'))
    for i in range(5):
        if i in grouped.groups:
            client_data[i] = grouped.get_group(i).reset_index(drop=True)
    return client_data

def create_dataloaders(client_data):
    """Creates PyTorch DataLoaders for each client."""
    loaders = []
    for i in range(len(client_data)):
        X_tensor = torch.tensor(client_data[i].drop("income", axis=1).values, dtype=torch.float32)
        y_tensor = torch.tensor(client_data[i]["income"].values, dtype=torch.long)
        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(dataset, batch_size=32, shuffle=True)
        loaders.append(loader)
    return loaders

class SimpleNN(nn.Module):
    """Simple neural network model for binary classification."""
    def __init__(self, input_dim):
        super(SimpleNN, self).__init__()
        self.layer = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 2)
        )

    def forward(self, x):
        return self.layer(x)

def train_local(model, loader, criterion, optimizer, epochs=1):
    """Trains model locally on one client."""
    model.train()
    for _ in range(epochs):
        for x_batch, y_batch in loader:
            optimizer.zero_grad()
            output = model(x_batch)
            loss = criterion(output, y_batch)
            loss.backward()
            optimizer.step()
    return model.state_dict()

def average_models(global_model, local_models):
    """Performs Federated Averaging on client models."""
    global_dict = global_model.state_dict()
    for k in global_dict.keys():
        global_dict[k] = torch.stack([local_model[k].float() for local_model in local_models], 0).mean(0)
    global_model.load_state_dict(global_dict)
    return global_model

def evaluate_model(model, X_test_tensor, y_test_tensor, criterion):
    """Evaluates model on test data."""
    model.eval()
    with torch.no_grad():
        outputs = model(X_test_tensor)
        loss = criterion(outputs, y_test_tensor).item()
        pred = torch.argmax(outputs, 1)
        acc = (pred == y_test_tensor).sum().item() / len(y_test_tensor)
    return acc, loss

def plot_results(acc_history, loss_history):
    """Plots accuracy and loss over communication rounds."""
    plt.figure()
    plt.plot(range(1, len(acc_history)+1), acc_history, marker='o')
    plt.xlabel("Communication Rounds")
    plt.ylabel("Global Model Accuracy")
    plt.title("Global Model Accuracy vs Communication Rounds")
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(range(1, len(loss_history)+1), loss_history, marker='o', color='red')
    plt.xlabel("Communication Rounds")
    plt.ylabel("Global Model Loss")
    plt.title("Global Model Loss vs Communication Rounds")
    plt.grid(True)
    plt.show()

def main():
    """Main function to execute Federated Learning process."""
    full_df, X_scaled, y = load_and_preprocess_data()
    client_data = split_data_non_iid(full_df)
    client_loaders = create_dataloaders(client_data)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.long)

    input_dim = X_test.shape[1]
    global_model = SimpleNN(input_dim)
    criterion = nn.CrossEntropyLoss()

    rounds = 20
    acc_history = []
    loss_history = []

    for rnd in range(rounds):
        local_models = []
        for loader in client_loaders:
            model = SimpleNN(input_dim)
            model.load_state_dict(global_model.state_dict())
            optimizer = optim.SGD(model.parameters(), lr=0.01)
            local_state = train_local(model, loader, criterion, optimizer)
            local_models.append(local_state)

        global_model = average_models(global_model, local_models)
        acc, loss = evaluate_model(global_model, X_test_tensor, y_test_tensor, criterion)
        acc_history.append(acc)
        loss_history.append(loss)
        print(f"Round {rnd+1}: Accuracy = {acc:.4f}, Loss = {loss:.4f}")

    plot_results(acc_history, loss_history)

if __name__ == "__main__":
    main()
