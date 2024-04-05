import logging
import os
from datetime import datetime

LOG_FOLDER_NAME = f'{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}'
logs_folder_path = os.path.join(os.getcwd(), 'logs', LOG_FOLDER_NAME)
os.makedirs(logs_folder_path, exist_ok = True)

logs_file_name = f'{LOG_FOLDER_NAME}.log'

LOG_FILE_PATH = os.path.join(logs_folder_path, logs_file_name)

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)