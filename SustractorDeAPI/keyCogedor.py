import json
import os

# Función para extraer las claves del primer coche
def extraer_claves_primer_coche(carpeta_entrada):
    archivos = os.listdir(carpeta_entrada)  # Listar todos los archivos en la carpeta de entrada
    archivos_json = [archivo for archivo in archivos if archivo.endswith('.json')]  # Filtrar solo archivos JSON
    
    if not archivos_json:
        print("No se encontraron archivos JSON en la carpeta.")
        return
    
    # Procesar solo el primer archivo JSON
    primer_archivo = archivos_json[0]
    ruta_archivo = os.path.join(carpeta_entrada, primer_archivo)  # Obtener ruta completa del archivo
    print(f"Procesando archivo: {ruta_archivo}")
    
    # Leer el archivo JSON
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        datos = json.load(file)
    
    # Si el archivo contiene varios coches, procesar solo el primero
    if isinstance(datos, list) and len(datos) > 0:  # Si hay varios coches
        primer_coche = datos[0]
    elif isinstance(datos, dict):  # Si solo hay un coche
        primer_coche = datos
    else:
        print("El archivo no contiene datos válidos.")
        return

    # Extraer las claves del primer coche
    keys_primer_coche = obtener_keys(primer_coche)
    
    # Mostrar las claves
    print("Claves del primer coche:", keys_primer_coche)

# Función recursiva para extraer las keys de un JSON
def obtener_keys(diccionario, keys_acumuladas=None):
    if keys_acumuladas is None:
        keys_acumuladas = []

    for key, valor in diccionario.items():
        keys_acumuladas.append(key)
        if isinstance(valor, dict):
            obtener_keys(valor, keys_acumuladas)
        elif isinstance(valor, list):
            for item in valor:
                if isinstance(item, dict):
                    obtener_keys(item, keys_acumuladas)

    return keys_acumuladas

# Ejemplo de uso: Procesar solo el primer coche en el primer archivo JSON en la carpeta "data"
carpeta_entrada = 'data'
extraer_claves_primer_coche(carpeta_entrada)
