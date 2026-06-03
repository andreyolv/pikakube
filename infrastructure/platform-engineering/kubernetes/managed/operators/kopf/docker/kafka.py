from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from kafka import KafkaProducer
from faker import Faker
import json

class KafkaGen:
    def __init__(self, bootstrap_servers):
        self.admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    def create_topic(self, topic, num_partitions=1, replication_factor=1):
        topic = NewTopic(name=topic, num_partitions=num_partitions, replication_factor=replication_factor)
        try:
            self.admin_client.create_topics(new_topics=[topic])
            print(f"Topic '{topic}' created!")
        except TopicAlreadyExistsError:
            print(f"Topic '{topic}' already exists.")
            
    def insert_data(self, topic, fields, quantity):
        fake = Faker()
                
        for _ in range(quantity):
            document = {}
            for field in fields:
                document[field] = getattr(fake, field)()
            message = json.dumps(document).encode('utf-8')
            self.producer.send(topic, value=message)
    
    def delete_topic(self, topic):
        try:
            self.admin_client.delete_topics(topics=[topic])
            print(f"Topic '{topic}' deleted!")
        except UnknownTopicOrPartitionError:
            print(f"Topic '{topic}' not exists.")