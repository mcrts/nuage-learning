# -*- coding: utf-8 -*-
import numpy as np

from src.model import FederatedSGDClassifier
from sklearn.datasets import load_iris
from sklearn.utils import resample, shuffle


def local_example(n_clients=3, sample_size=50, loops=200, eta0=0.1, replace=False):
    X, y = load_iris(return_X_y=True)
    X, y = resample(X, y, n_samples=n_clients * sample_size, replace=replace)
    datasets = list(zip(np.split(X, n_clients), np.split(y, n_clients)))

    server = FederatedSGDClassifier(n_classes=3, n_features=4, learning_rate="invscaling", eta0=eta0)
    clients = [FederatedSGDClassifier(n_classes=3, n_features=4, learning_rate="invscaling", eta0=eta0) for _ in range(n_clients)]

    # Initialize SGDs
    for c, (Xi, yi) in zip(clients, datasets):
        c.set_weights(c.generate_weights())
        c.run_training_epoch(Xi, yi)


    aggregated_metrics = []
    individual_metrics = []
    for _ in range(loops):
        # Train clients SGDs
        for c, (Xi, yi) in zip(clients, datasets):
            c.run_training_epoch(Xi, yi)

        # Aggregate clients metrics
        clients_metrics = [c.evaluate(Xi, yi) for c, (Xi, yi) in zip(clients, datasets)]
        individual_metrics.append([(m['accuracy'], m['logloss']) for m in clients_metrics])


        metrics = server.aggregate_metrics(clients_metrics)
        aggregated_metrics.append((metrics['accuracy'], metrics['logloss']))   

        # Aggregate clients weights
        clients_weights = [c.get_weights() for c in clients]
        clients_sizes = [len(d) for d in datasets]
        weights = server.aggregate_weights(clients_sizes, clients_weights)
        for c in clients:
            c.set_weights(weights)

    return aggregated_metrics, individual_metrics