from setuptools import setup, find_packages
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='watergrid-python',
    version='0.0.0',
    description='Distributed streaming data pipeline',
    long_description=long_description,
    url='https://github.com/ARMmaster17/watergrid-python',
    author='ARMmaster17',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["watergrid"],
    include_package_data=True,
    install_requires=[]
)