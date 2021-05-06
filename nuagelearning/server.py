# coding: utf-8

"""Server class."""

import time

import numpy as np
from confluent_kafka import Consumer, Producer

from nuagelearning.utils import deserialize_payload, serialize_payload, logger


class Server:
    """Server class."""

    readtopic = "clients"
    sendtopic = "server"
    session_time_out = 6000

    def __init__(self, n_clients, groupid, model, server, max_iter=100):
        """Instantiate the Server."""
        self.n_clients = n_clients
        self.groupid = groupid
        self.model = model
        self.server = server
        self.max_iter = max_iter
        self.current_metrics = None

    def get_consumer(self, topics):
        """Set up and return a Kafka consumer for given topics."""
        c = Consumer({
            'bootstrap.servers': self.server,
            'group.id': self.groupid,
            'auto.offset.reset': 'earliest',
            'session.timeout.ms': self.session_time_out
        })
        c.subscribe(topics)
        return c

    def fetch(self):
        """Fetch `self.n_clients` messages from `self.readtopic`."""
        consumer = self.get_consumer([self.readtopic])
        messages = consumer.consume(self.n_clients)
        consumer.commit()
        return [msg.value().decode('utf-8') for msg in messages]

    def get_producer(self):
        """Set up and return a Kafka producer."""
        return Producer({'bootstrap.servers': self.server})

    def send(self, payload):
        """Send a serialized payload to `self.sendtopic`."""
        producer = self.get_producer()
        producer.produce(self.sendtopic, payload)
        producer.flush()

    def prepare_payload(self, weights, metrics, state, epoch):
        """Assemble and serialize a payload.

        weights : dict of aggregated arrays of model weights
        metrics : optional dict of aggregated validation metrics
        state   : str, training state ('START', 'RUN' or 'STOP')
        epoch   : int, index of the next training epoch

        Return the serialized payload, as a string.
        """
        payload = {
            'weights': weights,
            'metrics': metrics,
            'state': state,
            'epoch': epoch
        }
        return serialize_payload(payload)

    def initialize(self):
        """Send an initial payload to clients, to share start weights."""
        payload = self.prepare_payload(
            weights=self.model.generate_weights(),
            metrics=None,
            state='START',
            epoch=0
        )
        self.send(payload)

    def run_once(self):
        payloads = self.fetch()
        payloads = [deserialize_payload(p) for p in payloads]
        # TODO: check that all payloads come from the same epoch
        if payloads[0]['state'] == 'START':
            metrics = None
        else:
            metrics = self.model.aggregate_metrics(
                partial_metrics=[p['metrics'] for p in payloads]
            )
            self.current_metrics = metrics

        epoch = payloads[0]['epoch'] + 1
        state = 'RUN' if self.keep_running(metrics, epoch) else 'STOP'
        if state != 'STOP':
            weights = self.model.aggregate_weights(
                dataset_sizes=[p['dataset_size'] for p in payloads],
                partial_weights=[p['weights'] for p in payloads]
            )
        else:
            weights = self.model.get_weights()
        
        payload = self.prepare_payload(
            weights,
            metrics,
            state,
            epoch
        )
        self.send(payload)
        keep_running = bool(state != 'STOP')
        return keep_running

    def run(self):
        """Run the training loop on the server side."""
        weights = self.model.get_weights()
        metrics = None
        keep_running = True
        while keep_running:
            keep_running = self.run_once()
            logger.info(self.current_metrics)


    def keep_running(self, metrics, epoch):
        """Return a boolean indicating whether to keep training.

        metrics : dict of aggregated validation metrics
        epoch   : int, index of the next epoch to run
        """
        # TODO: implement early stopping based on metrics monitoring.
        return (epoch < self.max_iter)
