from us_visa.configuration.mongo_db_connection import MongoDBClient
from us_visa.constant import DATABASE_NAME
from us_visa.logger import logging
from us_visa.exception import CustomException
import pandas as pd
import numpy as np
import sys


class USvisaData:
    """
        This class helps to export the entire mongo db record as pandas dataframe
    """

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise CustomException(e, sys)
    
    def export_collection_as_database(self, collection_name:str, database_name:[str] = None) -> pd.DataFrame:
        try:
            """
                Export the entire collection from MongoDB as a dataframe
                return pd.DataFrame of collection
            """
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"], axis = 1)
            df.replace({"na":np.nan}, inplace = True)
            return df
        except Exception as e:
            raise CustomException(e, sys)