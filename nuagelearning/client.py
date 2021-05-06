import time

from confluent_kafka import Consumer, Producer, KafkaException

from nuagelearning.utils import deserialize_payload, serialize_payload, logger


class Client:
    readtopic = "server"
    sendtopic = "clients"
    session_time_out = 6000

    def __init__(self, dataset, groupid, model, server):
        self.dataset = dataset
        self.groupid = groupid
        self.model = model
        self.server = server

    def get_consumer(self, topics):
        c = Consumer({
            'bootstrap.servers': self.server,
            'group.id': self.groupid,
            'auto.offset.reset': 'earliest',
            'session.timeout.ms': self.session_time_out,
        })
        c.subscribe(topics)
        return c

    def get_producer(self):
        p = Producer({
            'bootstrap.servers': self.server,
        })
        return p

    def fetch(self):
        consumer = self.get_consumer([self.readtopic])
        msg = consumer.consume(1)[0]
        consumer.commit()
        return msg.value().decode('utf-8')

    def send(self, payload):
        producer = self.get_producer()
        producer.produce(self.sendtopic, payload)
        producer.flush()
    
    def deserialize_message(self, message):
        message = deserialize_payload(message)
        return message

    def prepare_payload(self, weights, metrics, dataset_size, state, epoch):
        data = {
            'weights': weights,
            'metrics': metrics,
            'dataset_size': dataset_size,
            'state': state,
            'epoch': epoch,
            'client_id': self.groupid
        }
        payload = serialize_payload(data)
        return payload

    def get_state(self, message):
        if 'state' not in message:
            raise KeyError('No <state> key in message', message)
        return message['state']

    def get_epoch(self, message):
        if 'epoch' not in message:
            raise KeyError('No <epoch> key in message', message)
        return message['epoch']

    def set_weights(self, message):
        if 'weights' not in message:
            raise KeyError('No <weights> key in message', message)
        weights = message['weights']
        self.model.set_weights(weights)

    def evaluate(self):
        X, y = self.dataset
        metrics = self.model.evaluate(X, y)
        return metrics

    def train(self):
        X, y = self.dataset
        self.model.run_training_epoch(X, y)

    def get_weights(self):
        return self.model.get_weights()

    def run_once(self):
        message = self.fetch()
        message = self.deserialize_message(message)
        self.set_weights(message)

        if self.get_state(message) == "STOP":
            pass
        else:
            if self.get_state(message) == "START":
                metrics = None
            else:
                metrics = self.evaluate()

            self.train()
            weights = self.get_weights()
            payload = self.prepare_payload(
                weights,
                metrics,
                len(self.dataset[1]),
                self.get_state(message),
                self.get_epoch(message)
            )
            self.send(payload)
        
        keep_running = bool(self.get_state(message) != 'STOP')
        return keep_running


    def run(self):
        keep_running = True
        while keep_running:
            keep_running = self.run_once()
