# Quickstart

## Install nuage-learning
```bash
$ git clone https://github.com/mcrts/nuage-learning nuage-learning
$ pip install -e nuage-learning
```

## Running the example
* A kafka server should be running on localhost:9092
* There should be 2 topics 'server' and 'clients'

```bash
$ python nuage-learning/example_02_kafkathreaded.py
```
This example train a SGDClassifier on the Iris dataset spread across 100 worker nodes for 10 loops.

## Example results
[example_02_kafkathreaded.py : execution log](/images/running_example.png?raw=true "execution log")
[example_02_kafkathreaded.py : client message](/images/local_model.png?raw=true "client message")
[example_02_kafkathreaded.py : client message](/images/global_model.png?raw=true "server message")
[example_02_kafkathreaded.py : training analytics](/images/analytics.png?raw=true "training analytics")

# Acknowledgment
* Yannick Bouillard
* Paul Andrey
* Alexandre Filiot
* Martin Courtois


# Todo List
* Make an example with a kafka cloud instance (will probably need some work)
* CLI design
* Tweak FederatedSGDClassifier 's API

# Setup Kafka
<details>
  <summary>Installing, configuring and running Apache-Kafka</summary>

## 1. Install Apache-Kafka

java8 is required
```shell
apt install openjdk-8-jdk
```

Download and install Apache-Kafka
```shell
wget https://downloads.apache.org/kafka/2.8.0/kafka_2.12-2.8.0.tgz
tar -xvf kafka_2.12-2.8.0.tgz /opt/kafka_2.12-2.8.0
/opt/kafka_2.12-2.8.0/bin/kafka-topics.sh
```

Sanity-check
```shell
/opt/kafka_2.12-2.8.0/bin/kafka-topics.sh
```

Add /opt/kafka_2.12-2.8.0/bin to your $PATH in ~/.bashrc
```shell
export PATH = $PATH:/opt/kafka_2.12-2.8.0/bin
```

Setup log directories
```shell
mkdir /opt/kafka_2.12-2.8.0/data
mkdir /opt/kafka_2.12-2.8.0/data/zookeeper
mkdir /opt/kafka_2.12-2.8.0/data/kafka
```

Update /opt/kafka_2.12-2.8.0/config/zookeeperproperties
```
dataDir = /opt/kafka_2.12-2.8.0/data/zookeeper
```

Update /opt/kafka_2.12-2.8.0/config/zookeeperproperties
```
log.dirs = /opt/kafka_2.12-2.8.0/data/kafka
```

## 2. Start kafka

```shell
zookeeper-server-start.sh /opt/kafka_2.12-2.8.0/config/zookeeper.properties
kafka-server-start.sh /opt/kafka_2.12-2.8.0/config/server.properties
```

## 3. Install conduktor (Kafka GUI)

```shell
wget https://releases.conduktor.io/linux-deb
dpkg -i Conduktor-2.13.1.deb
```
</details>
