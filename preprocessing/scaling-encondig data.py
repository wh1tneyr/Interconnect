import pandas as pd
import os, sys
sys.path.append(os.getcwd())
from funciones.funcion import encoder, scaler, read_csv


""" CODIFICAR 'user_contract' """

user_contract = pd.read_parquet('files/datasets/final_provider/contract_cleaned.parquet')
user_contract_date_id = user_contract[['customerID', 'BeginDate', 'EndDate']]


user_contract_encoded = encoder(user_contract[['Type', 'PaperlessBilling', 'PaymentMethod']])

#cambiar la codificacion a numeros enteros
user_contract_encoded = user_contract_encoded.astype('int')


""" ESCALAR 'user_contract' """
user_contract_scaled = scaler(user_contract[['MonthlyCharges', 'TotalCharges']])

#oncatenar un solo dataframe user_contract
user_contract_concat = pd.concat([user_contract_date_id, user_contract_encoded, user_contract_scaled], axis='columns')

#guardar en un archivo parquet
user_contract_concat.to_parquet('files/datasets/data scaled-encoded/contract_scaled_encoded.parquet', engine='pyarrow', index=False)


""" CODIFICAR 'user_personal_info' """

user_personal_info = read_csv('files/datasets/final_provider/personal.csv')
user_personal_info_id = user_personal_info[['customerID', 'SeniorCitizen']]

user_personal_encoded = encoder(user_personal_info[['gender', 'Partner', 'Dependents']])

#cambiar la codificacion a num enteros 
user_personal_encoded = user_personal_encoded.astype('int')

#contatenar un solo dataframe
user_personal_concat = pd.concat([user_personal_info_id, user_personal_encoded], axis='columns')

#guardar en un arquivo parquet
user_personal_concat.to_parquet('files/datasets/data scaled-encoded/personal_scaled_encoded.parquet', engine='pyarrow', index=False)



""" CODIFICAR 'internet' """

internet = read_csv('files/datasets/final_provider/internet.csv')
internet_id = internet['customerID']
internet_to_encode = internet.drop(['customerID'], axis=1)

internet_encoded = encoder(internet_to_encode)

#convertir a num enteros 
internet_encoded = internet_encoded.astype('int')

#concatenar un solo dataframe 
internet_concat = pd.concat([internet_id, internet_encoded], axis='columns')

#guardar en un archivo parquet
internet_concat.to_parquet('files/datasets/data scaled-encoded/internet_scaled_encoded.parquet', engine='pyarrow', index=False)