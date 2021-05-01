setsid zookeeper-server-start.sh /opt/kafka_2.12-2.8.0/config/zookeeper.properties > zookeeper.log 2>&1 &
setsid kafka-server-start.sh /opt/kafka_2.12-2.8.0/config/server.properties > kafka.log 2>&1 &