from models import User

from confluent_kafka import Consumer
from confluent_kafka.cimpl import Message

config = {
    "bootstrap.servers" : "localhost:9092",
    "group.id" : "my_check_group"
}
consumer = Consumer(config)
TOPIC = ["navin_check"]

consumer.subscribe(TOPIC)

while True:
    data: Message = consumer.poll(1)
    if data is not None:
        if data.error():
            print(data.error())
        data: User = User.model_validate_json(data.value())
        print(f"Key: {data.id} Value: {data.firstName}")

