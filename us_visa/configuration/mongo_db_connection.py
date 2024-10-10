from us_visa.constant import MONGO_DB_URL_KEY, DATABASE_NAME
import pymongo
import certifi
from us_visa.exception import CustomException
from us_visa.logger import logging
import sys

ca = certifi.where()

class MongoDBClient:
    """
        Class Name:     MongoDBClient
        Description:    This class helps to create a connection to MongoDB
        Output:         Connection to mongodb database
        On Failure:     Raise an exception
    """
    client = None

    def __init__(self, database_name = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = MONGO_DB_URL_KEY
                if mongo_db_url is None:
                    raise Exception(f"Mongo DB URL is not set")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile = ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB Connection is successful")
        except Exception as e:
            raise CustomException(e, sys)