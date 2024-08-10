import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import read_parquet, parquet

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, accuracy_score


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

# # crear un modelo de bosque aleatorio
rf_clf_model = RandomForestClassifier(random_state=345,
                                      class_weight='balanced',
                                      criterion='entropy',
                                      max_depth=15,
                                      max_features=6,
                                      min_samples_split=2,
                                      n_estimators=100
                                      )

# # establecer hiperparametros para el buscador

# params = {
#     'n_estimators' : [20, 60, 100],
#     'max_depth' : [10, 15, 23],
#     'min_samples_split' : [2, 3],
#     'max_features' : [2, 4, 6],
#     'class_weight' : ['balanced', 'balanced_subsample'],
#     'criterion' : ['gini', 'entropy', 'log_loss']
# } 
 
# # # buscar los mejores hipeparametros 

# grid = GridSearchCV(estimator=rf_clf_model, param_grid=params, cv=5)

# grid.fit(train_features, train_target)

# # # mostrar los mejores hiperparámetros del modelo

# grid.best_params_


# # mejores hiperparametros :
# # # {'class_weight': 'balanced', 'criterion': 'entropy', 'max_depth': 15, 'max_features': 6, 'min_samples_split': 2, 'n_estimators': 100}

""" Entrenar el bosque aleatorio """

rf_clf_model.fit(train_features, train_target)

# # predecir la probabilidad de clases 
rf_clf_proba = rf_clf_model.predict_proba(train_features)

# Extraer solo las probabilidades de la clase positiva (clase 1)
rf_clf_proba_positive = rf_clf_proba[:, 1]

# # evaluar el modelo con auc_roc
roc_auc_score(train_target, rf_clf_proba_positive)

