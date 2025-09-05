import json
import datetime
import boto3
from faker import Faker

class MinioGen:
    def __init__(self, host, user, key):
        self.s3 = boto3.client(
            's3', 
            endpoint_url=host, 
            aws_access_key_id=user, 
            aws_secret_access_key=key
        )

    def create_bucket(self, bucket):
        try:
            self.s3.head_bucket(Bucket=bucket)
            print("The bucket already exists!")
        except:
            response = self.s3.create_bucket(Bucket=bucket)
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                print(f"The bucket '{bucket}' created!")
            else:
                print(f"Failed to create '{bucket}' S3 bucket.")
                        
    def insert_data(self, bucket, path, fields, quantity):
        try:
            fake = Faker()
            data = {}
            for i in range(quantity):
                key = f'{fields}{i + 1}'
                data[key] = getattr(fake, fields)()
                # TO DO LIST
                # for field in fields:
                #    data[field] = getattr(fake, field)()

            json_record = json.dumps(data)

            now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")

            file_name = f"{now}.json"
            object_key = path + file_name

            response = self.s3.put_object(
                Bucket=bucket, 
                Key=object_key, 
                Body=json_record
            )
            
        except self.s3.exceptions.NoSuchBucket:
            print(f"Bucket '{bucket}' does not exist.")

    def delete_bucket(self, bucket):
        # List objects in the bucket
        try:
            objects = self.s3.list_objects(Bucket=bucket).get('Contents', [])

            # Delete each object in the bucket
            for obj in objects:
                self.s3.delete_object(Bucket=bucket, Key=obj['Key'])
                print(f"Deleted object '{obj['Key']}' from bucket '{bucket}'")

            # Delete the bucket once it's empty
            try:
                self.s3.delete_bucket(Bucket=bucket)
                print(f"Bucket '{bucket}' deleted successfully!")
            except self.s3.exceptions.BucketNotEmpty:
                print(f"Bucket '{bucket}' is not empty. Delete its objects first.")
        except self.s3.exceptions.NoSuchBucket:
            print(f"Bucket '{bucket}' does not exist.")
