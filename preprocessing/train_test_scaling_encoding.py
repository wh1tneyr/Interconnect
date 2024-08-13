import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet, parquet, scaler_train, scaler_test, encoder_train, encoder_test
from sklearn.model_selection import train_test_split


# Leer los subconjuntos de datos 
data_train = read_parquet('files/datasets/final_provider/data_train.parquet')
data_test = read_parquet('files/datasets/final_provider/data_test.parquet')
data_valid = read_parquet('files/datasets/final_provider/data_valid.parquet')


# Filtrar columnas segun tipo en conjunto de entrnamiento 

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



# Filtrar columnas segun tipo en conjunto de prueba

test_to_encode = data_test[['Type', 'PaperlessBilling', 'PaymentMethod', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'gender', 'Partner', 'Dependents', 'MultipleLines']]

test_to_scale = data_test[['MonthlyCharges', 'TotalCharges']]

test_other_columns = data_test[['customerID', 'Churn', 'SeniorCitizen']]


# Codificar conjunto de entrenamiento 
test_encoded = encoder_test(train_to_encode, test_to_encode)

# Agregarle los IDs para realizar un merge luego
test_encoded['customerID'] = data_test['customerID']

# Escalar conjunto de entrenamiento
test_scaled = scaler_test(train_to_scale, test_to_scale)

# Agregarle los IDs para realizar un merge luego
test_scaled['customerID'] = data_test['customerID']

# Unir todo en nuevo conjunto de entrenamiento escalado y codificado
merge_1 = test_other_columns.merge(test_encoded, on='customerID')

test_scaled_encoded = merge_1.merge(test_scaled, on='customerID')


# Filtrar columnas segun tipo en conjunto de validacion

valid_to_encode = data_valid[['Type', 'PaperlessBilling', 'PaymentMethod', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'gender', 'Partner', 'Dependents', 'MultipleLines']]

valid_to_scale = data_valid[['MonthlyCharges', 'TotalCharges']]

valid_other_columns = data_valid[['customerID', 'Churn', 'SeniorCitizen']]


# Codificar conjunto de entrenamiento 
valid_encoded = encoder_test(train_to_encode, valid_to_encode)

# Agregarle los IDs para realizar un merge luego
valid_encoded['customerID'] = data_valid['customerID']

# Escalar conjunto de entrenamiento
valid_scaled = scaler_test(train_to_scale, valid_to_scale)

# Agregarle los IDs para realizar un merge luego
valid_scaled['customerID'] = data_valid['customerID']

# Unir todo en nuevo conjunto de entrenamiento escalado y codificado
merge_1 = valid_other_columns.merge(valid_encoded, on='customerID')

valid_scaled_encoded = merge_1.merge(valid_scaled, on='customerID')
