import time


from confluent_kafka import Consumer, Producer, KafkaException


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
            'session.timeout.ms': self.session_time_out,
        })
        return p

    def fetch(self):
        consumer = self.get_consumer([self.readtopic])
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue

            print(self.groupid, '| Received', '| message: {}'.format(msg.value().decode('utf-8')))
            break
        consumer.close()
        return msg.value()
    
    def send(self, payload):
        producer = self.get_producer()
        producer.produce(self.sendtopic, payload)
        producer.flush()
    
    def prepare_payload(self, weights, metrics, dataset_size, state, epoch):
        data = {
            'weights': weights,
            'metrics': metrics,
            'dataset_size': dataset_size
            'state': state,
            'epoch': epoch,
            'client_id': self.groupid
        }
        payload = self.serialize(data)
        return payload
    
    def set_weights(self, message):
        pass

    def get_state(self, message):
        if 'state' not in message:
            raise KeyError('No <state> key in message', message)
        return message['state']
    
    def evaluate(self):
        return []

    def train(self):
        pass

    def get_weights(self):
        return []

    def run(self):
        running = True
        while running:
            message = self.fetch()
            print(message)

            self.set_weights(message)

            if self.get_state(message) == "STOP":
                running = False
            else:
                metrics = self.evaluate()
                self.train()
                weights = self.get_weights()
                payload = self.prepare_payload(
                    weights,
                    metrics,
                    len(self.dataset),
                    self.get_state(message),
                    epoch
                )
                self.send(payload)