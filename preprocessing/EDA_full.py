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


# crear un nuevo dataframe para el conteo de cancelacion por tipo de contrato 
type_churn_count = in_.merge(out_, on='Type')


# visualizar el conteo de churn por tipo de contrato
#crear grafico de barras
colors = ['blue', 'orange', ]
ax_type_churn_count = type_churn_count.plot(kind='bar', color=colors, edgecolor='black')
ax_type_churn_count.set_xticklabels(type_churn_count['Type'], rotation=45)

# Agregar título y etiquetas
plt.title('Conteo de Churn por Tipo de Contrato')
plt.xlabel('Tipo de Contrato')
plt.ylabel('Conteo de Churn')
plt.legend(title='Contratos', labels=['In', 'Out'])

plt.show()


""" EVALUAR LOS MONTOS MENSUALES SEGUN TIPO DE CONTRATO """

# agrupar por tipo de contrato  churn y ver el promedio de los cargos mensuales
monthly_type_churn = full_data.groupby(['Type', 'Churn'])['MonthlyCharges'].mean()


# reindexar para acceder a los montos 
monthly_type_churn = monthly_type_churn.reset_index(name='MonthlyChrges')


# filtrar por contratos cancelados y vigentes
in_ = monthly_type_churn[monthly_type_churn['Churn'] == 1].reset_index(drop=True)
in_ = in_.drop(['Churn'], axis=1)
in_.columns = ['Type', 'In']

out_ = monthly_type_churn[monthly_type_churn['Churn'] == 0].reset_index(drop=True)
out_ = out_.drop(['Churn'], axis=1)
out_.columns = ['Type', 'Out']

monthly_charges_mean = in_.merge(out_, on='Type')


# visualizar los montos mensuales
# crear grafico de barras 
colors = ['blue', 'orange']

ax_monthly_charges_mean = monthly_charges_mean.plot(kind='bar', color=colors)
ax_monthly_charges_mean.set_xticklabels(monthly_charges_mean['Type'], rotation=45)

# Agregar título y etiquetas
plt.title('Promedio de cargos mensuales segun tipo de contrato y cancelacion')
plt.xlabel('Tipo de Contrato')
plt.ylabel('Promedio de cargos mensuales')
plt.legend(labels=['In', 'Out'])
plt.show()

# En promedio, los cargos mensuales son mas altos en los contratos que han cancelado el servicio


""" EVALUAR EL SERVICIO DE INTERNET Y LA TASA DE CANCELACION """

# agrupar por internet 
internet_churn = full_data.groupby('InternetService')['Churn'].value_counts()

# convertir el indice en columnas 
internet_churn  = internet_churn.reset_index(name='Count')

# eliminar la clase positiva y evaluar la tasa de cancelacion
internet_churn_rate = internet_churn[internet_churn['Churn'] == 0].drop(['Churn'], axis=1)


#visualizar tasa de cancelacion en internet_service
#colors = ['blue', 'orange', 'green']
ax_internet_churn_rate = internet_churn_rate.plot(kind='bar', legend=False)
ax_internet_churn_rate.set_xticklabels(internet_churn_rate['InternetService'], rotation=45)

# Agregar título y etiquetas
plt.title('Tasa de cancelacion según tipo de internet')
plt.xlabel('Servicio de internet')
plt.ylabel('Tasa de cancelacion')
plt.show()

# La tasa de cancelacion es mas alta entre los clientes con internet de fibra optica y mas baja entre los que no tienen servicio de internet