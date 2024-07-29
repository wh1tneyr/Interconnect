import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_csv, read_parquet, parquet, group_service, group_gender_churn, encoder, group_gender_churn_no_condition


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
in_ = in_.drop(['Churn'], axis=1).reset_index(drop=True)
in_.columns = ['Type', 'In']


out_ = churn_per_type[churn_per_type['Churn'] == 0].reset_index(drop=True)
out_ = out_.drop(['Churn'], axis=1).reset_index(drop=True)
out_.columns = ['Type', 'Out']


# crear un nuevo dataframe para el conteo de cancelacion por tipo de contrato 
type_churn_count = in_.merge(out_, on='Type')


""" Grafico: tasa de cancelación por tipo de contrato"""

#crear grafico de barras
# colors = ['blue', 'orange', ]
# ax_type_churn_count = type_churn_count.plot(kind='bar', color=colors, edgecolor='black')
# ax_type_churn_count.set_xticklabels(type_churn_count['Type'], rotation=45)

# # Agregar título y etiquetas
# plt.title('Tasa de cancelación por tipo de contrato')
# plt.xlabel('Tipo de Contrato')
# plt.ylabel('Tasa de cancelación')
# plt.legend(title='Contratos', labels=['In', 'Out'])

# plt.show()


""" EVALUAR LOS MONTOS MENSUALES SEGUN TIPO DE CONTRATO """

# agrupar por tipo de contrato  churn y ver el promedio de los cargos mensuales
monthly_type_churn = full_data.groupby(['Type', 'Churn'])['MonthlyCharges'].mean()


# reindexar para acceder a los montos 
monthly_type_churn = monthly_type_churn.reset_index(name='MonthlyChrges')


# filtrar por contratos cancelados y vigentes
in_ = monthly_type_churn[monthly_type_churn['Churn'] == 1].reset_index(drop=True)
in_ = in_.drop(['Churn'], axis=1).reset_index(drop=True)
in_.columns = ['Type', 'In']

out_ = monthly_type_churn[monthly_type_churn['Churn'] == 0].reset_index(drop=True)
out_ = out_.drop(['Churn'], axis=1).reset_index(drop=True)
out_.columns = ['Type', 'Out']

monthly_charges_mean = in_.merge(out_, on='Type')

""" Grafico: promedio de cargos mensuales segun tipo de contrato y cancelacion"""
# visualizar los montos mensuales
# crear grafico de barras 
# colors = ['blue', 'orange']

# ax_monthly_charges_mean = monthly_charges_mean.plot(kind='bar', color=colors, edgecolor='black')
# ax_monthly_charges_mean.set_xticklabels(monthly_charges_mean['Type'], rotation=45)

# # Agregar título y etiquetas
# plt.title('Promedio de cargos mensuales segun tipo de contrato y cancelacion')
# plt.xlabel('Tipo de Contrato')
# plt.ylabel('Promedio de cargos mensuales')
# plt.legend(labels=['In', 'Out'])
# plt.show()


## En promedio, los cargos mensuales son mas altos en los contratos que han cancelado el servicio



""" EVALUAR LOS MONTOS TOTALES SEGUN TIPO DE CONTRATO """

# agrupar por tipo de contrato  churn y ver el promedio de los cargos mensuales
total_type_churn = full_data.groupby(['Type', 'Churn'])['TotalCharges'].mean()


# reindexar para acceder a los montos 
total_type_churn = total_type_churn.reset_index(name='total_charges')


# filtrar por contratos cancelados y vigentes
in_2 = total_type_churn[total_type_churn['Churn'] == 1].reset_index(drop=True)
in_2 = in_2.drop(['Churn'], axis=1).reset_index(drop=True)
in_2.columns = ['Type', 'In']

out_2 = total_type_churn[total_type_churn['Churn'] == 0].reset_index(drop=True)
out_2 = out_2.drop(['Churn'], axis=1).reset_index(drop=True)
out_2.columns = ['Type', 'Out']

total_charges_mean = in_2.merge(out_2, on='Type')


""" Grafico: promedio de cargos totales segun tipo de contrato y cancelacion"""

# # crear grafico de barras 
# colors = ['blue', 'orange']

# ax_total_charges_mean = total_charges_mean.plot(kind='bar', color=colors, edgecolor='black')
# ax_total_charges_mean.set_xticklabels(total_charges_mean['Type'], rotation=45)

# # # Agregar título y etiquetas
# plt.title('Promedio de cargos totales segun tipo de contrato y cancelación')
# plt.xlabel('Tipo de Contrato')
# plt.ylabel('Promedio de cargos totales')
# plt.legend(labels=['In', 'Out'])
# plt.show()



""" EVALUAR EL SERVICIO DE INTERNET Y LA TASA DE CANCELACION """

# agrupar por internet 
internet_churn = full_data.groupby('InternetService')['Churn'].value_counts()	

# convertir el indice en columnas 	
internet_churn  = internet_churn.reset_index(name='Count')	

# eliminar la clase positiva y evaluar la tasa de cancelacion	
internet_churn_rate = internet_churn[internet_churn['Churn'] == 0].drop(['Churn'], axis=1).reset_index(drop=True)

# organizar los valores de 'count'
internet_churn_rate = internet_churn_rate.sort_values(by='Count', ascending=False)

""" Grafico: Tasa de cancelacion según tipo de internet """
#visualizar tasa de cancelacion en internet_service
# ax_internet_churn_rate = internet_churn_rate.plot(kind='bar', legend=False, edgecolor='black')
# ax_internet_churn_rate.set_xticklabels(internet_churn_rate['InternetService'], rotation=45)

# # Agregar título y etiquetas
# plt.title('Tasa de cancelacion según tipo de internet')
# plt.xlabel('Servicio de internet')
# plt.ylabel('Tasa de cancelacion')
# plt.show()

## La tasa de cancelacion es mas alta entre los clientes con internet de fibra optica y mas baja entre los que no tienen servicio de internet


""" EVALUAR TASA DE CANCELACION SEGUN OTROS SERVICIOS DERIVADOS DE INTERNET """

# crear un df para cada servicio de internet, filtrando unicamente la clase negativa,
# es decir, los contratos cancelados 

online_security_churn = group_service(full_data, 'OnlineSecurity')
online_backup_churn = group_service(full_data, 'OnlineBackup')
device_prot_churn = group_service(full_data, 'DeviceProtection')
tech_support_churn = group_service(full_data, 'TechSupport')
s_tv_churn = group_service(full_data, 'StreamingTV')
s_movies_churn = group_service(full_data, 'StreamingMovies')


# crear un solo df para la cancelacion de contratos con servicios derivados de internet 

data_services = [
    {'type': 'online_security', 'yes': online_security_churn['yes'].iloc[0], 'no': online_security_churn['no'].iloc[0]},
    {'type': 'online_backup', 'yes': online_backup_churn['yes'].iloc[0], 'no': online_backup_churn['no'].iloc[0]},
    {'type': 'device_protection', 'yes': device_prot_churn['yes'].iloc[0], 'no': device_prot_churn['no'].iloc[0]},
    {'type': 'tech_support', 'yes': tech_support_churn['yes'].iloc[0], 'no': tech_support_churn['no'].iloc[0]},
    {'type': 'streaming_tv', 'yes': s_tv_churn['yes'].iloc[0], 'no': s_tv_churn['no'].iloc[0]},
    {'type': 'streaming_movies', 'yes': s_movies_churn['yes'].iloc[0], 'no': s_movies_churn['no'].iloc[0]}
]


internet_services_churn = pd.DataFrame(data_services)  

internet_services_churn = internet_services_churn.sort_values(by='yes', ascending=False)

""" Grafico: Tasa de cancelacion en los servicios derivados de internet """

# visualizar tasa de cancelacion en servicios derivados de internet
# colors = ['blue', 'orange']

# ax_internet_services_churn = internet_services_churn.plot(kind='bar', color=colors, edgecolor='black')
# ax_internet_services_churn.set_xticklabels(internet_services_churn['type'], rotation=45)

# # # Agregar título y etiquetas
# plt.title('Tasa de cancelacion en servicios derivados de internet')
# plt.xlabel('tipo de servicio')
# plt.ylabel('Tasa de cancelacion segun si tenian el servicio o no')
# plt.legend(labels=['Si', 'No'])
# plt.show()


""" EVALUAR TASA DE CANCELACION SEGUN GENERO E INFORMACION PERSONAL """

# filtrar la info personal de los clientes y la cancelacion
data_personal_info = full_data[['customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'MultipleLines', 'Churn']]

# codificar variables categoricas en un nuevo df 
personal_encoded = data_personal_info[['customerID', 'gender','SeniorCitizen', 'Churn']]

encoded = encoder(data_personal_info[['Partner', 'Dependents', 'MultipleLines']])

# unir las nuevas variables codificadas al df personal_encoded
personal_encoded[['Partner', 'Dependents', 'MultipleLines']] = encoded 


# agrupar cancelaciones segun condicion y genero cuando se cumple la condicion
senior_churn = group_gender_churn(personal_encoded, 'gender', 'SeniorCitizen')
partner_churn = group_gender_churn(personal_encoded, 'gender', 'Partner')
dependents_churn = group_gender_churn(personal_encoded, 'gender', 'Dependents')
multiple_lines_churn = group_gender_churn(personal_encoded, 'gender', 'MultipleLines')


# agrupar cancelaciones segun condicion y genero cuando NO se cumple la condicion
young_churn = group_gender_churn_no_condition(personal_encoded, 'gender', 'SeniorCitizen')
single_churn = group_gender_churn_no_condition(personal_encoded, 'gender', 'Partner')
no_dependents_churn = group_gender_churn_no_condition(personal_encoded, 'gender', 'Dependents')


# crear un solo df para la cancelacion de contratos segun informacion personal

data_personal = [
    {'condition': 'senior_citizen', 'female': senior_churn['female'].iloc[0], 'male': senior_churn['male'].iloc[0]},
    {'condition': 'young_citizen', 'female': young_churn['female'].iloc[0], 'male': young_churn['male'].iloc[0]},
    {'condition': 'partner', 'female': partner_churn['female'].iloc[0], 'male': partner_churn['male'].iloc[0]},
    {'condition': 'single', 'female': single_churn['female'].iloc[0], 'male': single_churn['male'].iloc[0]},
    {'condition': 'dependents', 'female': dependents_churn['female'].iloc[0], 'male': dependents_churn['male'].iloc[0]},
    {'condition': 'no_dependents', 'female': no_dependents_churn['female'].iloc[0], 'male': no_dependents_churn['male'].iloc[0]}
]

personal_info_churn = pd.DataFrame(data_personal)



""" Grafico: Tasa de cancelacion segun genero e informacion personal """

# visualizar tasa de cancelacion segun informacion personal
# colors = ['blue', 'orange']

# ax_personal_info_churn = personal_info_churn.plot(kind='bar', color=colors, edgecolor='black')
# ax_personal_info_churn.set_xticklabels(personal_info_churn['condition'], rotation=45)

# # # # Agregar título y etiquetas
# plt.title('Tasa de cancelacion segun genero e informacion personal')
# plt.xlabel('Condicion')
# plt.ylabel('Tasa de cancelacion segun condicion de informacion personal')
# plt.legend(labels=['Mujer', 'Hombre'])
# plt.show()



""" TASA DE CANCELACION SEGUN SI EL CLIENTE TIENE MULTIPLES LINEAS TELEFONICAS """

# agrupar segun genero en clientes con multiples lineas
multiple_lines_churn = group_gender_churn(personal_encoded, 'gender', 'MultipleLines')

# agrupar segun genero en clientes SIN multiples lineas
no_multiple_lines_churn = group_gender_churn_no_condition(personal_encoded, 'gender', 'MultipleLines')


# crear un solo df para clientes con y sin multiples lineas
data_multiple_lines = [
    {'multiple_lines':'yes', 'female':multiple_lines_churn['female'].loc[0], 'male':multiple_lines_churn['male'].loc[0]},
    {'multiple_lines':'no', 'female':no_multiple_lines_churn['female'].loc[0], 'male':no_multiple_lines_churn['male'].loc[0]}
]

MultipleLines_churn = pd.DataFrame(data_multiple_lines)



""" Grafico: cancelacion para clientes con multiples lineas segun genero """

# # visualizar tasa de cancelacion segun multiples lineas
# colors = ['blue', 'orange']

# ax_multiple_lines_churn = MultipleLines_churn.plot(kind='bar', color=colors, edgecolor='black')
# ax_multiple_lines_churn .set_xticklabels(MultipleLines_churn['multiple_lines'], rotation=45)

# # # Agregar título y etiquetas
# plt.title('Tasa de cancelacion para clientes con multiples lineas segun genero')
# plt.xlabel('Multiples lineas telefonicas')
# plt.ylabel('Tasa de cancelacion segun genero')
# plt.legend(labels=['Mujer', 'Hombre'])
# plt.show()


""" TASA DE CANCELACION SEGUN GENERO """

# agrupar por genero y contar cancelaciones
gender_churn = full_data.groupby('gender')['Churn'].value_counts().reset_index(name='count')

gender_churn_rate = gender_churn[gender_churn['Churn']==0].drop(['Churn'], axis=1).reset_index(drop=True)


""" Grafico: cancelaciones segun genero """
 
# # # visualizar tasa de cancelacion segun genero
# ax_gender_churn = gender_churn_rate.plot(kind='bar', edgecolor='black', legend=False)
# ax_gender_churn.set_xticklabels(gender_churn_rate['gender'], rotation=45)

# # # Agregar título y etiquetas
# plt.title('Tasa de cancelación segun género')
# plt.xlabel('Género')
# plt.ylabel('Tasa de cancelación')
# plt.show()