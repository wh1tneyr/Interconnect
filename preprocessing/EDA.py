import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_csv, read_parquet
import matplotlib.pyplot as plt

""" LEER DATOS """
contract_prep = read_parquet('files/datasets/final_provider/contract_cleaned.parquet') 
internet_prep = read_csv('files/datasets/final_provider/internet.csv')
personal_prep = read_csv('files/datasets/final_provider/personal.csv')
phone_prep = read_csv('files/datasets/final_provider/phone.csv')


""" Examinar la variable target y ver el equilibrio de clases """
#crear una variable target y pasar los NO a 1 y las fechas a 0
# 1 = sigue vigente , 0=contrato terminado 

contract_prep['target'] = contract_prep['EndDate']

contract_prep['target'] = contract_prep['target'].replace('No', '1')
 
   
contract_prep[contract_prep['target'] != '1'] = '0'

contract_prep['target'] = contract_prep['target'].astype('int')

contract_prep
