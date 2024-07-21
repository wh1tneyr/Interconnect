import pandas as pd
import os, sys
sys.path.append(os.getcwd())
from funciones.funcion import encoder


""" Codificar user_contract """
user_contract = pd.read_parquet('files/datasets/final_provider/contract_cleaned.parquet')
user_contract_to_encode = user_contract[['Type', 'PaperlessBilling', 'PaymentMethod']]
user_contract_encoded = encoder(user_contract_to_encode)

