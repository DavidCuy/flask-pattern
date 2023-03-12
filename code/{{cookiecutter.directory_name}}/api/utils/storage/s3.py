import os
import boto3
from typing import List

from ...config.storage import config

class S3Storage:
    def __init__(self, config_name) -> None:
        aws_access_key = config['s3'][config_name]['aws_access_key']
        aws_secret_key = config['s3'][config_name]['aws_secret_key']
        self.bucket_name = config['s3'][config_name]['bucket_name']
        
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
            

    def list_files(self, path: str = "") -> List[str]:
        response = self.client.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix=path
        )
        return list(map(lambda r: r['Key'], response['Contents']))
    
    def get(self, path: str) -> str:
        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=path
        )
        try:
            content = response['Body'].read()
        except (FileNotFoundError, IOError) as e:
            #traceback.print_exc(file=sys.stdout)
            #print(str(e))
            raise(e)
        return content
    
    def put(self, path: str, content: bytes) -> dict:
        try:
            response = self.client.put_object(
                Body=content,
                Bucket=self.bucket_name,
                Key=path,
            )
        except (FileNotFoundError, IOError) as e:
            #print(str(e))
            raise(e)
        return response
    
    def delete(self, path: str) -> dict:
        try:
            response = self.client.delete_object(
                Bucket=self.bucket_name,
                Key=path,
            )
        except (FileNotFoundError, IOError) as e:
            #print(str(e))
            raise(e)
        return response