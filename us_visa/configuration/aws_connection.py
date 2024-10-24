import boto3
import os 
from us_visa.secret import AWS_ACCESS_KEY, AWS_SECRET_KEY
from us_visa.constant import REGION_NAME

class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self, region_name = REGION_NAME):
        """
            This class gets AWS credentials from secret.py and creates a connection with s3 bucket
        """
        if S3Client.s3_resource==None or S3Client.s3_client == None:
            __access_key_id = AWS_ACCESS_KEY
            __secret_access_key = AWS_SECRET_KEY
            if __access_key_id is None:
                raise Exception(f"AWS_ACCESS_KEY is not set")
            if __secret_access_key is None:
                raise Exception(f"AWS_SECRET_KEY is not set")
            S3Client.s3_resource = boto3.resource(
                                        's3',
                                        aws_access_key_id = __access_key_id
                                        aws_scret_acess_key = __secret_access_key
                                        region_name = region_name
            )

            S3Client.s3_client = boto3.client(
                                        's3',
                                        aws_access_key_id = __access_key_id
                                        aws_scret_acess_key = __secret_access_key
                                        region_name = region_name
            )
        self.s3_client = S3Client.s3_client
        self.s3_resource = S3Client.s3_resource