import json
import os 

carpeta = 'data2/'

todos_los_datos = []

for archivo in os.listdir(carpeta):
    if archivo.endswith('.json'): 
        ruta_archivo = os.path.join(carpeta, archivo)
        print(ruta_archivo)
        with open(ruta_archivo, 'r') as f:
            datos = json.load(f)  
            todos_los_datos.append(datos) 

print(len(todos_los_datos))