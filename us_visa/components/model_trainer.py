from us_visa.entity.artifact_entity import DataTransformationArtifact, ClassificationMetricArtifact, ModelTrainerArtifact
from us_visa.entity.config_entity import ModelTrainerConfig
import numpy as np
from neuro_mf import ModelFactory
from us_visa.logger import logging
from us_visa.exception import CustomException
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import sys 
from us_visa.utils.main_utils import load_numpy_array_data, load_object, save_object
from us_visa.entity.estimator import USvisaModel

class ModelTrainer:
    def __init__(self, data_transformation_artifact:DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
    
    def get_model_object_and_report(self, train:np.array, test:np.array):
        """
            Method Name: get_model_object_and_report
            Description: This function uses neuro_mf to get the best model object and report of the best model
            Output: Returns metric artifact and the best model object
            On Failure: Write an exception log and raise an error
        """
        try:
            logging.info("Using neuro_mf to get the best model object and report")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)

            logging.info("Separating the dependent and independent feature from the train and test arrays")
            x_train, y_train, x_test, y_test = train[:, :-1], train[:, -1], test[:, :-1], test[:,-1]

            best_model_detail = model_factory.get_best_model(X= x_train,
                                                             y= y_train,
                                                             base_accuracy=self.model_trainer_config.expected_accuracy)
            
            model_obj = best_model_detail.best_model
            logging.info(f"Print x_test {x_test}")
            y_pred = model_obj.predict(x_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            metric_artifact = ClassificationMetricArtifact(
                        f1_score=f1,
                        precision_score=precision,
                        recall_score=recall
            )
            return best_model_detail, metric_artifact
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        """
            Method name:    initiate_model_trainer
            Description:    This function initiates model trainer
            Output:         Returns model trainer artifact 
            On failure:     Write an log and raise an exception
        """
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)

            logging.info("Numpy load")
            logging.info(f"train_arr = {train_arr[1,:]}")
            logging.info(f"train_arr = {train_arr[1,:]}")
            best_model_detail, metric_artifact = self.get_model_object_and_report(train=train_arr, test=test_arr)

            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more than the base score")
                raise Exception("No best model found with score more than the base score")
            
            usvisa_model = USvisaModel(preprocessing_object=preprocessing_obj,
                                       trained_model_object=best_model_detail.best_model)
            logging.info("Created Us Visa model object with preprocessor and model")
            logging.info("Created best model file path")
            save_object(self.model_trainer_config.trained_model_file_path, usvisa_model)

            model_trainer_artifact = ModelTrainerArtifact(
                                        trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                        model_artifact = metric_artifact
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e, sys)

