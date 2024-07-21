import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet


""" Leer datos escalados y codificados """

user_contract_scaled = read_parquet('files/datasets/data_scaled_encoded/contract_scaled_encoded.parquet')
#cambiar el indice a la columna de ids
user_contract_scaled.set_index('customerID', inplace=True)



user_personal_info_scaled = read_parquet('files/datasets/data_scaled_encoded/personal_scaled_encoded.parquet')
#cambiar el indice a la columna de ids
user_personal_info_scaled.set_index('customerID', inplace=True)



internet_scaled = read_parquet('files/datasets/data_scaled_encoded/internet_scaled_encoded.parquet')
#cambiar el indice a la columna de ids
internet_scaled.set_index('customerID', inplace=True)



phone_scaled = read_parquet('files/datasets/data_scaled_encoded/phone_scaled_encoded.parquet')
#cambiar el indice a la columna de ids
phone_scaled.set_index('customerID', inplace=True)


""" Concatenar un solo dataframe """
