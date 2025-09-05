import requests
import time
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https:/xxxxxxxxxxxxx
NUM_REQUESTS = 1000
MAX_WORKERS = 10  # Número de threads simultâneas
RETRY_WAIT = 1 # Tempo de espera em caso de rate limit (429)

def make_request(i):
    try:
        response = requests.get(URL, verify=False)
        print(f"[{i+1}] Status: {response.status_code}")
        if response.status_code == 429:
            print(f"🚨 Rate limit atingido! Aguardando {RETRY_WAIT}s antes de continuar...")
            time.sleep(RETRY_WAIT)
        return response.status_code
    except requests.RequestException as e:
        print(f"❌ Erro na requisição {i+1}: {e}")
        return None

# Criando múltiplas threads para acelerar as requisições
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = {executor.submit(make_request, i): i for i in range(NUM_REQUESTS)}

    for future in as_completed(futures):
        future.result()  # Aguarda a execução de cada requisição

print("✅ Teste finalizado!")
