import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_csv, read_parquet
import matplotlib.pyplot as plt

""" LEER DATOS """
contract_prep = read_parquet('files/datasets/final_provider/contract_cleaned.parquet') 
internet_prep = read_csv('files/datasets/final_provider/internet.csv')
personal_prep = read_csv('files/datasets/final_provider/personal.csv')
phone_prep = read_csv('files/datasets/final_provider/phone.csv')


""" Examinar la variable churn"""
#crear una variable churn y pasar los 'No' a 1 y las fechas a 0
# 1 = sigue vigente,
# 0 = contrato terminado

contract_prep['churn'] = contract_prep['EndDate']
contract_prep['churn'] = contract_prep['churn'].replace('No', '1').apply(lambda x: 1 if x == '1' else 0)


""" DESEQUILIBRIO DE CLASES """

contract_prep['churn'].value_counts()
# hay desequilibrio de clases 


""" FECHAS DE REGISTRO"""

'Primera fecha registrada:', contract_prep['BeginDate'].sort_values().min()
'Ultima fecha registrada:', contract_prep['BeginDate'].sort_values().max()
#el dataset tiene datos registrados desde el primero de octubre del 2013 hasta el 01 de enero del 2020


""" EVALUAR TASA DE CANCELACION SEGUN EL TIPO DE CONTRATO """

churn_per_type = contract_prep.groupby('Type')['churn'].value_counts()

# Convertir el índice en columnas para acceder a los valores de 'churn'
churn_values = churn_per_type.reset_index(name='count')

# filtrar los contratos cancelados y los vigentes 
in_ = churn_values[churn_values['churn'] == 1].reset_index(drop=True)
in_ = in_.drop(['churn'], axis=1)
in_.columns = ['Type', 'In']


out_ = churn_values[churn_values['churn'] == 0].reset_index(drop=True)
out_ = out_.drop(['churn'], axis=1)
out_.columns = ['Type', 'Out']

# crear un nuevo dataframe con el conteo de contratos por tipo 
contract_count = contract_prep.groupby('Type')['customerID'].count()

# Convertir el índice en columnas para acceder a los valores de 'type'
contract_count = contract_count.reset_index(name='Count')

# incluir la info de los contratos vigentes y los canccelado en el nuevo df
merge_1 = contract_count.merge(in_, on='Type', how='inner')
contract_churn = merge_1.merge(out_, on='Type')



for index, row in contract_churn.iterrows():
    churn_rate = (row['Out'] / row['Count']) * 100
    contract_churn.at[index, 'churn_rate'] = churn_rate


#crear grafico de barras
colors = ['blue', 'orange', ]
ax_churn = contract_churn[['In', 'Out']].plot(kind='bar', color=colors, edgecolor='black')
ax_churn.set_xticklabels(contract_churn['Type'], rotation=45)

# Agregar título y etiquetas
plt.title('Conteo de Churn por Tipo de Contrato')
plt.xlabel('Tipo de Contrato')
plt.ylabel('Conteo de Churn')
plt.legend(title='Contratos', labels=['In', 'Out'])

plt.show()


# ver la cantidad de meses en month-to-month hasta abandonar plan 

months_to_churn = contract_prep[(contract_prep['Type'] == 'Month-to-month') & (contract_prep['churn'] == 0)]
