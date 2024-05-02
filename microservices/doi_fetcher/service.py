import json
import os
from confluent_kafka import Producer, Consumer, KafkaError
import logging

class DoiFetcherService:
    def __init__(self):
        # Initialize Kafka consumer
        self.consumer = Consumer({
            'bootstrap.servers': 'localhost:5001',
            'group.id': 'doi_fetcher_group',
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe(['fetch_doi'])

        # Initialize Kafka producer
        self.producer = Producer({'bootstrap.servers': 'localhost:5001'})

        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

    def consume_messages(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        self.logger.error(msg.error())
                        break

                doi_info = json.loads(msg.value().decode('utf-8'))
                self.extract_dois(doi_info)

        finally:
            self.consumer.close()

    def extract_dois(self, doi_info):
        file_name = doi_info['file_name']
        skip_flags = doi_info.get('skip_flags', [])

        directory = '../data/unfetched_dois'
        full_file_path = os.path.join(directory, file_name)

        if not os.path.isfile(full_file_path):
            self.logger.error(f"The file '{file_name}' does not exist in the directory.")
            return

        with open(full_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                for doi in line.strip().split():
                    self.publish_doi(doi)

    def publish_doi(self, doi):
        self.producer.produce('fetch_paper', value=json.dumps({'doi': doi}).encode())
        self.producer.flush()
        self.logger.info(f"DOI published: {doi}")

