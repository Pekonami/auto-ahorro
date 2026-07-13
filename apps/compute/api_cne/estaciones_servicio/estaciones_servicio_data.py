import dotenv
import http.client
import gzip
import json, os

def main_est_servicio_data():
    conn = http.client.HTTPSConnection("api.cne.cl")
    payload = ''

    config = dotenv.dotenv_values(".env")

    API_CNE = config.get("API_CNE")

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
        if linea["ubicacion"]["nombre_region"] == "Metropolitana de Santiago":
            datos_filtrados.append(linea)

    with open("api_cne/estaciones_servicio/estaciones_servicio_data.json", "w", encoding="utf-8") as file:
        json.dump(datos_filtrados, file, indent=4, ensure_ascii=False)

#with open("datos_api_cne.json", "w") as file:
    #data = json_data
