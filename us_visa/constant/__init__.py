import os
from datetime import date
from ..secret import mongo_connection_uri

DATABASE_NAME = 'US_VISA'
COLLECTION_NAME = 'visa_data'

MONGO_DB_URL_KEY = mongo_connection_uri

PIPELINE_NAME:str = "usvisa"
ARTIFACT_DIR:str = "artifact"

TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"

FILE_NAME:str = "usvisa.csv"
MODEL_FILE_NAME:str = "model.pkl"


"""
    Data ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME:str = "visa_data"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2


TARGET_COLUMN = "case_status"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")


"""
    Data validation related constansts start with DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

"""
    Data transformation related constants start with DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_OBJECT_DIR:str = "transformed_object"

"""
    Model trainer related constants start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = 'trained_model'
MODEL_TRAINER_TRAINED_MODEL_NAME:str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH:str = os.path.join('config','model.yaml')