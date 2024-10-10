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
