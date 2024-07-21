import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet


""" Leer datos escalados y codificados """

user_contract_scaled = read_parquet('files/datasets/data_scaled_encoded/contract_scaled_encoded.parquet')
#cambiar el indice a la columna de ids
#user_contract_scaled.set_index('customerID', inplace=True)



user_personal_info_scaled = read_parquet('files/datasets/data_scaled_encoded/personal_scaled_encoded.parquet')
#cambiar el indice a la columna de ids
#user_personal_info_scaled.set_index('customerID', inplace=True)



internet_scaled = read_parquet('files/datasets/data_scaled_encoded/internet_scaled_encoded.parquet')
#cambiar el indice a la columna de ids
#internet_scaled.set_index('customerID', inplace=True)



phone_scaled = read_parquet('files/datasets/data_scaled_encoded/phone_scaled_encoded.parquet')
#cambiar el indice a la columna de ids
#phone_scaled.set_index('customerID', inplace=True)


""" Concatenar un solo dataframe """
user_contract_scaled.info()
user_personal_info_scaled.info()

#concatenando contratos con personal info
contract_personal_merged = user_contract_scaled.merge(user_personal_info_scaled, on='customerID')

#concatenando internet cob phone
internet_phone_merged = internet_scaled.merge(phone_scaled, how='outer', on='customerID')


#datos ausentes en internet-phone
nan_internet_phone = internet_phone_merged[internet_phone_merged['InternetService'].isna()]

#comprobando en que dataframe se encuentran presentes los datos ausentes 
nan_internet_phone['customerID'].isin(phone_scaled['customerID']).sum()
        
""" """ """ Todos los datos ausentes en 'internet_phone_merge' estan presentes en dataset 'phone_scaled' excepto los de la columna 'MultipleLines', que estan presentes en 'internet_saceld' """ """ """

# TODO rellenar los datos ausentes en internet_phone_merged






columns_nan_phone_scaled = ['InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies'] 

columns_nan_internet_scaled = 'MultipleLines'

