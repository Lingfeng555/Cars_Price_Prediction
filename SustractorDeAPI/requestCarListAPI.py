import requests
import time



# Definir la URL de la request
url = "https://ms-mt--api-mobile.spain.advgo.net/search"

# Definir las cookies
cookies = {
    '_csrf': 'KwunAV/Whw4ECYWIgsypO7l8PKLKo4F5VVtUGYLd5GGP/mucf9v62/JC0/UqvsUsJyL+QM2cQvWkB4kLJora1LeR81WitLZ+TbJz+qaD7bg='
}

# Definir los headers
headers = {
    'cache-control': 'no-cache, no-store, max-age=0, must-revalidate',
    'content-type': 'application/json; charset=UTF-8',
    'user-agent': 'okhttp/4.8.0',
    'accept-encoding': 'gzip',
    'x-adevinta-amcvid': '13077773087506042612001499188921092246',
    'x-adevinta-channel': 'android',
    'x-adevinta-euconsent-v2': 'CQFfOEgQFfOEgAHABAESDgCsAP_AAH_AAAAAg1Nf_X__b2_r8_7_f_t0eY1P9_7__-0zjhfdF-8N3f_X_L8X52M5vF36tqoKuR4ku3bBIUdlHPHcTVmw6okVryPsbk2cr7NKJ7PkmlMbM2dYGH9_n9_z-ZKY7___f__z_v-v___9____7-3f3__5__--__e_V_-9zfn9_____9vP___9v-_9_3________3_r9_7_D_-f_87_XW-9_cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQuIAuwJGQm2jCKBACIKwkKoFABRAJC0QGELq4KdhcBPrCRACBFAAcEAIYAUZAAgAAAgCQiACQI4EAgEAgEAAIAFQgEABGwACgAsBAIABQHQsU4oAlAsIMiMiIUwIQpEgoJ7KBBKD9QVwgDLLACg0f8VCAgUAMVgRCQsXocASAlwkkC3VG-AAhACgFFKFYgk9MAA4JGy1B4Im0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAA',
    'x-adevinta-mt-variant': 'abtest6_variant',
    'x-adevinta-session-id': 'c21c16db-e33d-4979-8348-e4b619d5084a',
    'x-app-version': '5.98.2',
    'x-schibsted-tenant': 'coches',
    'x-user-agent': '3'
}



for n in range(1,3):
    
    data = {
    "pagination": {"page": n, "size": 100},
    "sort": {"order": "desc", "term": "relevance"},
    "experiments": {"tops": "V2"},
    "filters": {
        "cubicCapacity": {},
        "includingPaidItems": True
        # Agregar aquí los demás filtros si son necesarios
    }
    }
    
    
    response = requests.post(url, headers=headers, cookies=cookies, json=data)
    time.sleep(1)
    #guardar la respuesta en un archivo
    with open(f'response{n}.json', 'w') as f:
        f.write(response.text)
        

# Verificar la respuesta
print(response.status_code)
print(response.json())
