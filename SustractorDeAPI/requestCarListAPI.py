import requests
import time
import random
import json
from stem import Signal
from stem.control import Controller
from stem.connection import AuthenticationFailure
import logging
import sys
import threading
import math
import os


# Crear el logger
logger = logging.getLogger(f"SCRAPER")
logger.setLevel(logging.DEBUG)  # Configurar el nivel mínimo de logging para el logger



if not os.path.exists("logs"):
    os.makedirs("logs")
if not os.path.exists("data"):
    os.makedirs("data")
    
# Crear un handler para archivo
file_handler = logging.FileHandler(f"logs/{input("Introduce tu nombre: ")}.log")
file_handler.setLevel(logging.DEBUG)  # Guardar todos los niveles en el archivo

# Crear un handler para la consola (terminal)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Imprimir todos los niveles en la consola

# Crear un formato para los logs
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Añadir los handlers al logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

url_primary_data = "https://ms-mt--api-mobile.spain.advgo.net/search"

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

cookies_primary_data = {
    '_csrf': 't2iSZNmQ9R/e9/pP77GHCRLPHjtfCfT1tDcuepnzox3VxteKABxOTLE8MyfD1hBEnLkV4gTj5R9WTI682HBKXbeR81WitLZ+TbJz+qaD7bg='
}

headers_primary_data = {
    'cache-control': 'no-cache, no-store, max-age=0, must-revalidate',
    'content-type': 'application/json; charset=UTF-8',
    'user-agent': 'okhttp/4.8.0',
    'accept-encoding': 'gzip',
    'x-adevinta-amcvid': '70776775951951061133492683443108131625',
    'x-adevinta-channel': 'android',
    'x-adevinta-euconsent-v2': 'CQFijLQQFijLQAHABAESDgCsAP_AAH_AAAAAg1Nf_X__b2_r8_7_f_t0eY1P9_7__-0zjhfdF-8N3f_X_L8X52M5vF36tqoKuR4ku3bBIUdlHPHcTVmw6okVryPsbk2cr7NKJ7PkmlMbM2dYGH9_n9_z-ZKY7___f__z_v-v___9____7-3f3__5__--__e_V_-9zfn9_____9vP___9v-_9_3________3_r9_7_D_-f_87_XW-9_cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQuIAuwJGQm2jCKBACIKwkKoFABRAJC0QGELq4KdhcBPrCRACBFAAcEAIYAUZAAgAAAgCQiACQI4EAgEAgEAAIAFQgEABGwACgAsBAIABQHQsU4oAlAsIMiMiIUwIQpEgoJ7KBBKD9QVwgDLLACg0f8VCAgUAMVgRCQsXocASAlwkkC3VG-AAhACgFFKFYgk9MAA4JGy1B4Im0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAA',
    'x-adevinta-mt-variant': 'abtest6_variant',
    'x-adevinta-session-id': 'fad539b1-639a-4eb2-ac27-40de304c9947',
    'x-app-version': '5.98.2',
    'x-schibsted-tenant': 'coches',
    'x-user-agent': '3'
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

def request_primary_data (page: int) -> list :
    data = {
        "pagination": {"page": page, "size": 100},
        "sort": {"order": "desc", "term": "relevance"},
        "experiments": {"tops": "V2"},
        "filters": {
            "cubicCapacity": {},
            "includingPaidItems": False
        }
    }
    response = requests.post(url_primary_data, headers=headers_primary_data, cookies=cookies_primary_data, json=data, proxies=proxies)
    logger.info(f'REQUEST PAGE: {page} ESTATUS CODE: {response.status_code}')
    if(response.status_code != 200): return None
    ret = response.json()["items"]
    for car in ret:
        car.pop("resources")
        car.pop("phone")
        
    return ret

def request_details(id: str) -> dict: 
    url_details = 'https://ms-mt--api-mobile.spain.advgo.net/details/' + str(id)
    response = requests.get(url_details, headers=headers_details, cookies=cookies_details, proxies=proxies)
    logger.info(f'\tREQUEST CAR ID: {id} ESTATUS CODE: {response.status_code} LEFT : {AQUIQUIEROSABERCUANToSLEFT}')
    if(response.status_code != 200): return None
    ret = response.json()
    ret["ad"].pop("photos")
    return ret

def scrap_full_page(page: int) -> list:
    cars = request_primary_data(page)
    logger.info(f'GETEANDO COCHES DE LA PÁGINA {page} SCRAPEADA')
    for car in cars:
        try:
            car["detail"] = request_details(car["id"])
        except Exception as e:
            logger.info(f"Ocurrió un error inesperado: {e}")
            logger.info(f'ERROR AL INTENTAR LEER LA FICHA TECNICA DEL COCHE: {car["id"]}')
    return cars

def sendQuery(name: str, start: int, end: int) -> None:
    result = []

    for i in range (start, end):
        try:
            cars = scrap_full_page(i)
            cars.pop()
            result = result + cars
        except:
            logger.info(f'ERROR AL SCRAPEAR LA PAGINA {i}')
        logger.info(f'TOTAL DE COCHES REGISTRADOS HASTA AHORA: {len(result)}')
    try:
        result = result + scrap_full_page(end)
    except Exception as e:
        logger.info(f'ERROR AL SCRAPEAR LA ULTIMA PAGINA')
        print(f"Ocurrió un error: {e}")

    logger.info(f'TOTAL DE COCHES REGISTRADOS: {len(result)} ------------------------------------------------------')

    with open(f'data/{name}cars_{start}_{end}.json', 'w') as f:
        json.dump(result, f)

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

def tarea(name, start, end):
    sendQuery(name, start, end)

if __name__ == '__main__':
    start_time = time.time()
    NUMERO_DE_HILOS = 50
    hilos = []
    start = 1001 #inclusive
    end = 1500 #inclusive
    
    print("TOTAL ESTIMADO DE COCHES A SCRAPEAR: ", (end - start) * 100)
    
    BATCH = round((end - start)/NUMERO_DE_HILOS)
    change_tor_ip()

    x = start
    y = BATCH
    for i in range(NUMERO_DE_HILOS):
        t = threading.Thread(target=tarea, args=(f"Thread-{i+1}", x, y))
        hilos.append(t)
        t.start()
        print(f"x: {x}  y: {y}")
        x = y + 1
        y = y + BATCH

    for t in hilos:
        t.join()
        
    end_time = time.time()  # Captura el tiempo al final
    elapsed_time = end_time - start_time  # Calcula el tiempo transcurrido
    logger.info(f'Tiempo total transcurrido: {elapsed_time:.2f} segundos') 
