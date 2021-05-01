#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time
import numpy as np

from src.client import Client
from src.server import Server
from src.model import FederatedSGDClassifier

from sklearn.datasets import load_iris


SERVER = 'Atlas:9092'

if __name__ =='__main__':
    data = load_iris(return_X_y=True)
    model1 = FederatedSGDClassifier(n_classes=3, n_features=4)
    model2 = FederatedSGDClassifier(n_classes=3, n_features=4)
    client = Client(
        dataset=data,
        groupid='client.001',
        model=model1,
        server=SERVER
    )
    
    server = Server(
        n_clients=1,
        groupid='server.001',
        model=model2,
        server=SERVER
    )
    server.initialize()
    client.run()

    #th1 = threading.Thread(target=client.run, daemon=True)
    #th1.start()
    #time.sleep(10)
    print('BYEBYE')
