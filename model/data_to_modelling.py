import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet


# leer el dataset completo escalado y codificado
data = read_parquet('files/datasets/final_provider/full_data_scaled.parquet')

