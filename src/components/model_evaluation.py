import os
import sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

from sklearn.metrics import accuracy_score, precision_score
from src.utils import load_obj
import mlflow
import mlflow.sklearn
from urllib.parse import urlparse


@dataclass
class ModelEvaluationConfig:
    trained_model_file_path:str = os.path.join('artifacts','model.pkl')

class ModelEvaluation:   
    def __init__(self):
        self.model_evaluation_config = ModelEvaluationConfig()
     
    def evaluation_metrics(self, actual, predicted):
        accuracy = accuracy_score(actual, predicted)
        precision = precision_score(actual, predicted)
        return (accuracy, precision)
    
    def initiate_model_evaluation(self, test_arr):
        try:
            logging.info('Model evaluation started')
            
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]
            model = load_obj(self.model_evaluation_config.trained_model_file_path)
            logging.info('Model loaded successfully')
            
            with mlflow.start_run(run_name = 'Best Model'):
                prediction = model.predict(x_test)
                accuracy, precision = self.evaluation_metrics(y_test, prediction)                
                mlflow.log_metric('Precision', precision)
                mlflow.log_metric('Accuracy', accuracy)
                # remote_server_uri="https://dagshub.com/DarshanRokkad/Mlflow_Daghub_Practise.mlflow"
                # mlflow.set_tracking_uri(remote_server_uri)            
                tracking_uri_type_store = urlparse(mlflow.get_tracking_uri()).scheme
                logging.info(f"{tracking_uri_type_store}")
                if tracking_uri_type_store != 'file':
                    mlflow.sklearn.log_model(model, 'model', registered_model_name = "SpamClassifierModel")       # Register the model
                else:
                    mlflow.sklearn.log_model(model, 'model')
            
            logging.info('Model evaluation completed')
        except Exception as e:
            logging.info('!!! Error in model evaluation')
            CustomException(e, sys)