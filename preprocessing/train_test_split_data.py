import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet, parquet
from sklearn.model_selection import train_test_split


# Leer el dataset completo original
full_data = pd.read_parquet('files/datasets/final_provider/full_data.parquet')


# Eliminar las columnas de fechas del df 
data_to_split = full_data.drop(['EndDate', 'BeginDate'], axis=1)


# Establecer los IDs como indices
data_to_split.set_index('customerID', inplace=True)


# Dividir subconjuntos de entrenamiento, prueba y validación

data_train, data_test_1 = train_test_split(data_to_split, test_size=0.30, random_state=42)

data_test, data_valid = train_test_split(data_test_1, test_size=0.30, random_state=42)


# Guardar los subconjuntos en archivos parquet

parquet(data_train, 'files/datasets/final_provider/data_train.parquet') 
parquet(data_test, 'files/datasets/final_provider/data_test.parquet')
parquet(data_valid, 'files/datasets/final_provider/data_valid.parquet')
