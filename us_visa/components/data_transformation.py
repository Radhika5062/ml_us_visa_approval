from us_visa.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.constant import SCHEMA_FILE_PATH, TARGET_COLUMN, CURRENT_YEAR
from ..utils.main_utils import read_yaml_file, save_numpy_array_data, save_object, drop_columns
from us_visa.exception import CustomException
from us_visa.logger import logging
import sys
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer
from sklearn.compose import ColumnTransformer
from us_visa.entity.estimator import TargetValueMapping
import numpy as np
from imblearn.combine import SMOTEENN


class DataTransformation:
    def __init__(self, 
                 data_ingestion_artifact:DataIngestionArtifact,
                 data_transformation_config:DataTransformationConfig,
                 data_validation_artifact:DataValidationArtifact
                 ):
        """
            :param data_ingestion_artifact: output reference of data ingestion artifact stage
            :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(filename=SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e, sys)
    
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
    
    def get_data_transformer_object(self) -> Pipeline:
        """
            Method Name: get_data_transformer_object
            Description: This method creates and returns a data transformer object for data
            Output: data transformer object is created and returned
            On Failure: write an exception log and then raise an exception
        """
        logging.info("Entered the get_data_transformer_object method of DataTransformation class")
        try:
            logging.info("Initialized standard scaler, one hot encoder and ordinal encoder")
            
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()

            logging.info("Get schema")

            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            logging.info("Initialize Power Transformer")

            transform_pipe = Pipeline(
                steps = [
                    ('transformer', PowerTransformer(method = 'yeo-johnson'))
                ]
            )

            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", oh_transformer, oh_columns),
                    ("Ordinal_encoder", ordinal_encoder, or_columns),
                    ("Transformer", transform_pipe, transform_columns),
                    ("StandardScaler", numeric_transformer, num_features)
                ]
            )

            logging.info("Created preprocessor object from ColumnTransformer")

            logging.info("Exiting get_data_transformer_object")

            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)
    
    def operations_on_datasets(self, data):
        """
            method name: operations_on_datasets
            description: perform operations on the train and test datasets
            output:
            on failure: raise exception
        """
        try:
            logging.info("Entered the operations_on_datasets method")
            logging.info("Split the input and target variable from the training dataset")

            input_feature_df = data.drop(columns = [TARGET_COLUMN], axis = 1)
            target_feature_df = data[TARGET_COLUMN]

            logging.info("Get the age of the company and add it to the dataset")
            input_feature_df['company_age'] = CURRENT_YEAR - input_feature_df['yr_of_estab']

            logging.info("Drop the columns that are not required in model building from the dataset")
            drop_col = self._schema_config['drop_columns']
            input_feature_df = drop_columns(df=input_feature_df, cols = drop_col)

            logging.info("Encode the target variable so that it is in the form of numbers which can be passed to model")
            target_feature_df = target_feature_df.replace(
                    TargetValueMapping()._asdict()
                )

            return input_feature_df, target_feature_df
        except Exception as e:
            raise CustomException(e, sys)

    
    def initiate_data_transformation(self,) -> DataTransformationArtifact:
        """
            method name: initiate_data_transformation
            description: This method initiates the data transformation component for the pipeline
            output: data transformer steps are performed and preprocessor object is created
            on failure: write an exception log and then raise an exception
        """
        try:
            if self.data_validation_artifact.validation_status:
                logging.info("Starting data transformation")
                preprocessor = self.get_data_transformer_object()
                logging.info("Got the preprocessor object")

                logging.info("Read the train data and test data")
                train_df = DataTransformation.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
                test_df = DataTransformation.read_data(file_path= self.data_ingestion_artifact.test_file_path)

                logging.info("Working on the training datase")
                input_feature_train_df, target_feature_train_df = self.operations_on_datasets(train_df)
                input_feature_test_df, target_feature_test_df = self.operations_on_datasets(test_df)
                
                logging.info('Applying preprocessor object on training dataset')
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)

                logging.info('Applying preprocessor object on testing dataset')
                input_feature_test_arr = preprocessor.transform(input_feature_test_df)

                logging.info('Applying SMOTEENN on training dataset')
                smt = SMOTEENN(sampling_strategy="minority")
                input_feature_train_final, target_feature_train_final = smt.fit_resample(
                    input_feature_train_arr,
                    target_feature_train_df
                )
                logging.info("Creating train array and test array")
                train_arr = np.c_[
                                input_feature_train_final,
                                np.array(target_feature_train_final)
                ]

                test_arr = np.c_[
                                np.array(input_feature_test_df),
                                np.array(target_feature_test_df)
                ]

                logging.info("Save the preprocessor object")
                save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
                logging.info("Save the numpy array for train and test data")
                save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
                save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)

                logging.info("Create the artifact")
                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path = self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                    transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
                )

                return data_transformation_artifact
            else:
                raise Exception(self.data_validation_artifact.message)
        except Exception as e:
            raise CustomException(e, sys)




                


