# Librerias 
import pandas as pd
import os, sys
sys.path.append(os.getcwd())

# Funciones 
from funciones.funcion import read_parquet, parquet, model_eval
from sklearn.metrics import roc_auc_score, accuracy_score

# Modelos 
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier


# Leer el dataset completo 
full_data = read_parquet('files/datasets/final_provider/full_data.parquet')
