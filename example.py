#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
import numpy as np

from src.admin import Admin
from src.client import Client
from src.server import Server
from src.model import FederatedSGDClassifier
from src.utils import logger

from sklearn.datasets import load_iris
from sklearn.utils import shuffle, resample


SERVER = 'Atlas:9092'
N = 40

if __name__ =='__main__':
    admin = Admin(server=SERVER)
    admin.setup_server()

    X, y = load_iris(return_X_y=True)
    X, y = resample(X, y, n_samples=2000)
    datas = zip(np.split(X, N), np.split(y, N))
    clients = []
    for i, d in zip(range(1, N+1), datas):
        c = Client(
            dataset=d,
            groupid=f'client.{i:03d}',
            model=FederatedSGDClassifier(n_classes=3, n_features=4),
            server=SERVER
        )
        clients.append(c)

    server = Server(
        n_clients=N,
        groupid='server.001',
        model=FederatedSGDClassifier(n_classes=3, n_features=4),
        server=SERVER
    )

    server.initialize()
    time.sleep(1)


    threads = [
        threading.Thread(target=server.run, daemon=True)
    ]
    for c in clients:
        threads.append(threading.Thread(target=c.run, daemon=True))

    for th in threads:
        th.start()

    time.sleep(320)

    print()
    print('BYEBYE')
