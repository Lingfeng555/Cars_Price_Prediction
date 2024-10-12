import json
import os 
import pandas as pd
import numpy as np
import urllib.request
import requests
import sys
from PIL import Image
import zipfile
import shutil

from stem import Signal
from stem.control import Controller
from stem.connection import AuthenticationFailure

import threading

import os

# Agregar la carpeta 'scrapers' al sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Importar el Logger
import logging
from utils.logger import Logger

logger = Logger(name="PHOTOGRAPHER", log_file="scrapers/Photografer/logs/photographer.log").get_logger()

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

cookies_details = {
    '_csrf': 'jtmzuMqtWLjV4EgHNIXW0Yjrt5wlRaeyX7uf1+VR2Vn9aKoAaGjj1AGdFf2IyLa++KNpquuNwrSclnfdXiWhxbeR81WitLZ+TbJz+qaD7bg='
}

headers_details = {
    'cache-control': 'no-cache, no-store, max-age=0, must-revalidate',
    'accept-encoding': 'gzip',
    'content-type': 'application/json',
    'user-agent': 'okhttp/4.8.0',
    'x-adevinta-amcvid': '70776775951951061133492683443108131625',
    'x-adevinta-channel': 'android',
    'x-adevinta-euconsent-v2': 'CQFijLQQFijLQAHABAESDgCsAP_AAH_AAAAAg1Nf_X__b2_r8_7_f_t0eY1P9_7__-0zjhfdF-8N3f_X_L8X52M5vF36tqoKuR4ku3bBIUdlHPHcTVmw6okVryPsbk2cr7NKJ7PkmlMbM2dYGH9_n9_z-ZKY7___f__z_v-v___9____7-3f3__5__--__e_V_-9zfn9_____9vP___9v-_9_3________3_r9_7_D_-f_87_XW-9_cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQuIAuwJGQm2jCKBACIKwkKoFABRAJC0QGELq4KdhcBPrCRACBFAAcEAIYAUZAAgAAAgCQiACQI4EAgEAgEAAIAFQgEABGwACgAsBAIABQHQsU4oAlAsIMiMiIUwIQpEgoJ7KBBKD9QVwgDLLACg0f8VCAgUAMVgRCQsXocASAlwkkC3VG-AAhACgFFKFYgk9MAA4JGy1B4Im0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAA',
    'x-adevinta-session-id': 'fad539b1-639a-4eb2-ac27-40de304c9947',
    'x-app-version': '5.98.2',
    'x-schibsted-tenant': 'coches',
    'x-user-agent': '3'
}

def get_public_ip():
    response = requests.get('https://httpbin.org/ip', proxies=proxies)
    return response.json()["origin"]

def change_tor_ip():
    logger.info(f'IP INICIAL: {get_public_ip()}')
    with Controller.from_port(port=9051) as controller:
        password = input("Introduce la contraseña de Tor: ")
        try:
            # Intentar autenticarse con la contraseña proporcionada
            controller.authenticate(password=password) #Por defecto duende_verde
            logger.info("Autenticación exitosa")
            # Si la autenticación es exitosa, se puede cambiar el circuito
            controller.signal(Signal.NEWNYM)
            logger.info("IP cambiada a través de Tor")
            logger.info(f'IP CAMBIADO: {get_public_ip()}')
        except AuthenticationFailure:
            # Si la autenticación falla, muestra un mensaje y no permite la conexión
            logger.info("Error: La contraseña es incorrecta. No se puede conectar al ControlPort.")
            sys.exit()
        except Exception as e:
            # Captura cualquier otro tipo de excepción
            logger.info(f"Ocurrió un error inesperado: {e}")

def compress_image(logger, input_path, output_path, quality=70):
    # Abrir la imagen
    img = Image.open(input_path)
    
    # Guardar la imagen con compresión
    img.save(output_path, 'JPEG', quality=quality, optimize=True)
    
    # Obtener el tamaño del archivo comprimido
    size_before = os.path.getsize(input_path) / (1024 * 1024)  # Convertir a MB
    size_after = os.path.getsize(output_path) / (1024 * 1024)   # Convertir a MB
    logger.info(f"\tTamaño original: {size_before:.2f} MB")
    logger.info(f"\tTamaño comprimido: {size_after:.2f} MB")

def zip_folder_and_remove(logger, folder_path, output_path):
    # Comprimir la carpeta
    logger.info(f"\tZipping: {output_path}")
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    logger.info(f"\tZipped: {output_path}")
    # Eliminar la carpeta original después de comprimirla
    shutil.rmtree(folder_path)

def merge_csv_files_from_folder(folder_path):
    # Lista para almacenar los DataFrames
    df_list = []

    # Recorrer todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            # Obtener la ruta completa del archivo
            file_path = os.path.join(folder_path, filename)
            
            # Leer el archivo CSV y agregarlo a la lista de DataFrames
            df = pd.read_csv(file_path)
            df_list.append(df)

    # Concatenar todos los DataFrames en uno solo
    if df_list:
        merged_df = pd.concat(df_list, ignore_index=True)
        return merged_df
    else:
        print("No se encontraron archivos CSV en la carpeta.")
        return pd.DataFrame()  

def download_image(logger, url, filename):
    logger.info(f"\tDownloading: {url}")
    try:
        response = requests.get(url, proxies=proxies, timeout=30, headers=headers_details, cookies=cookies_details)
        response.raise_for_status()  

        with open(filename, 'wb') as f:
            f.write(response.content)

        compress_image(logger, filename, filename, quality=70)
    except requests.exceptions.RequestException as e:
        logger.info(f"\tERROR descargando {url}: {e}")
        return
    except Exception as e:
        logger.info(f"\tERROR general: {e}")
        return

    logger.info(f"\tDownloaded: {url} as {filename}")

def download_images_of_car(logger, base_path, id, urls):
    logger.info(f"Downloading images of the car: {id}")
    folder_path = os.path.join(base_path, str(id))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for i, url in enumerate(urls):
        filename = os.path.join(folder_path, f"imagen_{i + 1}.jpg")
        download_image(logger, url, filename)
    
    zip_folder_and_remove(logger, folder_path, folder_path + ".zip")

    logger.info(f"Downloaded images of the car in: {folder_path}")

def apply_download_to_row(logger, row, base_path):
    download_images_of_car(logger, base_path, row['id'], eval(row['images']))

def task(data, i, part):
    logger = Logger(name= f"PHOTOGRAPHER-{i}", log_file=f"scrapers/Photografer/logs/threads/part_{part}/photographer_{i}.log").get_logger()

    data.apply(lambda row: apply_download_to_row(logger , row, base_path), axis=1)

if __name__ == '__main__':

    proxy_handler = urllib.request.ProxyHandler(proxies)
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    change_tor_ip()

    part = input("Introduce your part [1-4]: ")
    data = merge_csv_files_from_folder(f"scrapers/Photografer/photos_urls/part_{part}")

    print(f"You can monitor all your threads in CARS_PRICE_PREDICTION/scrapers/Photographer/logs/part_{part}")

    base_path = input("Introduce the absolute path where you want to store the images; it must be already created folder\n(empty for default E:/images): ")

    if (base_path == None) or (base_path == ""):base_path = "E:/images"

    print(data["model"].value_counts())
    print(data["brand"].value_counts())
    print(f"Total: {len(data)}")

    NUMBER_OF_THREADS = int(input("Introduce the number of threads you want to use: "))
    threads = []

    # Aplicamos la función para cada fila del DataFrame
    #data.apply(lambda row: apply_download_to_row(row, base_path), axis=1)
    chunks = np.array_split(data, NUMBER_OF_THREADS)  # 'x' es el número de partes

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i} started with Thread-{i}")

        t = threading.Thread(target=task, args=(chunk, i, part))
        threads.append(t)
        t.start()
        #print(type(chunk))

    
    for i in range(len(threads)):
        threads[i].join()
        logger.info(f"Thread-{i} completed")