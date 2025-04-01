#main.py

"""
Entry point for running the federated learning simulation using Flower.
"""

import flwr as fl
from data_loader import CensusDataLoader
from model import LogisticRegression
from client import FLClient

class FederatedLearningProgram:
    def __init__(self):
        self.data_loader = CensusDataLoader()

    def run(self):
        X, y = self.data_loader.load_and_preprocess()
        clients_data = self.data_loader.partition_data(X, y)

        def client_fn(cid):
            model = LogisticRegression(X.shape[1])
            return FLClient(model, clients_data[int(cid)])

        strategy = fl.server.strategy.FedAvg()

        fl.simulation.start_simulation(
            client_fn=client_fn,
            num_clients=5,
            config=fl.server.ServerConfig(num_rounds=10),
            strategy=strategy,
        )

if __name__ == "__main__":
    FederatedLearningProgram().run()
