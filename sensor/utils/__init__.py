import pandas as pd 
from sensor.config import mongo_client
from sensor.logger import logging 
from sensor.exception import SensorException 
import os,sys 
import yaml

def get_collection_as_dataframe(database_name,collection_name):
    try:
        logging.info(f"reading from database{database_name} qand collection :{collection_name}")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"found columns:{df.columns}")
        if "_id" in df.columns:
            logging.info("dropping _id column")
            df=df.drop('_id',axis=1)
        return df 

    except exception as e:
        raise SensorException(e, sys)




def write_yaml_file(file_path,data):
    try:
        file_dir=os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path, "w")as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise SensorException(e, sys)



def convert_columns_float(df,exclude_columns):
    try:
        for column in  df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype(float)
    except Exception as e:
        raise SensorException(e, sys)