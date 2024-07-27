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

# concatenar cotract_prep e internet_prep (sin escalar ni codificar)
merge_1 = contract_prep.merge(internet_prep, on='customerID', how='left')

# comprobar valores ausentes 
merge_1.isna().sum()

# suponiendo que los ausentes corresponden a clientes que no pagan por servicios de internet,
# rellenar ausentes con 'No'

merge_1 = merge_1.fillna('No')
merge_1.isna().sum()

# concatenar merge_1 con personal_prep

merge_2 = merge_1.merge(personal_prep, on='customerID', how='left')

