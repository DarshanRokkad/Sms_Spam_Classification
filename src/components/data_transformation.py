import os
import sys
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd
from src.utils import save_obj
from sklearn.feature_extraction.text import TfidfVectorizer

@dataclass
class DataTransformationConfig:
    vectorizer_obj_file_path:str = os.path.join('artifacts', 'vectorizer.pkl')

class DataTransformation:
    def __init__(self):
        self.datatransformation_config = DataTransformationConfig()
    
    def initiate_data_transformation(self, train_data_path:str, test_data_path:str):
        try:
            logging.info('Data transformation started')
            
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)
            train_df.dropna(inplace = True)
            test_df.dropna(inplace = True)
            logging.info('Training data and test data read successfully')
            
            logging.info('Separating independent and dependent feature')
            Y = 'target'
            X_train_df = train_df.drop(columns = [Y], axis = 1)
            Y_train_arr = np.array(train_df[Y])
            X_test_df = test_df.drop(columns = [Y], axis = 1)
            Y_test_arr = np.array(test_df[Y])
            
            logging.info('Data preprocessing initiated')
            vectorizer = TfidfVectorizer(max_features=3000)
            X_train_arr = vectorizer.fit_transform(X_train_df['transformed_text']).toarray()
            X_test_arr = vectorizer.transform(X_test_df['transformed_text']).toarray()
            train_arr = np.c_[X_train_arr, Y_train_arr]
            test_arr = np.c_[X_test_arr, Y_test_arr]
            
            logging.info('Saving vectorizer object')
            save_obj(
                file_path = self.datatransformation_config.vectorizer_obj_file_path,
                obj = vectorizer
            )
            
            logging.info('Data transformation completed')
            return (train_arr, test_arr)
        except Exception as e:
            logging.info('!!! Error occured in during data transformation')
            raise CustomException(e, sys)