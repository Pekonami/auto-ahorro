import dotenv
import http.client
import gzip
import json, os
from dotenv import set_key

def main_api_cne_token():
    config = dotenv.dotenv_values(".env")

    my_email = config.get("correo")
    my_password = config.get("contrasena")

    conn = http.client.HTTPSConnection("api.cne.cl")

    payload = f"email={my_email}&password={my_password}"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    conn.request("POST", "/api/login", payload, headers)
    res = conn.getresponse()
    token_code = res.read()
    token = token_code.decode("utf-8")

    return token[10:len(token) - 2]

def main_est_servicio_data():
    conn = http.client.HTTPSConnection("api.cne.cl")
    payload = ''

    API_CNE = main_api_cne_token()
    set_key(".env", "API_CNE", API_CNE)

    headers = {
    'Authorization': f'Bearer {API_CNE}'
    }

    conn.request("GET", "/api/v4/estaciones", payload, headers)
    res = conn.getresponse()
    data = res.read()

    decompressed_data = gzip.decompress(data)
    result = decompressed_data.decode('utf-8')
    json_data = json.loads(result)

    datos_filtrados = []
    for linea in json_data:
        datos_filtrados.append(linea)
    with open("api_cne/estaciones_servicio/estaciones_servicio_data.json", "w", encoding="utf-8") as file:
        json.dump(datos_filtrados, file, indent=4, ensure_ascii=False)

main_est_servicio_data()
#con esto cargamos toda la data de las estaciones en estaciones_servicio_data.json

#with open("datos_api_cne.json", "w") as file:
    #data = json_data
