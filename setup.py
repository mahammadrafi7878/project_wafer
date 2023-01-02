from setuptools import find_packages,setup
from typing import List
REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_EDOT="-e ."

def get_requirements():
    with open (REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list=requirement_file.readlines()
        requirement_list=[requirement_name.replace("\n"," ") for requirement_name in requirement_list] 
        if HYPHEN_EDOT in requirement_list:
            requirement_list.remove(HYPHEN_EDOT)
        return requirement_list


setup(
    name="sensor",
    version="0.0.1",
    author="mahammadrafi",
    author_email="mahammadrafishaik222@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)


