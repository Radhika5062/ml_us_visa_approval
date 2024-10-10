import yaml
import sys
import os 
import numpy as np
import dill
import pandas as pd

from us_visa.logger import logging
from us_visa.exception import CustomException

def read_yaml_file(filename: str) -> dict:
    logging.info('Entered the read_yaml_file method')
    try:
        with open(filename, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys)

def write_yaml_file(file_path:str, data:object, replace: bool = False) -> None:
    logging.info('Entered the write_yaml_file method')
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path:str) -> object:
    logging.info("Entered the load_object method")
    try:
        with open(file_path, 'rb') as file:
            return dill.load(file)
    except Exception as e:
        raise CustomException(e, sys)

def save_numpy_array_data(file_path:str, array:np.array):
    logging.info("Entered the save_numpy_array_data method")
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise CustomException(e, sys)

def load_numpy_array_data(file_path:str) -> np.array:
    logging.info("Entered the load_numpy_array_data")
    try:
        with open(file_path, 'rb') as file:
            return np.load(file)
    except Exception as e:
        raise CustomException(e, sys)

def save_object(file_path:str, obj:object) -> None:
    logging.info("Entered the save_object method")
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            dill.dump(file_path)
    except Exception as e:
        raise CustomException(e, sys)

def drop_columns(df:pd.DataFrame, cols:list) -> pd.DataFrame:
    logging.info("Entered the drop_columns method")
    try:
        df = df.drop(columns = cols, axis = 1)
        return df
    except Exception as e:
        raise CustomException(e, sys)