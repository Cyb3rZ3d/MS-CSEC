#data_loader.py

"""
Handles dataset download, preprocessing, and partitioning for federated learning.

Uses the US Census Income dataset (also known as the Adult dataset) from the UCI repository.
"""

import pandas as pd
import torch
from sklearn.preprocessing import LabelEncoder, StandardScaler
from torch.utils.data import TensorDataset, DataLoader

class CensusDataLoader:
    def __init__(self):
        self.column_names = [
            "age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
            "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss",
            "hours-per-week", "native-country", "income"
        ]

    def load_and_preprocess(self):
        """
        Downloads and preprocesses the US Census Income dataset:
        - Handles missing values
        - Encodes categorical variables
        - Normalizes features

        Returns:
            X (np.ndarray): Features
            y (pd.Series): Labels
        """
        df = pd.read_csv(
            "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data",
            header=None, names=self.column_names, na_values=" ?"
        )
        df.dropna(inplace=True)

        for col in df.select_dtypes(include=["object"]).columns:
            if col != "income":
                df[col] = LabelEncoder().fit_transform(df[col])

        df["income"] = df["income"].apply(lambda x: 1 if ">50K" in x else 0)

        X = df.drop("income", axis=1)
        y = df["income"]

        X = StandardScaler().fit_transform(X)
        return X, y

    def partition_data(self, X, y):
        """
        Partitions data into 5 non-IID clients based on age groups.

        Returns:
            dict: Client ID to DataLoader mapping
        """
        clients_data = {}
        df = pd.DataFrame(X)
        df["target"] = y
        df["age_group"] = pd.cut(df[0], bins=[0, 30, 40, 50, 60, 100], labels=[0, 1, 2, 3, 4])

        for i in range(5):
            group = df[df["age_group"] == i]
            X_client = group.drop(["target", "age_group"], axis=1).values
            y_client = group["target"].values
            tx = torch.tensor(X_client, dtype=torch.float32)
            ty = torch.tensor(y_client, dtype=torch.long)
            loader = DataLoader(TensorDataset(tx, ty), batch_size=32, shuffle=True)
            clients_data[i] = loader

        return clients_data
