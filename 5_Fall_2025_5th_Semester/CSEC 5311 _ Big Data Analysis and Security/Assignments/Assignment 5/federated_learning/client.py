# client.py

"""
Implements the Flower client interface for federated training.
"""

import flwr as fl
import torch
import torch.nn as nn
import torch.optim as optim

class FLClient(fl.client.NumPyClient):
    def __init__(self, model, trainloader):
        self.model = model
        self.trainloader = trainloader
        self.criterion = nn.CrossEntropyLoss()
        self.optimizer = optim.SGD(self.model.parameters(), lr=0.01)

    def get_parameters(self):
        return [val.cpu().numpy() for val in self.model.state_dict().values()]

    def set_parameters(self, parameters):
        keys = list(self.model.state_dict().keys())
        state_dict = {k: torch.tensor(v) for k, v in zip(keys, parameters)}
        self.model.load_state_dict(state_dict, strict=True)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        self.model.train()
        for data, target in self.trainloader:
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = self.criterion(output, target)
            loss.backward()
            self.optimizer.step()
        return self.get_parameters(), len(self.trainloader.dataset), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        self.model.eval()
        correct, total_loss = 0, 0.0
        with torch.no_grad():
            for data, target in self.trainloader:
                output = self.model(data)
                total_loss += self.criterion(output, target).item()
                correct += (output.argmax(1) == target).sum().item()
        accuracy = correct / len(self.trainloader.dataset)
        return total_loss, len(self.trainloader.dataset), {"accuracy": accuracy}
