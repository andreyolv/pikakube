from prometheus_client import start_http_server
from prometheus_client import Summary, Counter, Histogram, Gauge, Info
import threading
import time
import random

FUNC_TIME = Gauge('function_execution_time_seconds', 'Time taken by the function to execute', ['instance'])

def process_request(instance):
    while True:
        start_time = time.time()

        sleep_time = random.randint(1, 10)
        time.sleep(sleep_time)

        execution_time = time.time() - start_time
        FUNC_TIME.labels(instance=instance).set(execution_time)

if __name__ == '__main__':
    start_http_server(8000)
    
    thread1 = threading.Thread(target=process_request, args=('QA',))
    thread2 = threading.Thread(target=process_request, args=('PRD',))
    
    thread1.start()
    thread2.start()