import pandas as pd
import os, sys
sys.path.append(os.getcwd())
from funciones.funcion import encoder, scaler


""" Codificar user_contract """

user_contract = pd.read_parquet('files/datasets/final_provider/contract_cleaned.parquet')
user_contract_date_id = user_contract[['customerID', 'BeginDate', 'EndDate']]


user_contract_encoded = encoder(user_contract[['Type', 'PaperlessBilling', 'PaymentMethod']])

#cambiar la codificacion a numeros enteros
user_contract_encoded = user_contract_encoded.astype('int')

""" Escalar user_contract """

user_contract_scaled = scaler(user_contract[['MonthlyCharges', 'TotalCharges']])


#oncatenar un solo dataframe user_contract
user_contract_concat = pd.concat([user_contract_date_id, user_contract_encoded, user_contract_scaled], axis='columns')

user_contract_concat.to_parquet('files/datasets/datasets preprocessed/user_contract_scaled.parquet', engine='pyarrow', index=False)