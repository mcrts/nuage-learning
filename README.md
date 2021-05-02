# Todo List
* Make an example with multiprocessing (just to make sure it works)
* Make an example with a kafka cloud instance (will probably need some work)
* Package the project
* CLI design
* Tweak FederatedSGDClassifier 's API

# Acknowledgment
* Yannick Bouillard
* Paul Andrey
* Alexandre Filiot
* Martin Courtois

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

  ```javascript
  console.log("I'm a code block!");
  ```
</details>
