# import os, sys
# sys.path.append(os.getcwd())
import pandas as pd

def read_csv(path):
    data = pd.read_csv(path)
    return data