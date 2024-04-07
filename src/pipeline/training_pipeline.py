import sys
from src.logger import logging
from src.exception import CustomException

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_training import ModelTrainer

class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
            return train_data_path, test_data_path
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_data_transformation(self, train_data_path:str, test_data_path:str):
        try:
            data_transformation = DataTransformation()
            train_arr, test_arr = data_transformation.initiate_data_transformation(train_data_path, test_data_path)
            return train_arr, test_arr
        except Exception as e:
            raise CustomException(e, sys)
    
    def start_model_trainer(self, train_arr, test_arr) -> None:
        try:
            model_trainer = ModelTrainer()
            model_trainer.initiate_model_training(train_arr, test_arr)
        except Exception as e:
            raise CustomException(e, sys)
    
    def train_model(self):
        try:
            logging.info('Training pipeline started')
            
            logging.info('Data ingestion initiated')
            train_data_path, test_data_path = self.start_data_ingestion()
            logging.info('Data transformation initiated')
            train_arr, test_arr = self.start_data_transformation(train_data_path, test_data_path)
            logging.info('Model trainer initiated')
            self.start_model_trainer(train_arr, test_arr)
            
            logging.info('Training pipeline completed')
        except Exception as e:
            logging.info('!!! Error occured while training model')
            raise CustomException(e, sys)


# for testing purpose 
# if __name__ == '__main__':
#     training_pipeline = TrainingPipeline()
#     training_pipeline.train_model()