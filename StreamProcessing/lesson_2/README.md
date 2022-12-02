# Урок 2. Kafka. Архитектура

## Задание

Задание - повторить всё с вебинара в консоли

## Решение

Создаем топик. Изменяем время хранения данных на 2 минуты

```bash
kafka-topics.sh --bootstrap-server localhost:9092 --create --topic lesson2 --replication-factor 1 --partitions 1 --config retention.ms=20000
```

В первом терминале создаём консьюмер, который вычитыват сообщения из топика и пишет их в консоль.

```bash
kafka-console-consumer.sh --topic lesson2 --bootstrap-server localhost:9092
```

Во втором терминале создаем провайдер, который записывет сообщения в топик.

```bash
for x in {1..5}; do $(echo "Test Message ${x}" | kafka-console-producer.sh --broker-list localhost:9092 --topic lesson2); sleep 1; done
```

В первом терминале наблюдаем пришедшие данные.

```bash
Test Message 1
Test Message 2
Test Message 3
Test Message 4
Test Message 5
```

Пересоздадим консьюмер, который вычитыват сообщения из самого начала топика. 

```bash
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic lesson2 --from-beginning
```

Вывод:

```bash
Test Message 1
Test Message 2
Test Message 3
Test Message 4
Test Message 5
```

Удаляем топик.

```bash
kafka-topics.sh -bootstrap-server localhost:9092 --delete --topic lesson2
```
