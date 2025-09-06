import os
import time
import struct
import pyodbc
from azure.cli.core import get_default_cli
from azure.identity import AzureCliCredential
from prometheus_client import start_http_server, Counter, Gauge

client_id = os.getenv('SPN_CLIENT_ID')
client_secret = os.getenv('SPN_CLIENT_SECRET')
tenant_id = os.getenv('SPN_TENANT_ID')
server = ""

def connect_to_db(server, database, driver):
    credential = AzureCliCredential()
    databaseToken = credential.get_token('https://database.windows.net/')

    azure_login()

    # get bytes from token obtained
    tokenb = bytes(databaseToken[0], "UTF-8")
    exptoken = b'';
    for i in tokenb:
        exptoken += bytes({i});
        exptoken += bytes(1);
        tokenstruct = struct.pack("=i", len(exptoken)) + exptoken;

    # build connection string using acquired token
    connString = "Driver={ODBC Driver "+str(driver)+" for SQL Server};SERVER="+server+";DATABASE="+database+""
    SQL_COPT_SS_ACCESS_TOKEN = 1256 
    conn = pyodbc.connect(connString, attrs_before = {SQL_COPT_SS_ACCESS_TOKEN:tokenstruct});
    return conn

def azure_login():
    str_login = f"login --service-principal --allow-no-subscriptions -u {client_id} -p {client_secret} -t {tenant_id}"
    str_split = str_login.split()
    cli = get_default_cli()
    cli.invoke(str_split)
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True

def main():
    start_http_server(8000)
    gather_metrics()




if __name__ == '__main__':
    main()
    while True:
        time.sleep(30)

#######
RESPONSE_TIME = Gauge('response_time', 'Hold the last request response time')

@RESPONSE_TIME.time()
def hello():
    time.sleep(5)