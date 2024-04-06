import os
import sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer

@dataclass
class DataIngestionConfig:
    raw_data_path:str = os.path.join('artifacts', 'raw_data.csv')
    modified_data_path:str = os.path.join('artifacts', 'modified_data.csv')
    train_data_path:str = os.path.join('artifacts', 'train.csv')
    test_data_path:str = os.path.join('artifacts', 'test.csv')
    
class DataIngestion:
    def __init__(self):
        self.dataingestion_config = DataIngestionConfig()
        
    def transform_text(self, document:str) -> str:
        '''
        1. Convert given text into lower case.
        2. Does the word tokenization.
        3. Remove word which contains character other than alpha numeric.
        4. Removes the stop words and punctuations from the text.
        5. Converts each words into it basic form.
        '''
        try:
            document = document.lower()
            document = nltk.word_tokenize(document)
            words = []
            for word in document:
                if word.isalnum():
                    words.append(word)
            not_a_stopwords = []
            for word in words:
                if word not in stopwords.words('english') and word not in string.punctuation:
                    not_a_stopwords.append(word)
            base_words = []
            porter_stemmer = PorterStemmer()
            for word in not_a_stopwords:
                base_words.append(porter_stemmer.stem(word))
            return ' '.join(base_words)
        except Exception as e:
            logging.info('!!! Error occured in transforming text document')
            raise CustomException(e, sys)
        
    def modify_original_df(self, raw_df):
        ''' 
        1. This function will drop the unwanted 3 columns and renames remaining 2 columns.
        2. Create 3 new columns i.e num_characters, num_words and num_sentences.
        3. Drops the duplicate column.
        4. Label encoding for dependent feature i.e 'target'.
        5. Give the transformed form of the text.
        '''
        try:
            logging.info('Modifiying original data started')
            
            modified_df = raw_df.copy(deep = True)
            logging.info('Coping original data successfully')
            
            unwanted_columns = ['Unnamed: 2','Unnamed: 3','Unnamed: 4']
            modified_df.drop(columns = unwanted_columns, inplace = True)
            logging.info('Dropped unwanted columns')
            
            renaming_columns = {
                'v1' : 'target',
                'v2' : 'text'
            }
            modified_df.rename(columns = renaming_columns, inplace = True)
            logging.info('Renamed v1 and v2 columns')
            
            modified_df['num_characters'] = modified_df['text'].apply(len)
            modified_df['num_words'] = modified_df['text'].apply(lambda x : len(nltk.word_tokenize(x)))
            modified_df['num_sentences'] = modified_df['text'].apply(lambda x : len(nltk.sent_tokenize(x)))
            logging.info('Created num_characters, num_words and num_sentences columns')
            
            encoder = LabelEncoder()
            modified_df['target'] = encoder.fit_transform(modified_df['target'])
            logging.info('Target columns encoded')
            
            modified_df = modified_df.drop_duplicates(keep = 'first')
            logging.info('Droped duplicated records')
            
            modified_df['transformed_text'] = modified_df['text'].apply(self.transform_text)
            logging.info('Created transformed text column')
            
            logging.info('Modifiying original data completed')
            return modified_df
        except Exception as e:
            logging.info('!!! Error occured in modifing original data')
            raise CustomException(e, sys)

    def initiate_data_ingestion(self):
        ''' returns training data path and test data path '''
        try:
            logging.info('Data ingestion started')
            
            raw_df = pd.read_csv('https://raw.githubusercontent.com/DarshanRokkad/Sms_Spam_Classification/master/notebooks/dataset/spam.csv', encoding = "ISO-8859-1")
            logging.info('Data read successfully')
            
            logging.info('Modifying of original data initiated')
            modified_df = self.modify_original_df(raw_df)
            
            logging.info('Train test split initiated')
            train_set, test_set = train_test_split(modified_df, test_size = 0.2, random_state = 42)
            
            file_dir = os.path.dirname(self.dataingestion_config.raw_data_path)
            os.makedirs(file_dir, exist_ok = True)
            
            logging.info('Saving csv files initiated')
            raw_df.to_csv(self.dataingestion_config.raw_data_path, index = False, header = True)
            modified_df.to_csv(self.dataingestion_config.modified_data_path, index = False, header = True)
            train_set.to_csv(self.dataingestion_config.train_data_path, index = False, header = True)
            test_set.to_csv(self.dataingestion_config.test_data_path, index = False, header = True)
            
            logging.info('Data ingestion completed')
            return (
                self.dataingestion_config.train_data_path,
                self.dataingestion_config.test_data_path
            )
        except Exception as e:
            logging('!!! Error occured in data ingestion')
            raise CustomException(e, sys)