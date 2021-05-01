#!/usr/bin/env python 
# -*- coding: utf-8 -*-
import threading
import time

from src.client import Client

SERVER = '192.168.1.17:9092'

if __name__ =='__main__':
    client = Client(
        dataset='mydata',
        groupid='groupid',
        model='model',
        server=SERVER
    )

    th1 = threading.Thread(target=client.run, daemon=True)
    th1.start()
    time.sleep(10)
    print('BYEBYE')
