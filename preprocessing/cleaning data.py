import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_csv



""" LEER LOS DATOS """

user_contract = read_csv('/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/contract.csv')
user_personal_info = read_csv('/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/personal.csv')
phone_ser = read_csv('/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/phone.csv')
internet_ser = read_csv('/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/internet.csv')



""" LIMPIAR DATOS (contract) """

#visualizar
user_contract.head(20)
user_contract.info()

#ver valores ausentes y duplicados
user_contract.isna().sum()
user_contract.duplicated().sum()
user_contract['customerID'].duplicated().sum()

""" no hay ausentes ni duplicados  """

# TODO : convertir 'BeginDate' a formato fecha
# TODO: convetir 'TotalCharges' a formato float

user_contract['BeginDate'] = pd.to_datetime(user_contract['BeginDate'], format='%Y-%m-%d')
user_contract['TotalCharges'] = pd.to_numeric(user_contract['TotalCharges'], errors='coerce')
 
#comprobar nuevamente valores ausentes 
user_contract.isna().sum()

#eliminar valores ausentes 
user_contract = user_contract.dropna().reset_index(drop=True)

""" no hay duplicados ni ausentes. Tipos de datos correctos """



""" LIMPIAR DATOS (user_personal_info) """

#visualizar
user_personal_info.info()
user_personal_info.head()

#datos nulos o duplicados
user_personal_info.isna().sum()
user_personal_info.duplicated().sum()

""" no hay duplicados ni ausentes. Tipos de datos correctos """



""" LIMPIAR DATOS (phone_ser) """

#visualizar
phone_ser.info()
phone_ser.head()

#ver duplicados y ausentes 
phone_ser.isna().sum()
phone_ser.duplicated().sum()

""" no hay duplicados ni ausentes. Tipos de datos correctos """



""" LIMPIAR DATOS (internet_ser) """

#visualizar 
internet_ser.info()
internet_ser.head()

#ver duplicados y ausentes
internet_ser.isna().sum()
internet_ser.duplicated().sum()

""" no hay duplicados ni ausentes. Tipos de datos correctos """
user_contract_cleaned = user_contract

#guardar contract como un nuevo dataframe limpio
user_contract.to_csv("/Users/whitneyrios/PYTHON/My projects py/Proyecto Final 17 Telecom/Proyecto_Final_Telecom/files/datasets/final_provider/contract_cleaned.csv", index=False)