from models import User

from confluent_kafka import Consumer
from confluent_kafka.cimpl import Message

from user_pb2 import User as UserProto

config = {
    "bootstrap.servers" : "localhost:9092",
    "group.id" : "my_check_group"
}
consumer = Consumer(config)
TOPIC = ["navin_basic_check"]

consumer.subscribe(TOPIC)

def basic_consume():
    while True:
        data: Message = consumer.poll(1)
        if data is None: continue
        if data.error():
            print(data.error())
            break
        data: User = User.model_validate_json(data.value())
        print(f"Key: {data.id} Value: {data.firstName}")


if __name__ == "__main__":
    basic_consume()
