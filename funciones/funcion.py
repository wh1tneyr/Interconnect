import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.metrics import roc_auc_score, accuracy_score



""" Funcion para leer archivos csv """
def read_csv(path):
    data = pd.read_csv(path)
    return data



""" Funcion para leer archivos parquet """
def read_parquet(path):
    data = pd.read_parquet(path)
    return data



""" Funcion para cambiar a formato fecha """
def to_date_time(data):
    data = pd.to_datetime(data, format='%Y-%m-%d')
    return data



""" Funcion para codificar caracteristicas categoricas """
def encoder(data):
    encoder = OrdinalEncoder()
    data_encoded = pd.DataFrame(encoder.fit_transform(data), columns=data.columns)
    data_encoded = data_encoded.astype('int')
    return data_encoded
    
    
    
""" Funcion para escalar caracteristicas numericas en conjunto de entrenamiento """
def scaler_train(train_data):
    scaler = StandardScaler()
    data_scaled = pd.DataFrame(scaler.fit_transform(train_data), columns=train_data.columns)
    return data_scaled


""" Funcion para guardar archivos parquet """
def parquet(data, path):
    engine='pyarrow'
    index=False
    return data.to_parquet(path, engine=engine, index=index)
    
 
 
""" Funcion para agrupar por servicio derivado de internet y contar las cancelaciones   """   

def group_service(full_data, column):
    # Agrupar y contar los valores de 'Churn'
    values = full_data.groupby(column)['Churn'].value_counts().reset_index(name='count')

    # Conservar solo la clase negativa
    data = values[values['Churn'] == 0].drop(['Churn'], axis=1).reset_index(drop=True)

    if len(data) < 2:
        raise ValueError("No hay suficientes datos para las clases 'yes' y 'no'.")

    # Asignar 'yes' y 'no' basados en la condición
    yes = data.iloc[0]
    no = data.iloc[1]

    # Construir el DataFrame resultante
    result_df = pd.DataFrame({'type': [column], 'yes': [yes['count']], 'no': [no['count']]})
    return result_df



""" Funcion para agrupar por genero e informacion personal y contar las cancelaciones para personas que cumplen la condicion descrita """  

def group_gender_churn(full_data, gender_column, column):
    # Agrupar y contar los valores de 'Churn'
    values = full_data.groupby([gender_column, column])['Churn'].value_counts().reset_index(name='count')

    # Conservar solo la clase negativa presentes  
    data = values[(values[column] == 1) & (values['Churn'] == 0)].drop([column,'Churn'], axis=1).reset_index(drop=True)

    if len(data) < 2:
        raise ValueError("No hay suficientes datos para las clases 'female' y 'male'.")

    # Asignar 'female' y 'male' basados en la condición
    female = data.iloc[0]
    male = data.iloc[1]

    # Construir el DataFrame resultante
    result_df = pd.DataFrame({'condition': [column], 'female': [female['count']], 'male': [male['count']]})
    return result_df


""" Funcion para agrupar por genero e informacion personal y contar las cancelaciones para personas que NO cumplen la condicion descrita """ 

def group_gender_churn_no_condition(full_data, gender_column, column):
    # Agrupar y contar los valores de 'Churn'
    values = full_data.groupby([gender_column, column])['Churn'].value_counts().reset_index(name='count')

    # Conservar solo la clase negativa presentes  
    data = values[(values[column] == 0) & (values['Churn'] == 0)].drop([column,'Churn'], axis=1).reset_index(drop=True)

    if len(data) < 2:
        raise ValueError("No hay suficientes datos para las clases 'female' y 'male'.")

    # Asignar 'female' y 'male' basados en la condición
    female = data.iloc[0]
    male = data.iloc[1]

    # Construir el DataFrame resultante
    result_df = pd.DataFrame({'condition': [column], 'female': [female['count']], 'male': [male['count']]})
    return result_df


""" Funcion para evaluar los modelos con roc_auc y exactitud  """

def model_eval(model, train_target, train_features):
    
    # Hacer predicciones con el modelo
    predictions = model.predict(train_features)
    
    # Predecir la probailidad de clase
    class_proba = model.predict_proba(train_features)
    
    # Extraer solo las probabilidades de la clase positiva (clase 1)
    class_proba_positive = class_proba[:, 1]
    
    # Evaluar el modelo con roc_auc
    model_auc_roc_score = roc_auc_score(train_target, class_proba_positive)
    
    # Evaluar el modelo con accuracy
    model_accuracy = accuracy_score(train_target, predictions)
    
    return model_auc_roc_score, model_accuracy
