# SOBERS Assignment

### Introduction
For this assignment our client has a web application that deals with accounting.
One of the features is to import csv's with bank statements.

In this assignment, 
There is already a version that runs for a single bank.
In this assignment a version is needed that is not a POC(Proof of Concept) but will be used as the main point for the bank integration feature. There for maintenance and extensibility will be important. 
Your task will be to create a script that parses data from different banks.
In the future the client would like to intergrate with integrate banks.

### How to run script
```
python3 data_parser.py bank1.csv bank2.csv bank3.csv
```

### How to run unit tests
```
python3 -m unittest -v tests_data_parser.py
```

### Requirements
Python: 3.7 or higher. It is related to the ordering mechanism of elements in dict
