import requests

# Definir la URL de la solicitud
url = "https://ms-mt--api-mobile.spain.advgo.net/details/58070687"

# Definir las cookies
cookies = {
    '_csrf': 'nuwzYfak9vPJAm6hgl/8mEzudyiBtSGthDfjs0vOPLFnS3FRwLVBPWHlFIrNmke6QxXK0lFFfWgLqimD865EEbeR81WitLZ+TbJz+qaD7bg='
}

# Definir los headers
headers = {
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


response = requests.get(url, headers=headers, cookies=cookies)

with open(f'details.json', 'w') as f:
    f.write(response.text)

print(response.status_code)
print(response.json())  
