# Librerias 
import pandas as pd
import os, sys
sys.path.append(os.getcwd())

# Funciones 
from funciones.funcion import read_parquet, parquet, encoder_train, scaler_train
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

# Modelos 
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier


# Leer el dataset completo 
full_data = read_parquet('files/datasets/final_provider/full_data.parquet')

# # Codificar y esacalar dataset completo
encoder = OrdinalEncoder()
scaler = StandardScaler()


# filtrar las columnas categoricas para codificar
data_to_encode = full_data[['customerID', 'Type', 'PaperlessBilling', 'PaymentMethod', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'gender', 'Partner', 'Dependents', 'MultipleLines']]

# filtrar las columnas numericas para escalar
data_to_scale = full_data[['MonthlyCharges', 'TotalCharges']]

# filtrar las columnas que no necesitan codificacion ni escala
data_other_columns = full_data[['customerID', 'BeginDate', 'EndDate', 'SeniorCitizen', 'Churn']]


# # codificar las variables categoricas
data_encoded = encoder_train(data_to_encode)

# agregar columna de IDs
data_encoded['customerID'] = full_data['customerID']


# # escalar variable numericas
data_scaled = scaler_train(data_to_scale)

# agregar columna IDs
data_scaled['customerID'] = full_data['customerID']


# # # crear un nuevo df con columnas codificadas y escaladas 
merge_1 = data_other_columns.merge(data_encoded, on='customerID')

full_data_scaled_encoded = merge_1.merge(data_scaled, on='customerID')


# # guardar el df escalado y codificado en un parquet
parquet(full_data_scaled_encoded, 'files/datasets/final_provider/datasets_scaled_encoded/full_data_scaled.parquet')