from us_visa.logger import logging
from us_visa.exception import CustomException
from us_visa.cloud_storage.aws_storage import SimpleStorageService
from us_visa.entity.estimator import USvisaModel
import sys
from pandas import DataFrame

class USVisaEstimator:
    """
        This class is used to save and retrieve us_visa model in s3 bucket and to do prediction
    """

    def __init__(self, bucket_name, model_path):
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model:USvisaModel = None
    
    def is_model_present(self, model_path):
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except CustomException as e:
            print(e)
            return False
    
    def load_model(self)->USvisaModel:
        """
            Method Name:    load_model
            Description:    Load the model from model_path
        """
        try:
            return self.s3.load_model(model_name=self.model_path, bucket_name=self.bucket_name)
        except Exception as e:
            raise CustomException(e, sys)
    
    def save_model(self, from_file, remove:bool=False)->None:
        """
            Save the model to the model_path
        """
        try:
            self.s3.upload_file(from_filename=from_file, to_filename=self.model_path, bucket_name=self.bucket_name, remove=remove)
        except Exception as e:
            raise CustomException(e, sys)
    
    def predict(self, dataframe:DataFrame):
        """
            Method Name:    predict
            Descriotion:    Make predictions from the model
            Output:         Predicted values
            On Failure:     Raise Exception
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise CustomException(e, sys)