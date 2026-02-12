import os,sys,json,certifi
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca=certifi.where() #certifi ensures if the http website is secure and verifies it (ssl/tls)

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException (e,sys)
        
    def csv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)  # corrected from read_clipboard to read_csv
            data.reset_index(drop=True,inplace=True)
            records=data.T.to_json()
            records=list(json.loads(data.T.to_json()).values()) #json.loads(...)=converts data string to python dictionary and also .T because beaucse3 it converts row to column and thats how mongodb expects data to be and also values because we dont want index or anythoing
            return records
        except Exception as e:
            raise NetworkSecurityException (e,sys)
                
    def insert_data_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL) #create a mongo server so you can acccess databasse and collection sotre inside(monog_client)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records) #records(each dict is one record and list is all records together) and collection(table) which is inside the database(folder)
            return len(self.records)  # Return the number of records (dictionaries) inserted into the collection!
        except Exception as e:
            raise NetworkSecurityException (e,sys)
            
if __name__=="__main__":
    FILE_PATH=r"Network_Data\phisingData.csv"
    DATABASE="AHMEDAI"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()

    records=networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(records)
    number_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(number_of_records)#stores the number of records insdide "number_of_records"