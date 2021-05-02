#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from src.model import FederatedSGDClassifier
from src.utils import get_logger
from sklearn.datasets import load_iris

LOGGER = get_logger('Example Two SGDs')


def step_example():
    X, y = load_iris(return_X_y=True)
    client = FederatedSGDClassifier(n_classes=3, n_features=4)
    server = FederatedSGDClassifier(n_classes=3, n_features=4)

    # Initialize SGDs
    client.set_weights(client.generate_weights())
    server.set_weights(server.generate_weights())
    # TODO: one training epoch needs to be run to set "classes_" on SGD otherwise set_weights does not work
    # TODO: this should be fixed
    client.run_training_epoch(X, y)
    server.run_training_epoch(X, y)

    # Train client SGD
    client.run_training_epoch(X, y)

    # Set server SGD weights with client SGD wieghts
    server.set_weights(client.get_weights())

    # Evaluate server SGD
    metrics = server.evaluate(X, y)
    LOGGER.info(metrics)

    # Metrics from server and client SGD should be the same
    LOGGER.info("Sanity check : Server and Client SGDs evaluation should return the same metrics : {}".format(server.evaluate(X, y) == client.evaluate(X, y)))


def loop_example(loops=100):
    X, y = load_iris(return_X_y=True)
    client = FederatedSGDClassifier(n_classes=3, n_features=4)
    server = FederatedSGDClassifier(n_classes=3, n_features=4)

    # Initialize SGDs
    client.set_weights(client.generate_weights())
    server.set_weights(server.generate_weights())
    # TODO: one training epoch needs to be run to set "classes_" on SGD otherwise set_weights does not work
    # TODO: this should be fixed
    client.run_training_epoch(X, y)
    server.run_training_epoch(X, y)


    for _ in range(loops):
        # Train client SGD
        client.run_training_epoch(X, y)

        # Set server SGD weights with client SGD wieghts
        server.set_weights(client.get_weights())

        # Evaluate server SGD
        metrics = server.evaluate(X, y)
        LOGGER.info(metrics)
    
    # Metrics from server and client SGD should be the same
    LOGGER.info("Sanity check : Server and Client SGDs evaluation should return the same metrics : {}".format(server.evaluate(X, y) == client.evaluate(X, y)))
    

if __name__ =='__main__':
    LOGGER.info('Running one step example')
    step_example()
    LOGGER.info('Running loop (100 steps) example')
    loop_example()
