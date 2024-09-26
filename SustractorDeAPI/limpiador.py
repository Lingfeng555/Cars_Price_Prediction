import os
import json

# Función para extraer datos relevantes de cada coche
def extraer_datos_relevantes(json_data):
    # Extraer la información importante
    nuevo_json = {
        "id": json_data.get("id"),
        "url": json_data.get("url"),
        "price": json_data.get("price", {}).get("amount"),
        "km": json_data.get("km"),
        "year": json_data.get("year"),
        "color": json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("color"),
        "cubicCapacity": json_data.get("cubicCapacity"),
        "brand": json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("specs", {}).get("make"),
        "model": json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("specs", {}).get("model"),
        "version":json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("specs", {}).get("version"),
        "car_id":json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("specs", {}).get("uniqueVehicleId"),
        "fuelType": json_data.get("fuelType"),
        "transmissionTypeId": json_data.get("transmissionTypeId"),
        "doors": json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("specs", {}).get("doors"),
        "seatingCapacity": json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("specs", {}).get("seatingCapacity"),
        "warranty_months": json_data.get("detail", {}).get("ad", {}).get("warranty", {}).get("months"),
        "province": json_data.get("location", {}).get("mainProvince"),
        "environmentalLabel": json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("specs", {}).get("environmentalLabel"),
        "co2Emissions": json_data.get("detail", {}).get("ad", {}).get("vehicle", {}).get("specs", {}).get("co2Emissions"),
        "co2EmissionsGramsPerKm": json_data.get("detail", {}).get("vehicleSpecs", {}).get("co2EmissionsGramsPerKm"),
        "consumption": json_data.get("detail", {}).get("vehicleSpecs", {}).get("consumption"),
        "dimensions": json_data.get("detail", {}).get("vehicleSpecs", {}).get("dimensionsInMillimeters"),
        "trunkCapacityInLiters": json_data.get("detail", {}).get("vehicleSpecs", {}).get("trunkCapacityInLiters"),
        "maxSpeed": json_data.get("detail", {}).get("vehicleSpecs", {}).get("maxSpeed"),
        "acceleration": json_data.get("detail", {}).get("vehicleSpecs", {}).get("acceleration"),
        "vehicleStandardEquipmentGroup": json_data.get("detail", {}).get("vehicleSpecs", {}).get("vehicleStandardEquipmentGroup"),
        
    }
    
    return nuevo_json

# Función para recorrer los archivos en la carpeta "data"
def procesar_archivos_json(carpeta_entrada, carpeta_salida, max_archivos):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)
        print(f"Carpeta '{carpeta_salida}' creada.")
    
    archivos = os.listdir(carpeta_entrada)  # Listar todos los archivos en la carpeta de entrada
    archivos_json = [archivo for archivo in archivos if archivo.endswith('.json')]  # Filtrar solo archivos JSON
    procesados = 0  # Contador de archivos procesados
    
    for archivo in archivos_json:
        if procesados >= max_archivos:
            break  # Parar si se alcanzó el límite de archivos a procesar
        
        ruta_archivo = os.path.join(carpeta_entrada, archivo)  # Obtener ruta completa del archivo
        print(f"Procesando archivo: {ruta_archivo}")
        
        # Leer el archivo JSON
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            datos = json.load(file)
        
        # Si el archivo contiene varios coches, procesar cada uno
        if isinstance(datos, list):  # En caso de que haya varios coches en una lista
            coches_filtrados = [extraer_datos_relevantes(coche) for coche in datos]
        else:  # En caso de que solo haya un coche
            coches_filtrados = extraer_datos_relevantes(datos)
        
        # Guardar el nuevo archivo JSON con los datos filtrados
        nuevo_nombre = f"filtrado_{archivo}"
        ruta_nueva = os.path.join(carpeta_salida, nuevo_nombre)
        
        with open(ruta_nueva, 'w', encoding='utf-8') as outfile:
            json.dump(coches_filtrados, outfile, ensure_ascii=False, indent=4)
        
        print(f"Archivo procesado y guardado como: {ruta_nueva}")
        procesados += 1

# Ejemplo de uso: Procesar hasta 3 archivos JSON en la carpeta "data" y guardar en "data_limpia"
carpeta_entrada = 'data'
carpeta_salida = 'data_limpia'
max_archivos = 3  # Cambia este valor para controlar cuántos archivos quieres procesar
procesar_archivos_json(carpeta_entrada, carpeta_salida, max_archivos)
