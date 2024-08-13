import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet, parquet
from sklearn.model_selection import train_test_split


# Leer los subconjuntos de datos 
data_train = read_parquet('files/datasets/final_provider/data_train.parquet')
data_test = read_parquet('files/datasets/final_provider/data_test.parquet')
data_valid = read_parquet('files/datasets/final_provider/data_valid.parquet')