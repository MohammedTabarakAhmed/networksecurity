import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()#artifact folder path timestamp and pipeline name
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)#database name collection name file path and traintest split ratio
        dataingestion=DataIngestion(dataingestionconfig) #fetch data from monfodb save it and split it
        logging.info("Initiate the data ingestion")
        dataingestionartifact=dataingestion.initiate_data_ingestion()
    except Exception as e:
        raise NetworkSecurityException (e,sys)