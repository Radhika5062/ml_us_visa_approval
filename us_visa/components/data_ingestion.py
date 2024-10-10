from us_visa.entity.config_entity import DataIngestionConfig
from us_visa.logger import logging
from us_visa.exception import CustomException
import sys 
from us_visa.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
from us_visa.data_access.usvisa_data import USvisaData
from us_visa.logger import logging
from us_visa.exception import CustomException
import os
from sklearn.model_selection import train_test_split


class DataIngestion:
    """
        Configuration for data ingestion
    """
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)
    
    def export_data_into_feature_store(self) -> pd.DataFrame:
        """
            Method Name:    export_data_into_feature_store
            Description:    This method exports data from mongodb to csv file
            Output:         data is returned as artifact of data ingestion components
            On Failure:     Write an exception log and then raise an exception
        """
        try:
            logging.info(f"Exporting data from mongodb")
            usvisa_data = USvisaData()
            dataframe = usvisa_data.export_collection_as_database(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path, index = False, header = True)
            return dataframe
        except Exception as e:
            raise CustomException(e, sys)
    
    def split_data_as_train_test(self, dataframe:pd.DataFrame) -> None:
        """
            Method Name:    split_data_as_train_test
            Description:    This method splits the dataframe into train set and test set based on the split ratio

            Output:         Train file and test files get created. No output returned.
            On Failure:     raise exception
        """
        try:
            train_set, test_set = train_test_split(dataframe, test_size = self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the data. Now is the time to store the data")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Exporting train and test file path")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index = False, header = True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index = False, header = True)
            logging.info("Exported train and test data to respective files")
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
            Method Name:    initiate_data_ingestion
            Description:    This method initiates the data ingestion components of training pipeline
            Output:         train and test datasets are returned as artifacts of data ingestion components
            On Failure:     Raise an exception
        """

        logging.info("Entered initate_data_ingestion method of DataIngestion class")
        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from mongodb")
            self.split_data_as_train_test(dataframe=dataframe)
            logging.info("Performed train test split on the dataset")
            logging.info("Exited initiate_data_ingestion method of DataIngestion Class")

            data_ingestion_artifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path
                                                            )
            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)
