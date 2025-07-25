import os
import sys
from dataclasses import dataclass

from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from catboost import CatBoostRegressor
from xgboost import XGBRegressor


from src.exception import CustomException
from src.logger import logging

from src.utils import save_object,evaluate_models

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info('Splitting training and test input data')

            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],train_array[:,-1],
                test_array[:,:-1],test_array[:,-1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Linear Regression": LinearRegression(),
                "KNN Classifier ": KNeighborsRegressor(),
                "Catboosting classifier": CatBoostRegressor(verbose=False),
                "Xgboost" : XGBRegressor(),
                "Adaboost ": AdaBoostRegressor(),
                "SVR" : SVR()
            }

            model_report:dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)

            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best modl name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException('No best modl     found')
            
            logging.info("Best model found")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj= best_model
            )

            predicted = best_model.predict(X_test)

            r2score = r2_score(y_test,predicted)

            return r2score, best_model_name
        except Exception as e:
            raise CustomException(e,sys)
            
