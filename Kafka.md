# Kafka

## Base concepts

Kafka cluster consists of:
- Zookeper (DataBase whits all metadata about cluster)
- Broker-controller
- Brokers

Controller - it's just randomly selected cluster leader

messages for kafka:
- in bytes (serialized by producer)
- topic name
- key (optional) Messages with the same key will go to similar partition, which guarantee order (FIFO)

Topics phisically splitted for partitions, which is regular log files


## Reliability

Kafka guarantee that no one message will be lost, because of:
`replication_factor` - it's number of partition replication (to different brokers)

Each partition have their own leader, and Produce/Consume messages got through that leader.
Followers only check leader sometimes and ketchup changes from leader

`min.insync.replicas` - number of replicas that can be syncronized

`acks` - 0/1/-1(all) it's number of confirmation from broker, that he getting message (no confirmation, at least from leader, and from all)


## Produce 

1. Producer.send
2. Fetch metadata (from Zookeeper. Who is leader, where is Brokers)
3. Serialize message (key, value)
4. Define partition (based on key. if message didn't have key, that round-robin algorithm)
5. Compress message
6. Accumulate batch
7. Actual sending to broker

## Consume

1. Consumer.poll
2. Fetch metadata
3. Connect to partition-leaders and reading

Better to use consumer groups, when number of consumers equal to number of partitions in topic, so each consumer will read their own partition

Kafka commit reading, and there implemented two alghorithms of commits:
- AutoCommit (at most once) - but you can miss messages
- ManualCommit (at least once) - but you can duplicate messages

Exact once not implemented, but Kafka lets you do it yourself