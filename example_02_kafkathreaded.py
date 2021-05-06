#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
import numpy as np

from nuagelearning.admin import Admin
from nuagelearning.client import Client
from nuagelearning.server import Server
from nuagelearning.model import FederatedSGDClassifier
from nuagelearning.utils import get_logger

from sklearn.datasets import load_iris
from sklearn.utils import resample


LOGGER = get_logger('Example kafka thread')
SERVER = 'localhost:9092'

def step_example(n_clients=2):
    admin = Admin(server=SERVER)
    admin.setup_server()

    X, y = load_iris(return_X_y=True)
    X, y = resample(X, y, n_samples=n_clients * 100)
    datasets = list(zip(np.split(X, n_clients), np.split(y, n_clients)))

    # Initialize Clients
    clients = [
        Client(
            dataset=d,
            groupid=f'client.{i:03d}',
            model=FederatedSGDClassifier(n_classes=3, n_features=4),
            server=SERVER
        )
        for i, d in zip(range(n_clients), datasets)
    ]

    # Initialize Server
    server = Server(
        n_clients=n_clients,
        groupid='server.001',
        model=FederatedSGDClassifier(n_classes=3, n_features=4),
        server=SERVER
    )
    server.initialize()
    time.sleep(1)

    # We do 2 loops to get an update on the metrics
    for c in clients:
        c.run_once()

    server.run_once()
    LOGGER.info(server.current_metrics)

    for c in clients:
        c.run_once()

    server.run_once()
    LOGGER.info(server.current_metrics)


def loop_example(loops=10, n_clients=10):
    #admin = Admin(server=SERVER)
    #admin.setup_server()

    X, y = load_iris(return_X_y=True)
    X, y = resample(X, y, n_samples=n_clients * 100)
    datasets = list(zip(np.split(X, n_clients), np.split(y, n_clients)))

    # Initialize Clients
    clients = [
        Client(
            dataset=d,
            groupid=f'client.{i:03d}',
            model=FederatedSGDClassifier(n_classes=3, n_features=4),
            server=SERVER
        )
        for i, d in zip(range(n_clients), datasets)
    ]

    # Initialize Server
    server = Server(
        n_clients=len(clients),
        groupid='server.001',
        model=FederatedSGDClassifier(n_classes=3, n_features=4),
        server=SERVER,
        max_iter=loops,
    )
    server.initialize()
    time.sleep(1)

    # Running the clients and server in threads
    threads = [
        threading.Thread(target=server.run, daemon=False)
    ]
    for c in clients:
        threads.append(threading.Thread(target=c.run, daemon=False))

    for th in threads:
        th.start()
    
    for th in threads:
        th.join()

    LOGGER.info(server.current_metrics)


if __name__ =='__main__':
    #LOGGER.info('Running one step example')
    #step_example()
    LOGGER.info('Running loop (10 steps) example')
    loop_example(loops=10, n_clients=100)
