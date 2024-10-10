from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from ..utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.constant import SCHEMA_FILE_PATH
from us_visa.exception import CustomException
from us_visa.logger import logging
import sys
import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
import json


class DataValidation:
    def __init__(self, 
                 data_ingestion_artifact:DataIngestionArtifact, 
                 data_validation_config:DataValidationConfig
                 ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(filename=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)
    
    def validate_number_of_columns(self, dataframe:pd.DataFrame) ->bool:
        """
            method name:    validate_number_of_columns
            description:    this method validates the number of columns
            output:         Returns bool value based on validate results
            on failure:     Write an exception log and then raise an exception
        """
        try:
            status = len(dataframe.columns) == len(self._schema_config['columns'])
            logging.info(f"Are all the required columns present {status}")
            return status
        except Exception as e:
            raise CustomException(e, sys)
    
    def is_column_exist(self, df:pd.DataFrame) -> bool:
        """
            method name:    is_column_exist
            description:    this method validates the presence of all the numercial as well as categorical columns
            output:         returns bool value based on the validation results
            on failure:     returns an exception
        """
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            missing_numerical_columns = [col 
                                         for col in self._schema_config['numerical_columns'] 
                                         if col not in dataframe_columns
                                         ]
            logging.info(f"Number of numerical columns missing = {len(missing_numerical_columns)}")
            if len(missing_numerical_columns) >0:
                logging.info(f"Missing numerical column are: {missing_numerical_columns}")
            
            missing_categorical_columns = [
                                            col 
                                            for col in self._schema_config['categorical_columns']
                                            if col not in dataframe_columns
                                          ]
            logging.info(f"Number of categorical columns missing = {len(missing_categorical_columns)}")
            if len(missing_categorical_columns) >0:
                logging.info(f"Missing categorical columns are {missing_categorical_columns}")
            
            return False if (len(missing_numerical_columns) >0 or
                             len(missing_categorical_columns)>0) else True
        except Exception as e:
            raise CustomException(e, sys)
        
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    def detect_dataset_drift(self, reference_df:pd.DataFrame, current_df: pd.DataFrame)->bool:
        """
            method name:    detect_dataset_drift
            description:    this method validates if drift is detected
            output:         return bool value based on the validation result
            on failure:     raise an exception
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df, current_df)
            report = data_drift_profile.json()
            json_report = json.loads(report)
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, data = json_report)
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected")

            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
        except Exception as e:
            raise CustomException(e, sys)
    
    def inititate_data_validation(self)->DataValidationArtifact:
        """
            method name:    initiate_data_validation
            description:    this method initiates the data validation component for pipeline
            output:         Returns book value based on validation results
            on failure:     raise an exception
        """
        try:
            validation_error_msg = ""
            logging.info("Starting data validation")
            train_df, test_df = (DataValidation.read_data(self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(self.data_ingestion_artifact.test_file_path))
            
            status = self.validate_number_of_columns(dataframe=train_df)
            logging.info(f"All required columns are present in the training dataframe: {status}")
            if not status:
                validation_error_msg= validation_error_msg + f" Columns are missing in training dataframe."
            
            status = self.validate_number_of_columns(dataframe=test_df)
            logging.info(f"All required columns are present in the test dataframe: {status}")
            if not status:
                validation_error_msg=validation_error_msg + f" Columns are missing in testing dataframe"
            
            status = self.is_column_exist(df=train_df)
            if not status:
                validation_error_msg = validation_error_msg + " Columns are missing in training dataset"
            
            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg = validation_error_msg + f" Columns are missing in test dataset"
            
            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    logging.info(f"Drift detected")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"
            else:
                logging.info(f"Validation error: {validation_error_msg}")
            
            data_validation_artifact = DataValidationArtifact(
                validation_status= validation_status,
                message=validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)



