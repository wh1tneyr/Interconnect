import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet


""" Leer datos escalados y codificados """

user_contract_scaled = read_parquet('files/datasets/data_scaled_encoded/contract_scaled_encoded.parquet')
user_personal_info_scaled = read_parquet('files/datasets/data_scaled_encoded/personal_scaled_encoded.parquet')
internet_scaled = read_parquet('files/datasets/data_scaled_encoded/internet_scaled_encoded.parquet')
phone_scaled = read_parquet('files/datasets/data_scaled_encoded/phone_scaled_encoded.parquet')


""" Concatenar un solo dataframe """
user_contract_scaled.info()
user_personal_info_scaled.info()

#concatenando contratos con personal info
contract_personal_merged = user_contract_scaled.merge(user_personal_info_scaled, on='customerID')

#concatenando internet cobn phone
internet_phone_merged = internet_scaled.merge(phone_scaled, how='outer', on='customerID')

#concatenar un solo dataframe
full_data_raw = contract_personal_merged.merge(internet_phone_merged, how='left', on='customerID')
full_data_no_nan = full_data_raw.dropna().reset_index(drop=True)
full_data_fillna_unknown = full_data_raw.fillna('unknown')

