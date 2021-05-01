#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import time

from src.client import Client
from src.server import Server

SERVER = '192.168.1.17:9092'

if __name__ =='__main__':
    client = Client(
        dataset='mydata',
        groupid='groupid',
        model='model',
        server=SERVER
    )
    server = Server(
        n_clients=2,
        groupid='server',
        model='model',
        server=SERVER
    )
    server.initialize()
    #th1 = threading.Thread(target=client.run, daemon=True)
    #th1.start()
    #time.sleep(10)
    print('BYEBYE')
