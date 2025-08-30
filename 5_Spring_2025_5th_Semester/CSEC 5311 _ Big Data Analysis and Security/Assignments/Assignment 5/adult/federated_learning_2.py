import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score

def load_and_preprocess_data(filepath):
    column_names = [
        "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
        "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
        "hours-per-week", "native-country", "income"
    ]
    data = pd.read_csv(filepath, header=None, names=column_names, na_values=" ?", skipinitialspace=True)
    data.dropna(inplace=True)

    for col in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])

    scaler = StandardScaler()
    for col in ["age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"]:
        data[col] = scaler.fit_transform(data[[col]]).flatten()

    return data

def split_data_non_iid(data):
    X = data.drop("income", axis=1).values
    y = data["income"].values
    age_bins = pd.qcut(data['age'], 5, labels=False, duplicates='drop')
    clients = [(X[age_bins == i], y[age_bins == i]) for i in range(5)]
    return clients, X, y

class LogisticRegressionModel(nn.Module):
    def __init__(self, input_dim):
        super(LogisticRegressionModel, self).__init__()
        self.linear = nn.Linear(input_dim, 1)

    def forward(self, x):
        return torch.sigmoid(self.linear(x))

def train_client(model, data_loader, criterion, optimizer, device):
    model.train()
    for X_batch, y_batch in data_loader:
        X_batch, y_batch = X_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)
        loss.backward()
        optimizer.step()

def evaluate_client(model, data_loader, device):
    model.eval()
    y_true, y_pred = [], []
    with torch.no_grad():
        for X_batch, y_batch in data_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            outputs = model(X_batch)
            y_true.extend(y_batch.cpu().numpy())
            y_pred.extend((outputs.cpu().numpy() > 0.5).astype(int))
    return accuracy_score(y_true, y_pred)

def federated_averaging(global_model, client_models):
    global_state_dict = global_model.state_dict()
    for key in global_state_dict.keys():
        global_state_dict[key] = torch.stack([client.state_dict()[key] for client in client_models], dim=0).mean(dim=0)
    global_model.load_state_dict(global_state_dict)

def main():
    #filepath = r"C:\Users\rubva\GitHub\MS-CSEC\5_Fall_2025_5th_Semester\CSEC 5311 _ Big Data Analysis and Security\Assignments\Assignment 5\adult"
    filepath = os.path.join(os.path.dirname(__file__), "adult.data")


    print("[*] Loading and preprocessing data...")
    data = load_and_preprocess_data(filepath)

    print("[*] Creating client splits...")
    clients_data, X, y = split_data_non_iid(data)
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    X_test = torch.tensor(X_test, dtype=torch.float32)
    y_test = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

    input_dim = X.shape[1]
    global_model = LogisticRegressionModel(input_dim)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    global_model.to(device)

    num_rounds = 10
    num_clients = len(clients_data)
    client_models = [LogisticRegressionModel(input_dim).to(device) for _ in range(num_clients)]
    criterion = nn.BCELoss()

    global_accuracies = []
    global_losses = []
    client_accuracies_per_round = {i: [] for i in range(num_clients)}

    for round_num in range(num_rounds):
        print(f"[*] Federated learning round {round_num + 1}/{num_rounds}")

        for client_idx, (X_client, y_client) in enumerate(clients_data):
            X_client = torch.tensor(X_client, dtype=torch.float32)
            y_client = torch.tensor(y_client, dtype=torch.float32).unsqueeze(1)
            data_loader = torch.utils.data.DataLoader(
                dataset=torch.utils.data.TensorDataset(X_client, y_client),
                batch_size=32,
                shuffle=True
            )
            client_model = client_models[client_idx]
            client_model.load_state_dict(global_model.state_dict())
            optimizer = optim.SGD(client_model.parameters(), lr=0.01)
            train_client(client_model, data_loader, criterion, optimizer, device)

        federated_averaging(global_model, client_models)

        test_loader = torch.utils.data.DataLoader(
            dataset=torch.utils.data.TensorDataset(X_test, y_test),
            batch_size=32,
            shuffle=False
        )

        global_model.eval()
        losses = []
        with torch.no_grad():
            for X_batch, y_batch in test_loader:
                X_batch, y_batch = X_batch.to(device), y_batch.to(device)
                outputs = global_model(X_batch)
                loss = criterion(outputs, y_batch)
                losses.append(loss.item())

        avg_loss = np.mean(losses)
        accuracy = evaluate_client(global_model, test_loader, device)
        global_accuracies.append(accuracy)
        global_losses.append(avg_loss)

        for i, (X_client, y_client) in enumerate(clients_data):
            X_client = torch.tensor(X_client, dtype=torch.float32)
            y_client = torch.tensor(y_client, dtype=torch.float32).unsqueeze(1)
            loader = torch.utils.data.DataLoader(
                dataset=torch.utils.data.TensorDataset(X_client, y_client),
                batch_size=32,
                shuffle=False
            )
            client_accuracy = evaluate_client(global_model, loader, device)
            client_accuracies_per_round[i].append(client_accuracy)

    # Plot Accuracy vs Communication Rounds
    plt.figure()
    plt.plot(global_accuracies, marker='o')
    plt.title("Global Model Accuracy vs Communication Rounds")
    plt.xlabel("Communication Round")
    plt.ylabel("Accuracy")
    plt.grid(True)
    plt.savefig("accuracy_vs_rounds.png")

    # Plot Loss vs Communication Rounds
    plt.figure()
    plt.plot(global_losses, marker='o')
    plt.title("Global Model Loss vs Communication Rounds")
    plt.xlabel("Communication Round")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.savefig("loss_vs_rounds.png")

    # Save client accuracy table
    rounds = list(range(1, num_rounds + 1))
    df_client = pd.DataFrame({f"Client {i+1}": accs for i, accs in client_accuracies_per_round.items()}, index=rounds)
    df_client.to_csv("client_accuracy_per_round.csv", index_label="Round")
    print("[*] Results saved: accuracy_vs_rounds.png, loss_vs_rounds.png, client_accuracy_per_round.csv")

if __name__ == "__main__":
    main()
