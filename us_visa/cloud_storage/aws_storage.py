from us_visa.configuration.aws_connection import S3Client
from us_visa.logger import logging
from us_visa.exception import CustomException
from mypy_boto3_s3.service_resource import Bucket
import sys
from typing import Union, List
from io import StringIO
import pickle
from botocore.exceptions import ClientError
import os
from pandas import DataFrame, to_csv, read_csv


class SimpleStorageService:
    def __init__(self):
        logging("Making the connection with AWS S3 bucket")
        s3_client = S3Client()
        logging.info("Getting the s3_reource and s3_client from the connection")
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client
    
    def get_bucket(self, bucket_name:str) -> Bucket:
        """
            Method Name: get_bucket
            Description: This method gets the bucket object based on the bucket name
            Output: Bucket object is returned based on the bucket name
            On Failure: Write an exception log and raise Exception
        """
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            logging.info("Exited the get_bucket of SimpleStorageServices Class")
            return bucket
        except Exception as e:
            raise CustomException(e, sys)
        


    def s3_key_path_available(self, bucket_name, s3_key) ->bool:
        """
            Method Name:    s3_key_path_available
            Description:    this method is used to check if the s3_key which is the name of the model file uploaded to
                            s3 bucket exists or not. If it exists then we also check if there are multiple such files or not. 
        """
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix = s3_key)]
            if len(file_objects)>0:
                return True
            else:
                return False
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_file_object(self, filename:str, bucket_name:str) -> Union[List[object], object]:
        """
            Method Name:    get_file_object
            Description:    This method gets the file object from bucket_name bucket based on the filename
            Output:         List of objects or object is returned based on filename
            On Failure:     Write an exception log and raise Exception
        """
        try:
            logging.info("Retrieve the bucket from S3 bucket")
            bucket = self.get_bucket(bucket_name=bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix = filename)]
            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(file_objects)
            logging.info("Exited the get_file_object method of the SimpleStorageService Class")
            return file_objs
        except Exception as e:
            raise CustomException(e, sys)
    
    @staticmethod
    def read_object(object_name:str, decode:bool = True, make_readable:bool=False) -> Union[StringIO, str]:
        """
            Method Name:    read_object
            Description:    This method reads the object_name object with kwargs
            Output:         Read the object
            On Failure:     raise exception
        """
        try:
            func = (
                lambda: object_name.get()["Body"].read().decode()
                    if decode is True
                    else object_name.get()["Body"].read()
            )
            conv_func = lambda: StringIO(func()) if make_readable is True else func()
            logging.info("Exiting the read_object method of the SimpleStorageService class")
        except Exception as e:
            raise CustomException(e, sys)

    
    def load_model(self, model_name:str, bucket_name:str, model_dir:str = None) -> object:
        """
            Method Name:    load_model
            Description:    This methos loads the model_name model from bucket_name bucket with kwargs
            Output:         lost of objects or object is returned based on the filename
            On Failure:     Write an exception log and then raise exception
        """
        try:
            func = (
                lambda: model_name
                        if model_dir is None
                        else model_dir + "/" + model_name
            )
            model_file = func()
            file_object = self.get_file_object(model_file, bucket_name=bucket_name)
            model_obj = self.read_object(file_object, decode = False)
            model = pickle.loads(model_obj)
            logging.info("Exited the load_model method of the SimpleStorageService class")
            return model
        except Exception as e:
            raise CustomException(e, sys)

    def create_folder(self, folder_name:str, bucket_name:str) -> None:
        """
            Method Name:    create_folder
            Description:    This method creates a folder_name folder in bucket_name bucket
            Output:         Folder is created in s3
            On failure:     Raise an exception
        """
        try:
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"
                self.s3_resource.put_object(Bucket = bucket_name, Key = folder_obj)
            else:
                pass
            logging.info("Exited the create_folder method of the SimpleStorageServices Class")
        
    def upload_file(self, from_filename:str, to_filename:str, bucket_name:str, remove:bool = True):
        """
            Method Name:    upload_file
            Description:    This method uploads the from_filename file to bucket_name bucket with to_filename as bucket filename
            Output:         File is uploaded in S3 bucket
            On Failure:     Raise an exception
        """
        try:
            logging.info(f"Uploading {from_filename} file to {to_filename} file in {bucket_name} bucket")
            self.s3_resource.meta.client.upload_file(from_filename, to_filename)
            logging.info(f"File upload completed")
            if remove is True:
                os.remove(from_filename)
                logging.info(f"Remove is set to {remove}, deleted the file")
            else:
                logging.info(f"Remove is set to {remove}, not deleted the file")
            logging.info("Exited the upload_file method of the SimpleStorageService Class")
        except Exception as e:
            raise CustomException(e,sys)
    
    def upload_df_as_csv(self, data_frame:DataFrame, local_filename:str, bucket_filename:str, bucket_name:str) -> None:
        """
            Method Name:    upload_df_as_csv
            Description:    This method uploads the dataframe to bucket_filename in the bucket_name bucket
            Output:         Folder is created in the S3 bucket
            On Failure:     Raise an exception
        """
        try:
            logging.info("Convert the dataframe into csv file")
            data_frame.to_csv(bucket_filename, index = None, header = True)
            logging.info("Upload the csv file in S3 bucket")
            self.upload_file(local_filename, bucket_filename, bucket_name=bucket_name)
            logging.info("Exited the upload_df_as_csv method of the SimpleStorageServices class")
        except Exception as e:
            raise CustomException(e, sys)
    
    def read_csv(self, filename:str, bucket_name:str) ->DataFrame:
        """
            Method Name:    read_csv
            Description:    This method gets the dataframe from the object name
            Output:         Get the dataframe
            On Failure:     Raise exception
        """
        try:
            csv_obj = self.get_file_object(filename=filename, bucket_name=bucket_name)
            df = self.get_df_from_object(csv_obj) 
            logging.info("Exited the read_csv method of SimpleStorageServices Class")
            return df
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_df_from_object(self, object_:object) ->DataFrame:
        """
            Method Name:    get_df_from_object
            Description:    This method gets the dataframe from the object name
            Output:         Get the dataframe
            On Failure:     Raise Exception
        """
        try:
            content = self.read_object(object_name=object_, make_readable=True)
            df = read_csv(content, na_values = "na")
            logging.info("Exited the get_df_from_object method of SimpleStorageServices Class")
            return df
        except Exception as e:
            raise CustomException(e, sys)
    

        
    