# Librerias 
import pandas as pd
import os, sys
sys.path.append(os.getcwd())

# Funciones 
from funciones.funcion import read_parquet, parquet

# Modelos 
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier


# Leer el dataset completo 
full_data_scaled = read_parquet('files/datasets/final_provider/datasets_scaled_encoded/full_data_scaled.parquet')

# Eliminar la columna de fechas del df
full_data = full_data_scaled.drop(['BeginDate', 'EndDate'], axis=1)

# Establecer la coluna IDs como indice del df
full_data.set_index('customerID', inplace=True)

# Definir las caracteristicas y el objetivo
features = full_data.drop(['Churn'], axis=1)
target = full_data['Churn']