import time


from confluent_kafka import Consumer, KafkaException


class Client:
    readtopic = "read_topic"
    sendtopic = "send_topic"
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

    def run(self):
        while True:
            print('I am running in the 90s')
            data = self.fetch()
            print(data)