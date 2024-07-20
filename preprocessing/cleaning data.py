import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_csv

#leer los datasets ----------------------------------------------
user_contract = read_csv('/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/contract.csv')
user_personal_info = read_csv('/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/personal.csv')
phone_ser = read_csv('/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/phone.csv')
internet_ser = read_csv('/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/internet.csv')

#limpiar datos (contratos) ------------------------------------------------
print(user_contract.head())

print(user_contract.info())

print(user_contract.isna().sum())