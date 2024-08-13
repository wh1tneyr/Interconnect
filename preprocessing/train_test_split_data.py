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

