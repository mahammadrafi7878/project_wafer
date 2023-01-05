import pandas as pd 
import pymongo
import json
from dataclasses import dataclass
import os 

TARGET_COLUMN="class"


@dataclass 
class EnvironmentVariable:
    mongo_db_url=os.getenv("MONGO_DB_URL") 

env_variable=EnvironmentVariable() 
mongo_client=pymongo.MongoClient(env_variable.mongo_db_url)
