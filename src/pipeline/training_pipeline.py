import sys
from src.logger import logging
from src.exception import CustomException

from src.components.data_ingestion import DataIngestion


class TrainingPipeline:
    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion()
            train_data_path, test_data_path = data_ingestion.initiate_data_ingestion()
            return train_data_path, test_data_path
        except Exception as e:
            raise CustomException(e, sys)
    
    def train_model(self):
        try:
            logging.info('Training pipeline started')
            
            logging.info('Data ingestion initiated')
            train_data_path, test_data_path = self.start_data_ingestion()
            
            logging.info('Training pipeline completed')
        except Exception as e:
            logging.info('!!! Error occured while training model')


# for testing purpose 
if __name__ == '__main__':
    training_pipeline = TrainingPipeline()
    training_pipeline.train_model()