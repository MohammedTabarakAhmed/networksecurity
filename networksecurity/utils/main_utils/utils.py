import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os,sys,dill,pickle #same complex python objects and pickle to save python objects(models)
import numpy as np

def read_yaml_file(file_path:str)->dict: #func that takes a file_path and return a dictionary
    try:
        with open(file_path,"r") as yaml_file:
            return yaml.safe_load(yaml_file) #converts yaml into python dict
    except Exception as e:
        raise NetworkSecurityException (e,sys) from e #from e meaning see the full error history
    
def write_yaml_file(file_path:str,content:object,replace:bool=False)->dict:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path),exist_ok=True)

        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException (e,sys) from e