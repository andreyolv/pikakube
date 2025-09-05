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
            cidade = faker.city()
            nome = faker.name()
            bairro = faker.word()
            idcompra = cont  # Usamos o mesmo contador para atribuir um ID de compra único

            print(f"Enviando -> {cidade},{nome},{bairro},{idcompra}")
            message = json.dumps({
                "cidade": cidade,
                "nome": nome,
                "bairro": bairro,
                "idcompra": idcompra
            }).encode('utf-8')

            key = str(uuid.uuid4())
            p.produce('usuarios', key=key, value=message)

            cont += 1

        except BufferError:
            print('Local producer queue is full ({0} messages awaiting delivery): try again.'.format(len(p)))

        time.sleep(1)
        p.poll(0)
        p.flush()