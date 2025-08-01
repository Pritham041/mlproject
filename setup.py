#Helps to building our application has package
from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)->List[str]:
    """
    This function will return the list of requirements
    """
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [ req.replace("\n","") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
            
    return requirements

# This is the setup file for the ML project
setup(
    name='mlproject',
    version='0.0.1',
    author='Pritham',
    author_email='1782959prithamreddy@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt'),
    description='A small ML project'
)