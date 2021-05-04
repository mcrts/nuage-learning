#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

from src.utils import get_logger, deserialize_payload
from confluent_kafka import Consumer

from examples import local_example

LOGGER = get_logger('Example kafka analytics')
SERVER = 'Atlas:9092'


def get_messages(consumer):
    keep_running = True
    while keep_running:
        msg = consumer.poll(2.0)
        if msg == None:
            keep_running = False
            raise StopIteration
        else:
            yield deserialize_payload(msg.value().decode('utf-8'))

def reset_offset(consumer, partitions):
    for p in partitions:
        o, _ = consumer.get_watermark_offsets(p)
        p.offset = o
    consumer.commit(offsets=partitions)

def analytics():
    c = Consumer({
            'bootstrap.servers': SERVER,
            'group.id': 'analytics',
            'auto.offset.reset': 'earliest'
        })

    c.subscribe(['server'], on_assign=reset_offset)
    metrics = {
        'accuracy': np.ndarray(shape=(0, 2), dtype=np.float64),
        'logloss': np.ndarray(shape=(0, 2), dtype=np.float64)
    }
    for msg in get_messages(c):
        epoch = msg['epoch']
        if epoch > 1:
            acc = msg['metrics']['accuracy']
            loss = msg['metrics']['logloss']
            metrics['accuracy'] = np.append(metrics['accuracy'], np.array([[epoch, acc]]), axis=0)
            metrics['logloss'] = np.append(metrics['logloss'], np.array([[epoch, loss]]), axis=0)

    LOGGER.info(metrics['accuracy'][1,:])
    c.close()

    acc = [x[1] for x in sorted(metrics['accuracy'], key=lambda x: x[0])]
    loss = [x[1] for x in sorted(metrics['logloss'], key=lambda x: x[0])]
    epoch = sorted(metrics['accuracy'][:, 0])
    plt.figure()
    plt.plot(epoch, acc, label='accuracy')
    plt.show()

    plt.figure()
    plt.plot(epoch, loss, label='loss')
    plt.show()


def analytics_local(n_clients=3, sample_size=50, loops=200, eta0=0.1, replace=False):
    agg_metrics, ind_metrics = local_example(n_clients, sample_size, loops, eta0, replace)
    agg_metrics = np.array(agg_metrics)
    ind_metrics = np.array(ind_metrics)

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy', color='tab:blue')
    ax1.plot(range(loops), agg_metrics[:,0], color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('sin', color='tab:red')  # we already handled the x-label with ax1
    ax2.plot(range(loops), agg_metrics[:,1],  color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    for i in range(n_clients):
        ax1.plot(range(loops), ind_metrics[:,i,0], linestyle='dashed', color='tab:blue', alpha=0.5)
        ax2.plot(range(loops), ind_metrics[:,i,1], linestyle='dashed', color='tab:red', alpha=0.5)



    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


if __name__ =='__main__':
    LOGGER.info('Running analytics')
    analytics_local(n_clients=3, sample_size=100, loops=200, eta0=0.05, replace=True)
