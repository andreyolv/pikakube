import time
import os
import json
import pickle
from kubernetes import client, config

CACHE_EXPIRATION_TIME = 600
CACHE_FILE = 'cache_file.pkl'

def carregar_cache():
    try:
        with open(CACHE_FILE, 'rb') as file:
            cache_data = pickle.load(file)
        return cache_data
    except (FileNotFoundError, pickle.PickleError):
        return None

def salvar_cache(data):
    with open(CACHE_FILE, 'wb') as file:
        pickle.dump(data, file)

def obter_dados():
    try:
        config.load_incluster_config() # config.load_kube_config()
        api_instance = client.CoreV1Api()
        namespaces = api_instance.list_namespace()

        list_namespaces = []
        for ns in namespaces.items:
            list_namespaces.append(ns.metadata.name)

        return list_namespaces

    except Exception as e:
        print(f"Erro ao listar namespaces: {e}")

while True:
    cache_data = carregar_cache()

    if cache_data is None or (time.time() -  cache_data['timestamp']) > CACHE_EXPIRATION_TIME:
        dados = obter_dados()
        timestamp = time.time()
        cache_data = {'NAMESPACE_LIST': dados, 'timestamp': timestamp}
        salvar_cache(cache_data)
        print(f"Cache atualizado em {time.ctime(timestamp)}")

    print("Namespaces:")
    print(cache_data)

    time.sleep(60)
