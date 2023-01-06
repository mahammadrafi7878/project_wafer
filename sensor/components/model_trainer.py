from sensor.entity import artifact_entity,config_entity 
from sensor.logger import logging 
from sensor.exception import SensorException 
from typing import Optional 
import os,sys 
from sensor import utils 
from xgboost import XGBClassifier 
from sklearn.metrics import f1_score  



class ModelTrainer:

    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        
        except Exception as e:
            raise SensorException(e, sys)


    def train_model(self,x,y):
        try:
            xgb_clf=XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf 

        except Exception as e:
            raise SensorException( e, sys)  




    def initiate_model_trainer(self):
        try:
            logging.info(f"loading train and test array")
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)


            logging.info(f"splitting input and target feature from both train and test set")
            x_train,y_train= train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]  

            logging.info(f"train the model")
            model=self.train_model(x=x_train, y=y_train)

            logging.info(f"calculating f1_score for train data")
            yhat_train=model.predict(x_train)
            f1_train_score=f1_score(y_true=y_train,y_pred=yhat_train)

            logging.info(f"calculating f1 test score")
            yhat_test=model.predict(x_test)
            f1_test_score=f1_score(y_true=y_test, y_pred=yhat_test)


            logging.info(f"f1_train_score:{f1_train_score}  and f1_test_score is : {f1_test_score}")


            logging.info(f"checking our model is underfitting or overfitting or goood model")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good as it not giving good accuracy score  i.e  expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {f1_test_score}")

            logging.info(f"checking our model is overfitting or not")
            diff=abs(f1_train_score-f1_test_score)
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"train and test score difference is :{diff} is more than overfitting threshold :{self.model_trainer_config.overfitting_threshold}")


            logging.info(f"saving model-object")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)


            logging.info("preparing the artifact")
            model_trainer_artifact  = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path, 
            f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)




        except Exception as e:
            raise SensorException(e, sys)