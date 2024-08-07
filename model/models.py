import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet, parquet


# leer conjunto de entrenamiento
data_train = read_parquet('files/datasets/final_provider/data_train.parquet')

# definir las caracteristicas y el objetivo
train_features = data_train.drop(['Churn'], axis=1)
train_target = data_train['Churn']

# leer conjunto de prueba
data_test = read_parquet('files/datasets/final_provider/data_test.parquet')

# definir caracteristicas y objetivo
test_features = data_test.drop(['Churn'], axis=1)
test_target = data_test['Churn']

# leer conjunto de validacion
data_valid = read_parquet('files/datasets/final_provider/data_valid.parquet')

# definir caracteristicas y objetivo
valid_features = data_valid.drop(['Churn'], axis=1)
valid_target = data_valid['Churn']