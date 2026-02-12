from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import DataIngestionArtifact

#confiugration of Data Ingestion Config
from networksecurity.entity.config_entity import DataIngestionConfig
import os,sys,pymongo
from typing import List
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
            #DataIngestionConfig object so it knows paths database names etc inside the class DataIngestion.
        except Exception as e:
            raise NetworkSecurityException (e,sys)
        
    def expect_collection_as_dataframe(self): #reads collection data from mongodb and converts into a dataframe and removes _id and na with NaN and return the clean dataframe
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) #connect to my mongodb server with the url mentioned inside .env
            collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list(): #id is unique identifier in mongodb whcih we dont need when we do ML
                df = df.drop(columns=["_id"])
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException (e,sys)

    def export_data_into_feature_store(self,dataframe=pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path

            #create folder
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException (e,sys)
        
    def split_data_as_train_test(self,dataframe=pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of DataIngestionClass")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True) #make a foldefr for train test csv called dir_path where train and tst csv was given in networksecurity\constants\trianing_pipline
            logging.info("Exportiong train and test file path")

        except  Exception as e:
            raise NetworkSecurityException (e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe=self.expect_collection_as_dataframe() #fecth data from mongo db as dataframe
            dataframe=self.export_data_into_feature_store(dataframe) #save dataframe as feautre store CSV and keep it
            self.split_data_as_train_test(dataframe) #split the train and test data and make dir_path folder
            artifact = DataIngestionArtifact(
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path
                )
            return artifact
        
        except Exception as e:
            raise NetworkSecurityException (e,sys)
        
    