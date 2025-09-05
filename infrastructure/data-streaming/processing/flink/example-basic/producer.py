import json
import random
import uuid
import datetime

from kafka import KafkaProducer

topic = 'clickstream'

customers = ['A', 'B', 'C', 'D', 'E', 'F']

def on_success(metadata):
    print(f"Message produced with the offset: {metadata.offset}")

def on_error(error):
    print(f"An error occurred while publishing the message. {error}")

producer = KafkaProducer(
    bootstrap_servers = "redpanda.redpanda.svc.cluster.local:9093",
    value_serializer=lambda m: json.dumps(m).encode('ascii')
)

# Produce 10 events
for i in range(0,10):
    random_customers = random.sample(customers, 2)
    
    message = {
        "id" : str(uuid.uuid4()),
        "value": round(random.uniform(0, 1000), 2),
        "customer_debit": random_customers[0],
        "customer_credit": random_customers[1],
        "ts": str(datetime.datetime.now())
    }

    future = producer.send(topic, message)

    # Add async callbacks to handle both successful and failed message deliveries
    future.add_callback(on_success)
    future.add_errback(on_error)

producer.flush()
producer.close()

