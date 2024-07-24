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


#Evaluar la variable churn respecto al tipo de pago
churn_contract_type = contract_prep.groupby('Type')['churn'].value_counts()

#crear grafico de barras
colors = ['blue', 'orange']
churn_contract_type.plot(kind='bar', color=colors, edgecolor='black')

# Agregar título y etiquetas
plt.title('Conteo de Churn por Tipo de Contrato')
plt.xlabel('Tipo de Contrato')
plt.ylabel('Conteo de Churn')
plt.legend(title='Churn', labels=['No', 'Yes'])

# Inclinar las etiquetas del eje y
churn_contract_type.set_xlabel(rotation=45)

plt.show()
#de los planes cancelados, la mayoria pertence al tipo de pago mes a mes. La menor fuga se presenta en los planes de dos años. 

#Calcular el porcentaje de cancelacion segun el tipo de contrato
contract_type_count = contract_prep.groupby('Type')['customerID'].count()