#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from src.model import FederatedSGDClassifier
from src.utils import get_logger
from sklearn.datasets import load_iris
from sklearn.utils import resample

LOGGER = get_logger('Example many SGDs')

N = 10
def step_example():
    X, y = load_iris(return_X_y=True)
    X, y = resample(X, y, n_samples=N * 100)
    datasets = list(zip(np.split(X, N), np.split(y, N)))

    server = FederatedSGDClassifier(n_classes=3, n_features=4)
    clients = [FederatedSGDClassifier(n_classes=3, n_features=4) for _ in range(N)]

    # Initialize SGDs
    for c, (Xi, yi) in zip(clients, datasets):
        c.set_weights(c.generate_weights())
        c.run_training_epoch(Xi, yi)

    # Train clients SGDs
    for c, (Xi, yi) in zip(clients, datasets):
        c.run_training_epoch(Xi, yi)

    # Aggregate clients metrics
    clients_metrics = [c.evaluate(Xi, yi) for c, (Xi, yi) in zip(clients, datasets)]

    metrics = server.aggregate_metrics(clients_metrics)
    LOGGER.info(metrics)

    # Aggregate clients weights
    clients_weights = [c.get_weights() for c in clients]
    clients_sizes = [len(d) for d in datasets]
    weights = server.aggregate_weights(clients_sizes, clients_weights)
    for c in clients:
        c.set_weights(weights)


def loop_example(loops=100):
    X, y = load_iris(return_X_y=True)
    X, y = resample(X, y, n_samples=N * 100)
    datasets = list(zip(np.split(X, N), np.split(y, N)))

    server = FederatedSGDClassifier(n_classes=3, n_features=4)
    clients = [FederatedSGDClassifier(n_classes=3, n_features=4) for _ in range(N)]

    # Initialize SGDs
    for c, (Xi, yi) in zip(clients, datasets):
        c.set_weights(c.generate_weights())
        c.run_training_epoch(Xi, yi)

    for _ in range(loops):
        # Train clients SGDs
        for c, (Xi, yi) in zip(clients, datasets):
            c.run_training_epoch(Xi, yi)

        # Aggregate clients metrics
        clients_metrics = [c.evaluate(Xi, yi) for c, (Xi, yi) in zip(clients, datasets)]

        metrics = server.aggregate_metrics(clients_metrics)
        LOGGER.info(metrics)

        # Aggregate clients weights
        clients_weights = [c.get_weights() for c in clients]
        clients_sizes = [len(d) for d in datasets]
        weights = server.aggregate_weights(clients_sizes, clients_weights)
        for c in clients:
            c.set_weights(weights)
    

if __name__ =='__main__':
    LOGGER.info('Running one step example')
    step_example()
    LOGGER.info('Running loop (100 steps) example')
    loop_example()
