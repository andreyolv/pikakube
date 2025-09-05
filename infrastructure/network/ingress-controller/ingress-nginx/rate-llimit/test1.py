import requests
import time

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://xxxxxxxxxxxxx
NUM_REQUESTS = 100
INTERVAL = 0.1

for i in range(NUM_REQUESTS):
    response = requests.get(URL, verify=False)
    print(f"[{i+1}] Status: {response.status_code}")

    if response.status_code == 429:
        print("🚨 Rate limit atingido! Aguardando antes de continuar...")
        time.sleep(5)

    time.sleep(INTERVAL)

print("✅ Teste finalizado!")