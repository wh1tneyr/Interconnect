import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet, parquet, scaler_train, scaler_test, encoder_train, encoder_test
from sklearn.model_selection import train_test_split


# Leer los subconjuntos de datos 
data_train = read_parquet('files/datasets/final_provider/data_train.parquet')
data_test = read_parquet('files/datasets/final_provider/data_test.parquet')
data_valid = read_parquet('files/datasets/final_provider/data_valid.parquet')


# Filtrar columnas segun su tipo en conjunto de entrnamiento 

train_to_encode = data_train[['Type', 'PaperlessBilling', 'PaymentMethod', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'gender', 'Partner', 'Dependents', 'MultipleLines']]

train_to_scale = data_train[['MonthlyCharges', 'TotalCharges']]

train_other_columns = data_train[['customerID', 'Churn', 'SeniorCitizen']]


# Codificar conjunto de entrenamiento 
train_encoded = encoder_train(train_to_encode)

# Agregarle los IDs para realizar un merge luego
train_encoded['customerID'] = data_train['customerID']

# Escalar conjunto de entrenamiento
train_scaled = scaler_train(train_to_scale)

# Agregarle los IDs para realizar un merge luego
train_scaled['customerID'] = data_train['customerID']

# Unir todo en nuevo conjunto de entrenamiento escalado y codificado
merge_1 = train_other_columns.merge(train_encoded, on='customerID')

train_scaled_encoded = merge_1.merge(train_scaled, on='customerID')