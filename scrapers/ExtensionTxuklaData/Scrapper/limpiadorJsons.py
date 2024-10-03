import os
import json


ruta_actual = os.path.dirname(os.path.realpath(__file__))
carpeta = os.path.join(ruta_actual, 'data')
carpeta2 = os.path.join(ruta_actual, 'data//result')



# Lista para almacenar todas las URLs
todas_las_urls = []

# Iterar sobre cada archivo .json en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith(".json"):
        # Abrir y leer el contenido del archivo .json
        with open(os.path.join(carpeta, archivo), 'r', encoding='utf-8') as f:
            try:
                urls = json.load(f)
                if isinstance(urls, list):  # Verificar si el contenido es una lista
                    todas_las_urls.extend(urls)
            except json.JSONDecodeError as e:
                print(f"Error leyendo el archivo {archivo}: {e}")

# Eliminar duplicados
todas_las_urls = list(set(todas_las_urls))

# Filtrar las URLs que no contienen '/renting/'
urls_filtradas = [url for url in todas_las_urls if '/renting/' not in url]

# Guardar el resultado en un archivo .json final
resultado_path = os.path.join(carpeta2, 'urlsClean.json')
with open(resultado_path, 'w', encoding='utf-8') as f:
    json.dump(urls_filtradas, f, ensure_ascii=False, indent=4)

print(f"Proceso completado. Archivo guardado en {resultado_path}")
