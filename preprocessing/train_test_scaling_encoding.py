import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet, parquet, scaler_train, scaler_test, encoder_train, encoder_test
from sklearn.model_selection import train_test_split


# Leer los subconjuntos de datos 
data_train = read_parquet('files/datasets/final_provider/data_train.parquet')
data_test = read_parquet('files/datasets/final_provider/data_test.parquet')
data_valid = read_parquet('files/datasets/final_provider/data_valid.parquet')


# # Filtrar los nombres de columnas segun el tipo 

cat_columns = ['Type', 'PaperlessBilling', 'PaymentMethod', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'gender', 'Partner', 'Dependents', 'MultipleLines']

num_columns = ['MonthlyCharges', 'TotalCharges']

other_columns = ['customerID', 'SeniorCitizen', 'Churn']


# Filtrar columnas segun su tipo en conjunto de entrnamiento 

train_to_encode = data_train[['Type', 'PaperlessBilling', 'PaymentMethod', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'gender', 'Partner', 'Dependents', 'MultipleLines']]

train_to_scale = data_train[['MonthlyCharges', 'TotalCharges']]

train_other_columns = data_train[['customerID', 'SeniorCitizen', 'Churn']]
