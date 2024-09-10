# Librerias ---------------------------------------- 
import os, sys
import platform 

# Systema operativo ---------------------------------------- 

sistema_operativo = platform.system()

# Definir extension de ejecutables ---------------------------------------- 

if sistema_operativo == 'Windows':
        extension_binarios = ".exe"
else:
        extension_binarios = ""
        
        
        
# Funciones para preproceso y EDA ---------------------------------------- 
os.system(f"python3{extension_binarios} funciones/funcion.py") # TODO No es necesario elecutar el script de funciones. Con cada ejecusión de python con `system`, se crea una nueva sesión de Python que es destruida cuando termina de ejecutarse. Basta con importarlo

# Preproceso de datos ----------------------------------------------------
os.system(f"python3{extension_binarios} preprocessing/cleaning_data.py")

# Exploracion de datos -------------------------------------------
os.system(f"python3{extension_binarios} preprocessing/EDA_full.py")

# Segmentacion de datos para el modelo --------------------------------------
os.system(f"python3{extension_binarios} preprocessing/train_test_split_data.py")

# Escalamiento y codificacion de datos para el modelos --------------------------------
os.system(f"python3{extension_binarios} preprocessing/train_test_scaling_encoding.py")

# Modelo --------------------------------------------------------------------------
os.system(f"python3{extension_binarios} model/creacion_de_modelos.py")