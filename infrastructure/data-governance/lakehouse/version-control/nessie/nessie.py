from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import *

# init session
spark = SparkSession \
    .builder \
    .appName("etl-device-subscription") \
    .config("spark.sql.execution.pyarrow.enabled", "true") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://45.55.126.192") \
    .config("spark.hadoop.fs.s3a.access.key", "minio") \
    .config("spark.hadoop.fs.s3a.secret.key", "minio123") \
    .config("spark.hadoop.fs.s3a.path.style.access", True) \
    .config("spark.hadoop.fs.s3a.fast.upload", True) \
    .config("spark.hadoop.fs.s3a.multipart.size", 104857600) \
    .config("fs.s3a.connection.maximum", 100) \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.extensions", "org.projectnessie.spark.extensions.NessieSpark32SessionExtensions") \
    .config("spark.sql.catalog.owshq", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.owshq.catalog-impl", "org.apache.iceberg.nessie.NessieCatalog") \
    .config("spark.sql.catalog.owshq.s3.endpoint", "http://45.55.126.192") \
    .config("spark.sql.catalog.owshq.warehouse", "s3a://lakehouse/production/iceberg/") \
    .config("spark.sql.catalog.owshq.uri", "http://159.89.242.182:19120/api/v1") \
    .config("spark.sql.catalog.owshq.ref", "main") \
    .config("spark.sql.catalog.owshq.auth_type", "NONE") \
    .getOrCreate()

# print spark's config
print(SparkConf().getAll())
spark.sparkContext.setLogLevel("INFO")