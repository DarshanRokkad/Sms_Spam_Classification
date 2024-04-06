import os
import sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from src.utils import save_obj, evaluate_models

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB , MultinomialNB , BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score , precision_score


@dataclass
class ModelTrainerConfig:
    trained_model_file_path:str = os.path.join('artifacts', 'model.pkl')
    
class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_training(self, train_array, test_array) -> None:
        try:
            logging.info('Model training started')
            
            logging.info('Train test split initiated')
            x_train, y_train, x_test, y_test =(
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )
            
            logging.info('All model creation initiated')
            models = {
                'Logistic Regression' : LogisticRegression(solver = 'liblinear', penalty ='l1'),
                'Bernoulli Naive Bayes' : BernoulliNB(),
                'Gaussian Naive Bayes' : GaussianNB(),
                'Multinomial Naive Bayes' : MultinomialNB(),
                'Support Vector Classifier' : SVC(kernel = 'sigmoid', gamma = 1.0),
                'Decision Tree Classifier' : DecisionTreeClassifier(max_depth = 5),
                'Extra Tree Classifier' : ExtraTreesClassifier(n_estimators = 50, random_state = 2),
                'Random Forest Classifier' : RandomForestClassifier(n_estimators = 50, random_state = 2),
                'Bagging Classifier' : BaggingClassifier(n_estimators = 50, random_state = 2),
                'Ada Boost Classifier' : AdaBoostClassifier(n_estimators = 50, random_state = 2),
                'Gradient Boosting Classifier' : GradientBoostingClassifier(n_estimators = 50,random_state = 2),
                'XG Boost Classifier' : XGBClassifier(n_estimators = 50,random_state = 2)
            }
            
            performance_df = evaluate_models(x_train, y_train, x_test, y_test, models)
            logging.info(f'\n{performance_df}\n')
            best_model_name, precision, accuracy = performance_df.iloc[0]['Algorithm'], performance_df.iloc[0]['Precision'], performance_df.iloc[0]['Accuracy']
            best_classifier = models[best_model_name]
            logging.info(f'Best model is {best_model_name} with precision {precision} and accuracy {accuracy}')
            
            logging.info('Training best model')
            best_classifier.fit(x_train, y_train)
            
            logging.info(f'Saving {best_model_name} : {best_classifier} model')
            save_obj(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_classifier
            )
            
            logging.info('Model training completed')
        except Exception as e:
            logging.info('!!! Error occured in model trainer')
            CustomException(e, sys)