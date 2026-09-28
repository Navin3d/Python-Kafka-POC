# Python-Kafka-POC
Simple POC with Confluent Kafka python fastapi and docker compose for kafka.

## Obervation:
- Sometimes initially topic not found error is seen.
- No messages in basic consumer is no encode in producer or schema registry is not running in docker.

```commandline
python -m grpc_tools.protoc -I. --python_out=. user.proto
```

## References:
- [Kafka Protobuf](https://oneuptime.com/blog/post/2026-01-21-kafka-protobuf/view)
