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

