# coding: utf-8

"""Docstring."""

import time

import numpy as np
from confluent_kafka import Consumer, Producer

from src.utils import deserialize_payload, serialize_payload


class Server:
    """Docstring."""

    readtopic = "clients"
    sendtopic = "server"
    session_time_out = 6000

    def __init__(self, n_clients, groupid, model, server):
        self.n_clients = n_clients
        self.groupid = groupid
        self.model = model
        self.server = server

    def get_consumer(self, topics):
        c = Consumer({
            'bootstrap.servers': self.server,
            'group.id': self.groupid,
            'auto.offset.reset': 'earliest',
            'session.timeout.ms': self.session_time_out
        })
        c.subscribe(topics)
        return c

    def get_producer(self):
        return Producer({'bootstrap.servers': self.server})

    def send(self, payload):
        producer = self.get_producer()
        producer.produce(self.sendtopic, payload)
        producer.flush()

    def prepare_payload(self, weights, metrics, state, epoch):
        payload = {
            'weights': weights,
            'metrics': metrics,
            'state': state,
            'epoch': epoch
        }
        return serialize_payload(payload)

    def initialize(self):
        payload = self.prepare_payload(
            weights=self.model.generate_weights(),
            metrics=None,
            state='START',
            epoch=0
        )
        self.send(payload)
    
    def simulate(self, state, epoch):
        payload = self.prepare_payload(
            weights=self.model.generate_weights(),
            metrics=None,
            state=state,
            epoch=epoch
        )
        self.send(payload)

    def fetch(self):
        consumer = self.get_consumer([self.readtopic])
        messages = consumer.consume(self.n_clients)
        return [msg.value() for msg in messages]

    def run(self):
        pass
        # in a loop:
        # fetch partial weights and/or scores
        # aggregate weights and/or scores
        # apply stopping criteria
        # send message (stop? ; weights ; scores)
        # if stop: kill
