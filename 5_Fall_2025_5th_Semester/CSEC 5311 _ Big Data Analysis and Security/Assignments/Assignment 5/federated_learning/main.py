# main.py

import flwr as fl
import matplotlib.pyplot as plt
from data_loader import CensusDataLoader
from model import LogisticRegression
from client import FLClient
import torch

class FederatedLearningProgram:
    def __init__(self):
        self.data_loader = CensusDataLoader()
        self.accuracy_list = []
        self.loss_list = []

    def evaluate_global_model(self, model, testloader):
        model.eval()
        correct, total_loss = 0, 0.0
        criterion = torch.nn.CrossEntropyLoss()
        with torch.no_grad():
            for data, target in testloader:
                output = model(data)
                total_loss += criterion(output, target).item()
                correct += (output.argmax(1) == target).sum().item()
        accuracy = correct / len(testloader.dataset)
        return total_loss, accuracy

    def run(self):
        X, y = self.data_loader.load_and_preprocess()
        clients_data = self.data_loader.partition_data(X, y)
        testloader = self.data_loader.create_testloader(X, y)

        def client_fn(cid):
            model = LogisticRegression(X.shape[1])
            return FLClient(model, clients_data[int(cid)])

        class CustomFedAvg(fl.server.strategy.FedAvg):
            def aggregate_fit(self, rnd, results, failures):
                aggregated_params, _ = super().aggregate_fit(rnd, results, failures)
                model = LogisticRegression(X.shape[1])
                if aggregated_params is not None:
                    params_dict = zip(model.state_dict().keys(), aggregated_params)
                    state_dict = {k: torch.tensor(v) for k, v in params_dict}
                    model.load_state_dict(state_dict, strict=True)
                    loss, acc = flp.evaluate_global_model(model, testloader)
                    flp.loss_list.append(loss)
                    flp.accuracy_list.append(acc)
                    print(f"Round {rnd} - Global Loss: {loss:.4f}, Accuracy: {acc:.4f}")
                return aggregated_params, {}

        flp = self
        strategy = CustomFedAvg()

        fl.simulation.start_simulation(
            client_fn=client_fn,
            num_clients=5,
            config=fl.server.ServerConfig(num_rounds=10),
            strategy=strategy,
        )

        # Plot graphs
        rounds = list(range(1, 11))
        plt.figure()
        plt.plot(rounds, self.accuracy_list, marker='o')
        plt.title("Global Model Accuracy vs. Communication Rounds")
        plt.xlabel("Rounds")
        plt.ylabel("Accuracy")
        plt.savefig("accuracy_vs_rounds.png")

        plt.figure()
        plt.plot(rounds, self.loss_list, marker='o')
        plt.title("Global Model Loss vs. Communication Rounds")
        plt.xlabel("Rounds")
        plt.ylabel("Loss")
        plt.savefig("loss_vs_rounds.png")

if __name__ == "__main__":
    FederatedLearningProgram().run()
