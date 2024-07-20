# import os, sys
# sys.path.append(os.getcwd())
import pandas as pd

#funcion para leer archivos csv
def read_csv(path):
    data = pd.read_csv(path)
    return data

#funcion para cambiar a formato fecha
def to_datetime(data):
    data = pd.to_datetime(data, format='%Y-%m-%d')
    return data