import os
from pathlib import Path

list_of_files = [
    
    'notebooks/experiments.ipynb',                      # folder for all jupyter notebooks
    
    'artifacts/.gitkeep',                               # folder to store csv and pickle files
    
    'requirements.txt',                                 # requirements for projects 
      
    'src/__init__.py',                                  # main source code folder
    'src/components/__init__.py',                       # components
    'src/components/data_ingestion.py',
    'src/components/data_transformation.py',
    'src/components/model_training.py',
    'src/components/model_evaluation.py',    
    'src/pipeline/__init__.py',                         # pipelines
    'src/pipeline/training_pipeline.py',
    'src/pipeline/prediction_pipeline.py',
    'src/exception.py',                                 # custom exception handling
    'src/logger.py',                                    # logging
    'src/utils.py',                                     # common functions
    
    'setup.py',                                         # for converting project into package 
    
    'application.py',                                   # for creating the flask application 
    'templates/home.html',                             # for creating the ui for the application
    'static/css/style.css',
    
    'images/.gitkeep',                                  # supporting images for github readme

]

# let's create the project structure
for file_path in list_of_files:
    file_path = Path(file_path)
    file_dir, file_name = os.path.split(file_path)
    
    if file_dir != '':
        os.makedirs(file_dir, exist_ok = True)
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        with open(file_path, 'w') as f:
            pass    # creating an empty file