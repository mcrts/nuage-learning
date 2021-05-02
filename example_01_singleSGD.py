#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from src.model import FederatedSGDClassifier
from src.utils import get_logger
from sklearn.datasets import load_iris

LOGGER = get_logger('Example Single SGD')


def step_example():
    X, y = load_iris(return_X_y=True)
    sgd = FederatedSGDClassifier(n_classes=3, n_features=4)

    # Initialize SGD
    sgd.set_weights(sgd.generate_weights())
    # Train SGD
    sgd.run_training_epoch(X, y)
    # Evaluate SGD
    metrics = sgd.evaluate(X, y)
    LOGGER.info(metrics)


def loop_example(loops=100):
    X, y = load_iris(return_X_y=True)
    sgd = FederatedSGDClassifier(n_classes=3, n_features=4)

    # Initialize SGD
    sgd.set_weights(sgd.generate_weights())
    for _ in range(loops):
        # Train SGD
        sgd.run_training_epoch(X, y)
        # Evaluate SGD
        metrics = sgd.evaluate(X, y)
        LOGGER.info(metrics)


if __name__ =='__main__':
    LOGGER.info('Running one step example')
    step_example()
    LOGGER.info('Running loop (100 steps) example')
    loop_example()
