from confluent_kafka import Producer
from faker import Faker
import json
import uuid
import time

if __name__ == '__main__':
    conf = {'bootstrap.servers': 'localhost:29092'}

    # Create Producer instance
    p = Producer(**conf)

    # Configurações do Faker
    faker = Faker(['pt_BR'])
    date_format = '%Y-%m-%d'

    cont = 0
    while 1:
        try:
            produto = faker.word()
            preco = str(faker.random_digit()) + '.' + str(faker.random_number(digits=2))
            date = faker.date_between(start_date='-3y', end_date='today').strftime(date_format)
            valor = faker.random_number(digits=4)

            print(f"Enviando -> {produto},{preco},{date},{valor}")
            message = json.dumps({
                "idcompras": cont,
                "produto": produto,
                "preco": preco,
                "data": date,
                "valor": valor
            }).encode('utf-8')

            key = str(uuid.uuid4())
            p.produce('compras', key=key, value=message)

            cont += 1

        except BufferError:
            print('Local producer queue is full ({0} messages awaiting delivery): try again.'.format(len(p)))

        time.sleep(1)
        p.poll(0)
        p.flush()
