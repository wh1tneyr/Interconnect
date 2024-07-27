import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_csv, read_parquet, parquet
import matplotlib.pyplot as plt

""" LEER DATOS """
contract_prep = read_parquet('files/datasets/final_provider/contract_cleaned.parquet') 
internet_prep = read_csv('files/datasets/final_provider/internet.csv')
personal_prep = read_csv('files/datasets/final_provider/personal.csv')
phone_prep = read_csv('files/datasets/final_provider/phone.csv')


# concatenar cotract_prep e internet_prep (sin escalar ni codificar)
merge_1 = contract_prep.merge(internet_prep, on='customerID', how='left')

# comprobar valores ausentes 
merge_1.isna().sum()


# suponiendo que los ausentes corresponden a clientes que no pagan por servicios de internet,
# rellenar ausentes con 'No'
merge_1 = merge_1.fillna('No')
merge_1.isna().sum()


# concatenar merge_1 con personal_prep
merge_2 = merge_1.merge(personal_prep, on='customerID', how='left')
merge_2.isna().sum()


# concatenar merge_2 con phone_prep
full_data = merge_2.merge(phone_prep,  on='customerID', how='left')

full_data.isna().sum()

# suponiendo que los ausentes corresponden a clientes que no tienen multiples lineas,
# rellenar ausentes con 'No'
full_data = full_data.fillna('No')

full_data.isna().sum()


#crear una variable Churn y pasar los 'No' a 1 y las fechas a 0
# 1 = sigue vigente,
# 0 = contrato terminado
full_data['Churn'] = full_data['EndDate']
full_data['Churn'] = full_data['Churn'].replace('No', '1').apply(lambda x: 1 if x == '1' else 0)


# guardar full_data como parquet
parquet(full_data, 'files/datasets/final_provider/full_data.parquet')


""" DESEQUILIBRIO DE CLASES """

full_data['Churn'].value_counts()
# hay un fuerte desequilibrio entre la clases negativa y positiva


""" FECHAS DE REGISTRO"""

'Primera fecha registrada:', full_data['BeginDate'].sort_values().min()
'Ultima fecha registrada:', full_data['BeginDate'].sort_values().max()

# el dataset tiene datos registrados desde el primero de octubre del 2013 hasta el 01 de enero del 2020


""" EVALUAR TASA DE CANCELACION SEGUN EL TIPO DE CONTRATO """

# agrupar por tipo de contrato y hacer conteo de churn
churn_per_type = full_data.groupby('Type')['Churn'].value_counts()

# convertir el índice en columnas para acceder a los valores de 'churn'
churn_per_type = churn_per_type.reset_index(name='Count')

# filtrar los contratos cancelados y los vigentes 
in_ = churn_per_type[churn_per_type['Churn'] == 1].reset_index(drop=True)
in_ = in_.drop(['Churn'], axis=1)
in_.columns = ['Type', 'In']


out_ = churn_per_type[churn_per_type['Churn'] == 0].reset_index(drop=True)
out_ = out_.drop(['Churn'], axis=1)
out_.columns = ['Type', 'Out']

