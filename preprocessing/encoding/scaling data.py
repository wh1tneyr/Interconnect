import pandas as pd
import os, sys
sys.path.append(os.getcwd())
from funciones.funcion import encoder, scaler


""" Codificar user_contract """
user_contract = pd.read_parquet('files/datasets/final_provider/contract_cleaned.parquet')
user_contract_encoded = encoder(user_contract[['Type', 'PaperlessBilling', 'PaymentMethod']])

#cambiar la codificacion a numeros enteros
user_contract_encoded = user_contract_encoded.astype('int')

