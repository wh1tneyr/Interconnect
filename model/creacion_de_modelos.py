# Librerias 
import pandas as pd
import os, sys
sys.path.append(os.getcwd())
import joblib

# Funciones 
from funciones.funcion import read_parquet, parquet, model_eval


# Modelos 
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier



""" LEER CONJUNTOS DE ENTRENAMIENTO  """

# leer conjunto de entrenamiento
data_train = read_parquet('files/datasets/final_provider/datasets_scaled_encoded/train_scaled_encoded.parquet')

data_train.set_index('customerID', inplace=True)

# definir las caracteristicas y el objetivo
train_features = data_train.drop(['Churn'], axis=1)
train_target = data_train['Churn']

# leer conjunto de prueba
data_test = read_parquet('files/datasets/final_provider/datasets_scaled_encoded/test_scaled_encoded.parquet')

data_test.set_index('customerID', inplace=True)

# definir caracteristicas y objetivo
test_features = data_test.drop(['Churn'], axis=1)
test_target = data_test['Churn']

# leer conjunto de validacion
data_valid = read_parquet('files/datasets/final_provider/datasets_scaled_encoded/valid_scaled_encoded.parquet')

data_valid.set_index('customerID', inplace=True)


# definir caracteristicas y objetivo
valid_features = data_valid.drop(['Churn'], axis=1)
valid_target = data_valid['Churn']



""" BOSQUE ALEATORIO  """

# Crear un modelo de bosque aleatorio
rf_model = RandomForestClassifier(random_state=345,
                                      class_weight='balanced',
                                      criterion='entropy',
                                      max_depth=10,
                                      max_features='sqrt',
                                      min_samples_split=5,
                                      n_estimators=200
                                      )


""" ENTRENAMIENTO Y EVALUACION BOSQUE ALEATORIO """

# Entrenar el modelo de bosque aleatorio 
rf_model.fit(train_features, train_target)

# # Evaluar el modelo en conjunto de entrenamiento
rf_roc_auc_train, rf_accuracy_train = model_eval(rf_model, train_target, train_features)

# # Evaluar el modelo en conjunto de prueba 
rf_roc_auc_test, rf_accuracy_test = model_eval(rf_model, test_target, test_features)


# Mostrar outputs de evaluacion
# # Roc_auc
rf_roc_auc_train
rf_roc_auc_test

# # Exactitud
rf_accuracy_train
rf_accuracy_test


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


""" ENTRENAMIENTO Y EVALUACION ARBOL DE DECISION """

# Entrenar el modelo  
dt_model.fit(train_features, train_target)

# Evaluar el modelo en conjunto de entrenamiento
dt_roc_auc_train, dt_accuracy_train = model_eval(dt_model, train_target, train_features)

# Evaluar el modelo en conjunto de prueba 
dt_roc_auc_test, dt_accuracy_test = model_eval(dt_model, test_target, test_features)


# Mostrar outputs de evaluacion
# # Roc_auc
dt_roc_auc_train
dt_roc_auc_test

# # Exactitud
dt_accuracy_train
dt_accuracy_test



""" MODELO CATBOOST """

# Construir un modelo catboost
cb_model = CatBoostClassifier(
    random_seed=42,
    iterations=150,          # Aumentar las iteraciones
    learning_rate=0.05,      # Reducir la tasa de aprendizaje
    loss_function='CrossEntropy',
    max_depth=6,             # Reducir la profundidad máxima
    l2_leaf_reg=5,           # Agregar regularización L2
    early_stopping_rounds=20 # Habilitar early stopping
)



""" ENTRENAMIENTO Y EVALUACION DEL MODELO CATBOOST """

# Entrenar el modelo 
cb_model.fit(train_features, train_target,  cat_features=None)

# Evaluar el modelo en conjunto de entrenamiento
cb_roc_auc_train, cb_accuracy_train = model_eval(cb_model, train_target, train_features)

# Evaluar el modelo en conjunto de prueba 
cb_roc_auc_test, cb_accuracy_test = model_eval(cb_model, test_target, test_features)

# Mostrar outputs de evaluacion
# # Roc_auc
cb_roc_auc_train
cb_roc_auc_test

# # Exactitud
cb_accuracy_train
cb_accuracy_test

""" MODELO LIGHTGBM """

# Construir el modelo lightgbm
lgbm_model = LGBMClassifier(
    random_state=42,
    n_estimators=200,          # Aumentar el número de estimadores
    learning_rate=0.01,        # Reducir la tasa de aprendizaje
    objective='binary',
    class_weight='balanced',
    max_depth=6,               # Reducir la profundidad máxima
    reg_alpha=0.1,             # Añadir regularización L1
    reg_lambda=0.1,            # Añadir regularización L2
    subsample=0.8,             # Muestreo de filas
    colsample_bytree=0.8,      # Muestreo de características
    #early_stopping_rounds=10   # Habilitar early stopping
)



""" ENTRENAR Y EVALUAR EL MODELO LIGHTGBM """

# Entrenar el modelo
lgbm_model.fit(train_features, train_target)

# Evaluar el modelo en conjunto de entrenamiento
lgbm_roc_auc_train, lgbm_accuracy_train = model_eval(lgbm_model, train_target, train_features)

# Evaluar el modelo en conjunto de prueba 
lgbm_roc_auc_test, lgbm_accuracy_test = model_eval(lgbm_model, test_target, test_features)

# Mostrar outputs de evaluacion
# # Roc_auc
lgbm_roc_auc_train
lgbm_roc_auc_test

# # Exactitud
lgbm_accuracy_train
lgbm_accuracy_test

# Save model ---------------------------------------- 

joblib.dump(
        rf_model,
        f"files/modeling_output/model_fit/random_forest.joblib"
        )

joblib.dump(
        dt_model,
        f"files/modeling_output/model_fit/decision_tree.joblib"
        )

joblib.dump(
        cb_model,
        f"files/modeling_output/model_fit/catboost.joblib"
        )

joblib.dump(
        lgbm_model,
        f"files/modeling_output/model_fit/light_gbm.joblib"
        )