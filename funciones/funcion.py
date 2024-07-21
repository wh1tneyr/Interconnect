import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

""" Funcion para leer archivos csv """
def read_csv(path):
    data = pd.read_csv(path)
    return data



""" Funcion para cambiar a formato fecha """
def to_date_time(data):
    data = pd.to_datetime(data, format='%Y-%m-%d')
    return data



""" Funcion para codificar caracteristicas categoricas """
def encoder(data):
    encoder = OrdinalEncoder()
    data_encoded = pd.DataFrame(encoder.fit_transform(data), columns=data.columns)
    return data_encoded
    
    
""" Funcion para escalar caracteristicas numericas """
def scaler(data):
    scaler = StandardScaler()
    data_scaled = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
    return data_scaled