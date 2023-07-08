"""
In Python, setup.py is a module used to build and distribute Python packages.
It typically contains information about the package, such as its name, version, and dependencies,
as well as instructions for building and installing the package.

"""
# importing the setup files and the packages. 
from setuptools import find_packages,setup
from typing import List

HYPEN_E_DOT='-e .'

# Function to get the list of all the requirements to be installed from requirements.txt file. 
def get_requirements(file_path:str)->List[str]:
    requirements=[]
    # Open the requirements.txt file and read line by line. 
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements

                                                        

setup(
    name='Zomato Delivery Time Prediction',
    version='0.0.1',
    author='Rohit',
    author_email='my-email-id',
    install_requires=get_requirements('requirements.txt'),
    packages=find_packages()
)
