import pandas as pd
import os, sys
sys.path.append(os.getcwd())

from funciones.funcion import encoder, scaler, read_parquet

full_data = read_parquet('files/datasets/final_provider/full_data.parquet')
