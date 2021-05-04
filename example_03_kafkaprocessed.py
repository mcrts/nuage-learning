#!/usr/bin/env python
# -*- coding: utf-8 -*-
import multiprocessing
import time

import numpy as np
from sklearn.datasets import load_iris
from sklearn.utils import resample

from src.admin import Admin
from src.client import Client
from src.server import Server
from src.model import FederatedSGDClassifier
from src.utils import get_logger


LOGGER = get_logger('Example kafka process')
SERVER = 'Atlas:9092'


def run_client(idx, dst):
    """Instantiate and run a Client."""
    client = Client(
        dataset=dst,
        groupid=f'client.{idx:03d}',
        model=FederatedSGDClassifier(n_classes=3, n_features=4),
        server=SERVER
    )
    client.run()


def run_server(n_clients, loops):
    """Instantiate and run a Server."""
    server = Server(
        n_clients=n_clients,
        groupid='server.001',
        model=FederatedSGDClassifier(n_classes=3, n_features=4),
        server=SERVER,
        max_iter=loops,
    )
    server.initialize()
    server.run()
    LOGGER.info(server.current_metrics)


def run_example(n_clients, loops):
    """Run a Kafka-backed federated learning example.

    Use multiprocessing to isolate the server and clients'
    instantiation and running, so as to emulate behaviour
    of distinct participants to the training.

    n_clients : number of clients to spawn
    loops     : maximum number of iterations to train for
    """
    # Set up the Kafka backend topics.
    admin = Admin(server=SERVER)
    admin.setup_server()
    # Load the iris dataset and randomly cut it into bootstrapped subsplits.
    X, y = load_iris(return_X_y=True)
    X, y = resample(X, y, n_samples=n_clients * 100)
    datasets = list(zip(np.split(X, n_clients), np.split(y, n_clients)))
    # Instantiate processes wrapping the server and clients' code.
    processes = [
        multiprocessing.Process(target=run_server, args=(n_clients, loops))
    ]
    processes.extend([
        multiprocessing.Process(target=run_client, args=(idx, dst))
        for idx, dst in enumerate(datasets)
    ])
    # Run the processes parallelly and wait for them to resolve.
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()

if __name__ =='__main__':
    LOGGER.info('Running multiprocessed loop (10 steps) example')
    run_example(n_clients=10, loops=10)
