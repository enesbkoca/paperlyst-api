import json
from confluent_kafka import Producer


class GatewayService:
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': 'localhost:5001'})

    def send_to_kafka(self, topic: str, message: dict[str, ...]):
        message_json = json.dumps(message)

        self.producer.produce(topic, value=message_json.encode())
        self.producer.flush()