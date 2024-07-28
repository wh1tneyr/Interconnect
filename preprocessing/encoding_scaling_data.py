import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import encoder, scaler, read_parquet


# leer el dataset completo
full_data = read_parquet('files/datasets/final_provider/full_data.parquet')

# filtrar las columnas categoricas para codificar
data_to_encode = full_data[['Type', 'PaperlessBilling', 'PaymentMethod', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'gender', 'Partner', 'Dependents', 'MultipleLines']]

# filtrar las columnas numericas para escalar
data_to_scale = full_data[['MonthlyCharges', 'TotalCharges']]

# filtrar las columnas que no necesitan codificacion ni escala
data_rest = full_data[['customerID', 'BeginDate', 'EndDate', 'SeniorCitizen', 'Churn']]