import httpx
import gzip
import json
import asyncio
from typing import List
from ..models.cne import EstacionServicioInput
from services.redis_service import RedisService

#pasamos de la lógica simple de http.client al plan técnico, que recomienda usar httpx (async)
#'Esto evitará bloquear los hilos del servidor mientras esperas la respuesta de la CNE.  '

class CNEService:
    def __init__(self, api_token: str):
        self.base_url = "https://api.cne.cl"
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.redis = RedisService()

    #-----------
    #buscar que hace async aca
    #-----------
    async def fetch_all_estaciones(self) -> List[EstacionServicioInput]:
        # httpx maneja la decompressión gzip de forma automática si los headers están bien,
        # si la API de CNE es muy estricta se replica lo que hice en el otro código (en /api_cne)
        async with httpx.AsyncClient() as client: #???
            response = await client.get(f"{self.base_url}/api/v4/estaciones", headers=self.headers)

            if response.status_code != 200:
                raise Exception(f"Error al conectar con CNE: {response.status_code}")
            
            #si el contenido viene en raw gzip
            try:
                content = gzip.decompress(response.content).decode("utf-8")
                raw_json = json.loads(content)
            except:
                #fallback por si httpx ya lo tenia descomprimido
                raw_json = response.json()

            #esta es la gracia de pydantic, que es parseo y validación automática
            #si hay algun atributo incorrecto, sale validation error
            return [EstacionServicioInput(**estacion) for estacion in raw_json]

    async def get_precios_providencia(self, api_token: str) -> List[EstacionServicioInput]:
        all_stations = await self.fetch_all_estaciones()
        
        # Filtramos usando los objetos tipados con un rendimiento óptimo
        filtradas = [
            estacion for estacion in all_stations
            if estacion.ubicacion.nombre_region == "Metropolitana de Santiago" 
            and estacion.ubicacion.nombre_comuna == "Providencia"
        ]
        return filtradas

async def main():
  token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jbmUuY2wvYXBpL2xvZ2luIiwiaWF0IjoxNzg1MTg4NzU4LCJleHAiOjE3ODUxOTIzNTgsIm5iZiI6MTc4NTE4ODc1OCwianRpIjoiVGJ6UWFIZVAxMUlnc0p1OCIsInN1YiI6IjQ2MjMiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.XMtiRasWTh_zW3UoiXcJengP7iZCb_Adt17r1pscPl0"
  service = CNEService(api_token=token)

  try:
    resultados = await service.get_precios_providencia("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5jbmUuY2wvYXBpL2xvZ2luIiwiaWF0IjoxNzg1MTg4NzU4LCJleHAiOjE3ODUxOTIzNTgsIm5iZiI6MTc4NTE4ODc1OCwianRpIjoiVGJ6UWFIZVAxMUlnc0p1OCIsInN1YiI6IjQ2MjMiLCJwcnYiOiIyM2JkNWM4OTQ5ZjYwMGFkYjM5ZTcwMWM0MDA4NzJkYjdhNTk3NmY3In0.XMtiRasWTh_zW3UoiXcJengP7iZCb_Adt17r1pscPl0")
    print(f"Se encontraron {len(resultados)} estaciones en Providencia.")
  except Exception as e:
    print(f"Ocurrió un error: {e}")


if __name__ == "__main__":
  asyncio.run(main())