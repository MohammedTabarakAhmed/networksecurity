'''
it is used by setup tools to define the config of pro,such as its metadata,dependecies,and more
{essential} part of packagig and distributing python projects.}
'''

from setuptools import find_packages,setup #find_packages=__init__.py and setup =is the blueprint for packaging your Python project so others can install and use it.
from typing import List

def get_requirements()-> List[str]: #This function will return a list of str
    requirements_lst:List[str]=[]
    try:
        with open("requirements.txt",'r') as file:
        #read lines from the file
            lines=file.readlines()
        #process each lines
        for line in lines:
            ##ignore empty lines and -e .
            requirement=line.strip() 
            if requirement and requirement != '-e .': #-e . is editable mode will refer to the setup.py file and execurte it will not consider -e .
                requirements_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    
    return requirements_lst

print(get_requirements())

setup(
    name="NetworkSecurity",
    version='0.0.0.1',
    author="Ahmed",
    author_email="tabarakahmed030@gmail.com",
    packages=find_packages(), #will find all the packages(__init__.py)
    install_requires=get_requirements() #which dependencies to be installed
)