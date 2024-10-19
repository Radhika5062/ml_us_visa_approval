from us_visa.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from us_visa.logger import logging
from us_visa.exception import CustomException
from us_visa.components.data_ingestion import DataIngestion
from us_visa.components.data_validation import DataValidation
from us_visa.components.data_transformation import DataTransformation
import sys

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
            This method of training pipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainingPipeline Class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            logging.info(data_ingestion)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainingPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys)
    
    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:
        """
            This method of train pipeline class is responsible for starting data validation component
        """
        try:
            logging.info("Entered the start_data_validation method of TrainingPipeline Class")
            data_validation = DataValidation(
                                        data_ingestion_artifact= data_ingestion_artifact,
                                        data_validation_config=self.data_validation_config
            )
            data_validation_artifact = data_validation.inititate_data_validation()
            logging.info("Performed data validation operation")
            logging.info("Exited the start_data_validation method of TrainingPipeline Class")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)
    
    def start_data_transformation(self, data_ingestion_artifact:DataIngestionArtifact,
                                  data_validation_artifact:DataValidationArtifact) -> DataTransformationArtifact:
        """
            This method of the TrainingPipeline class is responsible for starting data transformation component
        """
        try:
            data_transformation = DataTransformation(
                    data_ingestion_artifact=data_ingestion_artifact,
                    data_transformation_config=self.data_transformation_config,
                    data_validation_artifact=data_validation_artifact
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys)

    
    def run_pipeline(self)-> None:
        """
            This method is responsible for running the complete training pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_config = self.start_data_transformation(
                                        data_ingestion_artifact=data_ingestion_artifact,
                                        data_validation_artifact=data_validation_artifact                                        
                                        )
        except Exception as e:
            raise CustomException(e, sys)
        