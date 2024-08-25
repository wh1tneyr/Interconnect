# Ambiente virtual -----------------------------------------------

import pandas as pd
import os, sys
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
import platform 

# Modelos 
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
