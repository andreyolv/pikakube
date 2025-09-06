from prometheus_client import start_http_server
from prometheus_client import Summary, Counter, Histogram, Gauge, Info
import time
import random

FUNC_TIME = Gauge('function_execution_time_seconds', 'Time taken by the function to execute', ['instance'])

def process_request():
    start_time = time.time()
    
    sleep_time = random.randint(1, 10)
    time.sleep(sleep_time)
    
    execution_time = time.time() - start_time
    FUNC_TIME.labels(instance='QA').set(execution_time)

def process_request2():
    start_time = time.time()
    
    sleep_time = random.randint(1, 10)
    time.sleep(sleep_time)
    
    execution_time = time.time() - start_time
    FUNC_TIME.labels(instance='PRD').set(execution_time)

if __name__ == '__main__':
    start_http_server(8000)
    while True:
        process_request()