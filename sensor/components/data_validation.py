from sensor.entity import config_entity,artifact_entity 
from sensor.logger import logging
from sensor.exception import SensorException 
from scipy.stats import ks_2samp 
from typing import Optional 
import os,sys 
import pandas as pd 
import numpy as np 
from sensor import utils    



class DataValidation:
    def __init__(self,data_validation_config:config_entity.DataValidationConfig,data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>' *20} DATA VALIDATION {'<<'*20}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.validation_error=dict()

        except Exception as e:
            raise SensorException(e, sys)   



    def drop_missing_values_columns(self,df,report_key_name):
        try:
            threshold=self.data_validation_config.missing_threshold
            null_report=df.isna().sum()/df.shpe[0]
            logging.info(f"selecting column nane which containing null above {threshold}")
            drop_column_names=null.report[null_report>threshold].index

            logging.info(f"column names to drop{list(drop_column_names)}")
            self.validation_error[report_key_name]=list(drop_column_names)
            df.drop(list(drop_column_names),axis=1,inplace=True)

            if len(df.columns)==0:
                return None
            return df
        except Exception as e:
            raise SensorException(e, sys)  


    def is_required_columns_exists(self,base_df,current_df,report_key_name):
        try:
            base_columns=base_df.columns
            current_columns=current_df.columns 

            missing_columns=[]
            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"columns:[{base} is not available")
                    missing_columns.append(base_column)

                if len(missing_columns)>0:
                    self.validation_error[report_key_name]=missing_columns
                    return False
                return True
        except Exception as e:
            raise SensorException(e, sys)


    def data_drift(self,base_df,current_df,report_key_name):
        try:
            drift_report-=dict() 
            base_columns=base_df.columns
            current_columns=current_df.columns

            for base_column in base_columns:
                base_data,current_data=base_df[base_column],current_df[base_column]   

                logging.info(f"Hypothesis {base_column}: {base_data.dtype}, {current_data.dtype} ")
                same_distribution =ks_2samp(base_data,current_data)

                if same_distribution.pvalue>0.05:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution": True
                    }

                else:
                    drift_report[base_column]={
                        "pvalues":float(same_distribution.pvalue),
                        "same_distribution":False
                    }

            self.validation_error[report_key_name]=drift_report

        except Exception as e:
            raise SensorException(e, sys)   




    def initiate_data_validation(self):
        try:
            logging.info(f"Reading base dataframe")
            base_df=pd.read_csv(self.data_validation_config.base_file_path)
            base_df.replce({"na":np.NAN},inplace=True)
            logging.info(f"rep;aced na values with nan")

            logging.info(f"drop null values columns from base df")
            base_df=self.drop_missing_values_columns(df=base_df, report_key_name="missing_values_within_base_dataset")
            
            logging.info((f"reading train dataframe"))
            train_df=pd.read_csv(self.data_validation_config.train_file_path)
            logging.info(f"reading test dataframe")
            test_df=pd.read_csv(self.data_validation_config.test_file_path) 

            logging.info(f"dropping null vakluecolumns from  train df")
            train_df=self.drop_missing_values_columns(df=train_df, report_key_name="missing_values_within_train_dataset")
            logging.info(f"dropping missing value columns in test dataset")
            test_df=self.drop_missing_values_columns(df=test_df, report_key_name="missing_values_within_test_dataset") 

            exclude_columns=["class"]
            base_df=utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            train_df=utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            test_df=utils.convert_columns_float(df=test-df, exclude_columns=exclude_columns)



            logging.info(f"is all required columns present in train df")
            train_df_column_status=self.is_required_columns_exists(base_df=base_df, current_df=train_df, report_key_name="missing_columns_within_train_dataset")
            logging.info(f"is required columns exisy in test df")
            test_df_column_status=self.is_required_columns_exists(base_df=base_df, current_df=test_df, report_key_name="missing_columns_within_test_dataset")

            if train_df_column_status:
                logging.info("if all required columns are present in train df checkinhgh for data drift")
                self.data_drift(base_df=base_df, current_df=train_df, report_key_name="data_drift_within_train_dataset")

            if test_df_column_status:
                logging.info(f"if all required columns are exist in test df then checking for data drift")
                self.data_drift(base_df=base_df, current_df=test_df, report_key_name="data_drift_within_test_dataset")



            logging.info("Write reprt in yaml file")
            utils.write_yaml_file(file_path=self.data_validation_config.report_file_path,
            data=self.validation_error)



            data_validation_artifact=artifact_entity.DataValidationArtifact(report_file_path=self.data_validation_config.report_file_path)
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise SensorException(e, sys)


        except Exception as e:
            raise SensorException(e, sys)

