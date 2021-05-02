import time

from confluent_kafka.admin import AdminClient, NewTopic

from src.utils import logger


class Admin:
    topics = ["server", "clients"]
    session_time_out = 6000

    def __init__(self, server):
        self.admin = AdminClient({'bootstrap.servers': server})

    def initialize(self):
        topics = [NewTopic(topic, num_partitions=3, replication_factor=1) for topic in self.topics]
        fs = self.admin.create_topics(topics)

        for topic, f in fs.items():
            try:
                f.result()
                logger.info("Topic {} created".format(topic))
            except Exception as e:
                logger.info("Failed to create topic {}: {}".format(topic, e))

    def clear(self):
        fs = self.admin.delete_topics(self.topics)

        for topic, f in fs.items():
            try:
                f.result()
                logger.info("Topic {} deleted".format(topic))
            except Exception as e:
                logger.info("Failed to delete topic {}: {}".format(topic, e))
    
    def setup_server(self):
        self.clear()
        time.sleep(2)
        self.initialize()
