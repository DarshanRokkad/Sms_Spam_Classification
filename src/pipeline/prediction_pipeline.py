import os
import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import load_obj, transform_text
from dataclasses import dataclass


@dataclass
class PredictPipelineConfig:
    vectorizer_path:str = os.path.join('artifacts', 'vectorizer.pkl')
    model_path:str = os.path.join('artifacts', 'model.pkl')
    
class PredictionPipeline:
    def __init__(self) -> None:
        self.prediction_pipeline_config = PredictPipelineConfig()
    
    def predict(self, text:str) -> str:
        try:
            logging.info('Prediction pipeline started')
            
            transformed_text = transform_text(text)
            logging.info('Text transformation done')
            
            vectorizer = load_obj(file_path = self.prediction_pipeline_config.vectorizer_path)
            model = load_obj(file_path = self.prediction_pipeline_config.model_path)
            logging.info('Vectorizer object and model loaded succesfully')            
            
            vector_input = vectorizer.transform([transformed_text])
            logging.info('Converted input text into vector')
            
            result = 'Spam' if (model.predict(vector_input)[0]) else 'Not Spam'
            logging.info(f'Predicted output is ** {result} **')
            
            logging.info('Prediction pipeline completed')
            return result
        except Exception as e:
            logging.info('!!! Error occured in prediction pipeline')
            raise CustomException(e, sys)


# for testing purpose
# if __name__ == '__main__':
#     prediction_pipeline = PredictionPipeline()
#     spam_text = 'SIX chances to win CASH! From 100 to 20,000 pounds txt> CSH11 and send to 87575. Cost 150p/day, 6days, 16+ TsandCs apply Reply HL 4 info'
#     ham_text = "I'm gonna be home soon and i don't want to talk about this stuff anymore tonight, k? I've cried enough today"
#     print(prediction_pipeline.predict(spam_text))