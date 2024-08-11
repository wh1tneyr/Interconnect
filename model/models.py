# Librerias 
import pandas as pd
import os, sys
sys.path.append(os.getcwd())

# Funciones 
from funciones.funcion import read_parquet, parquet, model_eval
from sklearn.metrics import roc_auc_score, accuracy_score

# Modelos 
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier



""" LEER CONJUNTOS DE ENTRENAMIENTO  """

# leer conjunto de entrenamiento
data_train = read_parquet('files/datasets/final_provider/data_train.parquet')

data_train.set_index('customerID', inplace=True)

# definir las caracteristicas y el objetivo
train_features = data_train.drop(['Churn', 'BeginDate'], axis=1)
train_target = data_train['Churn']

# leer conjunto de prueba
data_test = read_parquet('files/datasets/final_provider/data_test.parquet')

data_test.set_index('customerID', inplace=True)

# definir caracteristicas y objetivo
test_features = data_test.drop(['Churn', 'BeginDate'], axis=1)
test_target = data_test['Churn']

# leer conjunto de validacion
data_valid = read_parquet('files/datasets/final_provider/data_valid.parquet')

data_valid.set_index('customerID', inplace=True)


# definir caracteristicas y objetivo
valid_features = data_valid.drop(['Churn', 'BeginDate'], axis=1)
valid_target = data_valid['Churn']



""" BOSQUE ALEATORIO  """

# Crear un modelo de bosque aleatorio
rf_model = RandomForestClassifier(random_state=345,
                                      class_weight='balanced',
                                      criterion='entropy',
                                      max_depth=15,
                                      max_features=6,
                                      min_samples_split=2,
                                      n_estimators=100
                                      )

# Establecer hiperparametros para el buscador

# params = {
#     'n_estimators' : [20, 60, 100],
#     'max_depth' : [10, 15, 23],
#     'min_samples_split' : [2, 3],
#     'max_features' : [2, 4, 6],
#     'class_weight' : ['balanced', 'balanced_subsample'],
#     'criterion' : ['gini', 'entropy', 'log_loss']
# } 
 
# Buscar los mejores hipeparametros 

# grid = GridSearchCV(estimator=rf_model, param_grid=params, cv=5)

# grid.fit(train_features, train_target)

# Mostrar los mejores hiperparámetros del modelo

# grid.best_params_


# Mejores hiperparametros :
# # # {'class_weight': 'balanced', 'criterion': 'entropy', 'max_depth': 15, 'max_features': 6, 'min_samples_split': 2, 'n_estimators': 100}

""" ENTRENAMIENTO Y EVALUACION BOSQUE ALEATORIO """

# Entrenar el modelo de bosque aleatorio 
rf_model.fit(train_features, train_target)

# # Evaluar el modelo en conjunto de entrenamiento
rf_roc_auc_train, rf_accuracy_train = model_eval(rf_model, train_target, train_features)

# # Evaluar el modelo en conjunto de prueba 
rf_roc_auc_test, rf_accuracy_test = model_eval(rf_model, test_target, test_features)

print('\n Auc_roc conjunto de entrenamiento (RF):', rf_roc_auc_train, '\n')
print('\n Exactitud conjunto de entrenamiento (RF):', rf_accuracy_train, '\n')

print('\n Auc_roc conjunto de prueba (RF):', rf_roc_auc_test, '\n')
print('\n Exactitud conjunto de prueba (RF):', rf_accuracy_test, '\n')


""" ARBOL DE DECISION """

# Construir un modelo de arbol de decision
dt_model = DecisionTreeClassifier(
    random_state=42,
    class_weight='balanced',
    criterion='gini',
    max_depth=5,
    max_features=6,
    min_samples_split=2,
    splitter='random'
    )

# Establecer hiperparametros para el buscador

# params = {
#     'max_depth' : [5, 10, 20],
#     'min_samples_split' : [2, 4, 6],
#     'max_features' : [2, 4, 6],
#     'class_weight' : ['balanced', 'None'],
#     'criterion' : ['gini', 'entropy', 'log_loss'],
#     'splitter' : ['best', 'random']
# } 
 
# Buscar los mejores hipeparametros 

# grid = GridSearchCV(estimator=dt_model, param_grid=params, cv=5)

# grid.fit(train_features, train_target)

# # Mostrar los mejores hiperparámetros del modelo

# grid.best_params_

# Mejores hiperparametros 
# # {'class_weight': 'balanced', 'criterion': 'gini', 'max_depth': 5, 'max_features': 6, 'min_samples_split': 2, 'splitter': 'random'}


""" ENTRENAMIENTO Y EVALUACION ARBOL DE DECISION """

# Entrenar el modelo  
dt_model.fit(train_features, train_target)

# Evaluar el modelo en conjunto de entrenamiento
dt_roc_auc_train, dt_accuracy_train = model_eval(dt_model, train_target, train_features)

# Evaluar el modelo en conjunto de prueba 
dt_roc_auc_test, dt_accuracy_test = model_eval(dt_model, test_target, test_features)

print('\n Auc_roc conjunto de entrenamiento (DT):', dt_roc_auc_train, '\n')
print('\n Exactitud conjunto de entrenamiento (DT):', dt_accuracy_train, '\n')

print('\n Auc_roc conjunto de prueba (DT):', dt_roc_auc_test, '\n')
print('\n Exactitud conjunto de prueba (DT):', dt_accuracy_test, '\n')


""" MODELO CATBOOST """

# Construir un modelo catboost
cb_model = CatBoostClassifier(
    random_seed=42,
    iterations=50,
    learning_rate=0.1,
    loss_function='CrossEntropy',
    max_depth=10
    )


# Establecer hiperparametros para el buscador
# params = {
#     'iterations' : [50, 100, 150 ],
#     'learning_rate' : [0.01, 0.1, 0.5, 0.8],
#     'loss_function' : ['CrossEntropy', 'AUC', 'BalancedAccuracy'],
#     'max_depth' : [10, 20, 40],
#     }

# # Buscar los mejores hipeparametros 

# grid = GridSearchCV(estimator=cb_model, param_grid=params, cv=5)

# grid.fit(train_features, train_target)

# # Mostrar los mejores hiperparámetros del modelo

# grid.best_params_

# # Mejores hiperparametros 

# # # {'iterations': 50, 'learning_rate': 0.1, 'loss_function': 'CrossEntropy', 'max_depth': 10}