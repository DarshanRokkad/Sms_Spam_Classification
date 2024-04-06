import os
import sys
from src.logger import logging
from src.exception import CustomException
import dill

import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


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
    
def transform_text(document:str) -> str:
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