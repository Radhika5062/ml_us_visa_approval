from dataclasses import dataclass
from us_visa.entity.config_entity import ModelEvaluationConfig
from us_visa.entity.artifact_entity import DataIngestionArtifact, ModelTrainerArtifact
from us_visa.logger import logging
from us_visa.exception import CustomException
import sys

@dataclass
class EvaluateModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float

class ModelEvaluation:
    def __init__(self, 
                 model_eval_config:ModelEvaluationConfig,
                 data_ingestion_artifact:DataIngestionArtifact,
                 model_trainer_artifact:ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)
    
    def 
        