import time
import kopf
from minio import MinioGen

# -----------------MINIO-------------------
@kopf.on.create('miniogens')
def create_fn(spec, **kwargs):
    spec = kwargs["body"]["spec"]
    
    miniogen = (MinioGen(spec["source"]["host"]
                        ,spec["source"]["access_key"]
                        ,spec["source"]["secret_key"])
    )
    miniogen.create_bucket(spec["source"]["bucket"]) 

@kopf.timer('miniogens', interval=0)
def my_timer(spec, **kwargs):
    spec = kwargs["body"]["spec"]

    miniogen = (MinioGen(spec["source"]["host"]
                        ,spec["source"]["access_key"]
                        ,spec["source"]["secret_key"])
    )

    (miniogen.insert_data(spec["source"]["bucket"]
                        ,spec["source"]["path"]
                        ,spec["datagen"]["fields"]
                        ,spec["datagen"]["quantity"])
    )

    time.sleep(spec["datagen"]["interval"])

@kopf.on.delete('miniogens')
def delete_fn(spec, **kwargs):
    spec = kwargs["body"]["spec"]
    
    miniogen = (MinioGen(spec["source"]["host"]
                        ,spec["source"]["access_key"]
                        ,spec["source"]["secret_key"])
    )
    miniogen.delete_bucket(spec["source"]["bucket"]) 

## -----------------POSTGRESQL-------------------
#
#@kopf.timer('postgresgen', interval=0)
#def my_timer(spec, **kwargs):
#    spec = kwargs["body"]["spec"]
#
#    PSQL_HOST = spec["source"]["host"]
#    PSQL_DB = spec["source"]["database"]
#    PSQL_TABLE = spec["source"]["table"]
#    PSQL_USER = spec["source"]["user"]
#    PSQL_PASSWORD = spec["source"]["password"]
#
#    records = spec["datagen"]["records"]
#    interval = spec["datagen"]["interval"]
#    fields = spec["datagen"]["fields"]
#
#    client = PostgresClient(db=PSQL_DB, username=PSQL_USER, password=PSQL_PASSWORD, host=PSQL_HOST)
#    client.connect_if_not_connected()
#
#    while i < records:
#        client.insert_row(PSQL_TABLE, fields)
#        i += 1
#
#    time.sleep(interval)
#
## -----------------MONGODB-------------------
# @kopf.on.create('mongogen')
# def create_fn(spec, **kwargs):
#     spec = kwargs["body"]["spec"]
#     
#     mongogen = (MongoGen(spec["source"]["host"]
#                         ,spec["source"]["user"]
#                         ,spec["source"]["password"]
#                         ,spec["source"]["database"])
#     )
#     mongogen.create_collection(spec["source"]["collection"]) 
# 
# @kopf.timer('mongogen', interval=0)
# def my_timer(spec, **kwargs):
#     spec = kwargs["body"]["spec"]
# 
#     mongogen = (MongoGen(spec["source"]["host"]
#                         ,spec["source"]["user"]
#                         ,spec["source"]["password"]
#                         ,spec["source"]["database"])
#     )
# 
#     (mongogen.insert_data(spec["source"]["collection"]
#                         ,spec["datagen"]["fields"]
#                         ,spec["datagen"]["quantity"])
#     )
# 
#     time.sleep(spec["datagen"]["interval"])
# 
# @kopf.on.delete('mongogen')
# def delete_fn(spec, **kwargs):
#     spec = kwargs["body"]["spec"]
#     
#     mongogen = (MongoGen(spec["source"]["host"]
#                         ,spec["source"]["user"]
#                         ,spec["source"]["password"]
#                         ,spec["source"]["database"])
#     )
# 
#     mongogen.drop_collection(spec["source"]["collection"]) 
# 
# ## -----------------KAFKA-------------------
# @kopf.on.create('kafkagen')
# def create_fn(spec, **kwargs):
#     spec = kwargs["body"]["spec"]
#     
#     kafkagen = KafkaGen(spec["source"]["host"])
# 
#     kafkagen.create_topic(spec["source"]["topic"]) 
# 
# @kopf.timer('kafkagen', interval=0)
# def my_timer(spec, **kwargs):
#     spec = kwargs["body"]["spec"]
# 
#     kafkagen = KafkaGen(spec["source"]["host"])
# 
#     (kafkagen.insert_data(spec["source"]["topic"]
#                         ,spec["datagen"]["fields"]
#                         ,spec["datagen"]["quantity"])
#     )
# 
#     time.sleep(spec["datagen"]["interval"])
# 
# @kopf.on.delete('kafkagen')
# def delete_fn(spec, **kwargs):
#     spec = kwargs["body"]["spec"]
#     
#     kafkagen = KafkaGen(spec["source"]["host"])
# 
#     kafkagen.delete_topic(spec["source"]["collection"]) 
# 