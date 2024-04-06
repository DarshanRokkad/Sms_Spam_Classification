import os
import sys
from src.logger import logging
from src.exception import CustomException
import dill

def save_obj(file_path:str, obj) -> None:
    ''' save the given object in the given file path '''
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        dill.dump(obj, open(file_path, 'wb'))
        logging.info('Object saved successfully')
    except Exception as e:
        logging.info('!!! Error occured in save object')
        raise CustomException(e, sys)
    
def load_obj(file_path:str):
    ''' loads the object from the given file path '''
    try:
        obj = dill.load(open(file_path, 'rb'))
        logging.info('Object loaded successfully')
        return obj
    except Exception as e:
        logging.info('!!! Error occured in loading object')
        raise CustomException(e, sys)