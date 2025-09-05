import argparse
import atexit
import json
import logging
import random
import time
import sys

from collections import namedtuple


from confluent_kafka import Producer


logging.basicConfig(
  format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S',
  level=logging.INFO,
  handlers=[
      logging.FileHandler("sales_producer.log"),
      logging.StreamHandler(sys.stdout)
  ]
)

logger = logging.getLogger()

Product = namedtuple('Product', ['name', 'price'])

PRODUCTS = [
    Product('Toothpaste', 4.99),
    Product('Toothbrush', 3.99),
    Product('Dental Floss', 1.99)
]

SELLERS = ['LNK', 'OMA', 'KC', 'DEN']


def make_sales_item():
    seller_id = random.choice(SELLERS)
    qty = random.randint(1, 5)
    product = random.choice(PRODUCTS)

    sales_item = {
        'seller_id': seller_id,
        'product': product.name,
        'quantity': qty,
        'product_price': product.price,
        'sale_ts': int(time.time() * 1000)
    }

    return sales_item


class ProducerCallback:
    def __init__(self, record, log_success=False):
        self.record = record
        self.log_success = log_success

    def __call__(self, err, msg):
        if err:
            logger.error('Error producing record {}'.format(self.record))
        elif self.log_success:
            logger.info('Produced {} to topic {} partition {} offset {}'.format(
                self.record,
                msg.topic(),
                msg.partition(),
                msg.offset()
            ))


def main(args):
    logger.info('Starting sales producer')
    conf = {
        'bootstrap.servers': args.bootstrap_server,
        'linger.ms': 200,
        'client.id': 'sales-1',
        'partitioner': 'murmur2_random'
    }

    producer = Producer(conf)

    atexit.register(lambda p: p.flush(), producer)

    i = 1
    while True:
        is_tenth = i % 10 == 0
        sales_item = make_sales_item()
        producer.produce(topic=args.topic,
                        value=json.dumps(sales_item),
                        on_delivery=ProducerCallback(sales_item, log_success=is_tenth))

        if is_tenth:
            producer.poll(1)
            time.sleep(5)
            i = 0 # no need to let i grow unnecessarily large

        i += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bootstrap-server')
    parser.add_argument('--topic')
    args = parser.parse_args()
    main(args)
