from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_name:str) -> List[str]:
    with open(file_name, 'r') as file:
        requirements = [requirement.replace('\n', '') for requirement in file.readlines()]
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name = 'sms_spam_classification',
    version = '0.0.1',
    author = 'DarshanRM',
    author_email = 'darshanrokkad2003@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)