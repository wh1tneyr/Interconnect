import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet, parquet
from sklearn.model_selection import train_test_split


# leer el dataset completo escalado y codificado
data = read_parquet('files/datasets/final_provider/full_data_scaled.parquet')

# quitar las columnas de cargos totales y fecha de cancelacion
data_to_model = data.drop(['EndDate', 'TotalCharges'], axis=1)


# dividir subconjuntos de entrenamiento, prueba y validación

data_train, data_test = train_test_split(data_to_model, test_size=0.30, random_state=42)

data_valid, data_valid_2 = train_test_split(data_test, test_size=0.30, random_state=42)


