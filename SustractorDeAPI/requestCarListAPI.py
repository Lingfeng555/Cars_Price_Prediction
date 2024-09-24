import requests
import time
import random
import json

#The random delay between request of details
limite_inferio = 1.5
limite_superior = 2.5

#Must be intergers
start = 0
end = 1

url_primary_data = "https://ms-mt--api-mobile.spain.advgo.net/search"

cookies_primary_data = {
    '_csrf': 'KwunAV/Whw4ECYWIgsypO7l8PKLKo4F5VVtUGYLd5GGP/mucf9v62/JC0/UqvsUsJyL+QM2cQvWkB4kLJora1LeR81WitLZ+TbJz+qaD7bg='
}

headers_primary_data = {
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

cookies_details = {
    '_csrf': 'nuwzYfak9vPJAm6hgl/8mEzudyiBtSGthDfjs0vOPLFnS3FRwLVBPWHlFIrNmke6QxXK0lFFfWgLqimD865EEbeR81WitLZ+TbJz+qaD7bg='
}

headers_details = {
    'cache-control': 'no-cache, no-store, max-age=0, must-revalidate',
    'accept-encoding': 'gzip',
    'content-type': 'application/json',
    'user-agent': 'okhttp/4.8.0',
    'x-adevinta-amcvid': '36297421111129133872656379157495233779',
    'x-adevinta-channel': 'android',
    'x-adevinta-euconsent-v2': 'CQFfTckQFfTckAHABAESDgCsAP_AAH_AAAAAg1Nf_X__b2_r8_7_f_t0eY1P9_7__-0zjhfdF-8N3f_X_L8X52M5vF36tqoKuR4ku3bBIUdlHPHcTVmw6okVryPsbk2cr7NKJ7PkmlMbM2dYGH9_n9_z-ZKY7___f__z_v-v___9____7-3f3__5__--__e_V_-9zfn9_____9vP___9v-_9_3________3_r9_7_D_-f_87_XW-9_cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEQagCzDQuIAuwJGQm2jCKBACIKwkKoFABRAJC0QGELq4KdhcBPrCRACBFAAcEAIYAUZAAgAAAgCQiACQI4EAgEAgEAAIAFQgEABGwACgAsBAIABQHQsU4oAlAsIMiMiIUwIQpEgoJ7KBBKD9QVwgDLLACg0f8VCAgUAMVgRCQsXocASAlwkkC3VG-AAhACgFFKFYgk9MAA4JGy1B4Im0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAA',
    'x-adevinta-session-id': 'b2fe2561-7788-4f8d-a982-d6d427de1e7a',
    'x-app-version': '5.98.2',
    'x-schibsted-tenant': 'coches',
    'x-user-agent': '3'
}

def request_primary_data (page: int) -> list :
    data = {
        "pagination": {"page": page, "size": 5},
        "sort": {"order": "desc", "term": "relevance"},
        "experiments": {"tops": "V2"},
        "filters": {
            "cubicCapacity": {},
            "includingPaidItems": False
        }
    }
    time.sleep(random.uniform(1.5, 2.5))
    response = requests.post(url_primary_data, headers=headers_primary_data, cookies=cookies_primary_data, json=data)
    print(f'REQUEST PAGE: {page} ESTATUS CODE: {response.status_code}')
    if(response.status_code != 200): return None
    ret = response.json()["items"]
    for car in ret:
        car.pop("resources")
    return ret

def request_details(id: str) -> dict: 
    url_details = 'https://ms-mt--api-mobile.spain.advgo.net/details/' + str(id)
    response = requests.get(url_details, headers=headers_details, cookies=cookies_details)
    time.sleep(random.uniform(limite_inferio, limite_superior))
    print(f'\tREQUEST CAR ID: {id} ESTATUS CODE: {response.status_code}')
    if(response.status_code != 200): return None
    ret = response.json()
    ret["ad"].pop("photos")
    return ret

def scrap_full_page(page: int) -> list:
    cars = request_primary_data(page)
    for car in cars:
        try:
            car["detail"] = request_details(car["id"])
        except:
            print(f'ERROR AL INTENTAR LEER LA FICHA TECNICA DEL COCHE: {car["id"]}')
    return cars

def sendQuery(start: int, end: int) -> None:
    result = []
    try:
        for i in range (start, end-1):
            cars = scrap_full_page(i)
            cars.pop()
            result = result + cars
        result = result + scrap_full_page(i)
    except:
        print(f'El error ha ocurrido con la pagina {i}')
    with open(f'cars{start}_{end}.json', 'w') as f:
        json.dump(result, f)

sendQuery(start, end)