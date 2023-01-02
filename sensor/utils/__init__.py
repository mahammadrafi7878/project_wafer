import pandas as pd 
from sensor.config import mongo_client
from sensor.logger import logging 
from sensor.exception import SensorException 
import os,sys 


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