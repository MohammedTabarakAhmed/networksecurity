import sys
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig,DataValidationConfig

if __name__=="__main__":
    try:
        trainingpipelineconfig=TrainingPipelineConfig()#artifact folder path timestamp and pipeline name
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)#database name collection name file path and traintest split ratio
        dataingestion=DataIngestion(dataingestionconfig) #fetch data from mongodb save it and split it
        logging.info("Initiate the data ingestion")
        dataingestionartifact=dataingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)
        
        data_validation_config=DataValidationConfig(trainingpipelineconfig) #create path like Artifacts/timestamp/data_validation/
        data_validation=DataValidation(dataingestionartifact,data_validation_config) #first argument is train test data and second argument is folder path and settings
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation() #run the whole file and 1.check schema,2.check columns,3.drift report with k2_2samp ,4.save valid and invalid files
        logging.info("data Validation Completed")
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityException (e,sys)